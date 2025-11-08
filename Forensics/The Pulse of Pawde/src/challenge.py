#!/usr/bin/env python3
# make_challenge.py
#
# Captures live traffic on INTERFACE, synthesizes ICMP timing-channel packets
# encoding the provided binary string, merges them, and writes a challenge PCAP.
# After writing the PCAP it uses 'editcap' to add the requested capture comment.
#
# NOTE: This script requires:
#  - root (or capture) privileges to sniff live traffic
#  - tshark/editcap (part of Wireshark) installed for adding the capture comment
#

from scapy.all import sniff, wrpcap, Ether, IP, ICMP
import random
import os
import sys
import time
import tempfile
import subprocess
import shutil

# === CONFIGURATION ===
INTERFACE = "eth0"                 # capture interface
CAPTURE_DURATION = 1800              # seconds to capture background traffic
OUTPUT_PCAP = "challenge.pcap"     # final output file (after editcap)
TMP_PCAP = None                    # will be created in tempdir
SRC_MAC = "00:11:22:33:44:55"
DST_MAC = "66:77:88:99:aa:bb"
SRC_IP = "192.168.42.100"
DST_IP = "192.168.42.129"

# Capture comment to inject (exact string requested)
CAPTURE_COMMENT = (
    "This might be of use to you "
    "9f3b2e49e4c7a0d13b184cc2a67f5c01, "
    "2e8ac13fce7a91d8fa8f75e90b1c52d4"
)

# Binary data to encode (same as before)
binary_data = """00110011 01100010 00111000 00110110 00110000 00110011 01100101 00111000 
00110111 00110111 00111001 01100011 01100001 00110110 01100001 00110100 
01100011 00111000 00110000 00110001 00111000 00110000 00110011 01100100 
01100001 00110001 00110011 00110001 00110111 01100001 00110000 00110101 
00110111 00110001 00110010 00110101 00110100 01100010 00111001 01100110 
01100001 01100001 01100011 00110010 01100100 00111001 00110001 00111000 
00111000 00110100 00111000 01100101 01100110 00110110 01100101 01100110 
00110010 01100100 00110111 00111000 01100011 00110100 00110100 00110011 
00110011 01100101 00111000 00110011 00110100 00111000 00110011 01100001 
00110101 01100010 00110010 01100110 00110011 01100100 01100001 00111000 
01100001 00110101 00110100 00111000 01100011 00110111 01100110 00110110 
01100010 01100010 00111000 00110111 01100001 01100011 01100100 00110100"""
binary_data = binary_data.replace(" ", "").replace("\n", "")

# Timing encoding ranges
DELAY_RANGE_0 = (0.20, 0.49)
DELAY_RANGE_1 = (1.10, 1.49)

# === FUNCTIONS ===

def build_icmp_pairs(binary_string, base_time):
    """Generate Ethernet/IP/ICMP request/reply pairs encoding bits via timing."""
    pkts = []
    timestamp = base_time
    seq = 0

    for bit in binary_string:
        # Choose delay per bit
        delay = random.uniform(*DELAY_RANGE_1) if bit == "1" else random.uniform(*DELAY_RANGE_0)

        # ICMP Echo Request
        req = (
            Ether(src=SRC_MAC, dst=DST_MAC)
            / IP(src=SRC_IP, dst=DST_IP)
            / ICMP(type=8, id=0x1337, seq=seq)
        )
        req.time = timestamp

        # ICMP Echo Reply
        rep = (
            Ether(src=DST_MAC, dst=SRC_MAC)
            / IP(src=DST_IP, dst=SRC_IP)
            / ICMP(type=0, id=0x1337, seq=seq)
        )
        rep.time = timestamp + delay

        pkts.extend([req, rep])
        timestamp += delay + random.uniform(0.05, 0.25)
        seq += 1

    print(f"[+] Generated {len(pkts)} ICMP packets encoding {len(binary_string)} bits")
    print(f"[*] ICMP duration: {pkts[-1].time - base_time:.1f}s")
    return pkts


def add_capture_comment_with_editcap(infile, outfile, comment):
    """
    Use Wireshark's editcap to add a capture file comment.
    editcap usage: editcap --capture-comment "<comment>" infile outfile
    Returns True on success, False otherwise.
    """
    editcap_cmd = shutil.which("editcap")
    if not editcap_cmd:
        print("[!] editcap not found on PATH; cannot add capture comment.")
        return False

    try:
        # Run editcap to produce final outfile with the capture comment
        subprocess.run([editcap_cmd, "--capture-comment", comment, infile, outfile],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] editcap failed: {e}. stderr:\n{e.stderr.decode(errors='ignore')}")
        return False
    except Exception as ex:
        print(f"[!] Unexpected error running editcap: {ex}")
        return False


def main():
    global TMP_PCAP

    print(f"[*] Capturing background traffic on {INTERFACE} for {CAPTURE_DURATION}s...")
    try:
        captured_packets = sniff(iface=INTERFACE, timeout=CAPTURE_DURATION)
    except Exception as e:
        print(f"[!] Error capturing on {INTERFACE}: {e}")
        sys.exit(1)

    print(f"[+] Captured {len(captured_packets)} packets")

    # Get timeline bounds
    if not captured_packets:
        base_time_min = time.time()
        base_time_max = base_time_min + 100
    else:
        base_time_min = min(p.time for p in captured_packets)
        base_time_max = max(p.time for p in captured_packets)

    print(f"[*] Background timeline: {base_time_min:.3f} → {base_time_max:.3f}")

    # Choose an insertion start time safely inside the captured span
    start_time = random.uniform(base_time_min, max(base_time_min + 1.0, base_time_max - 10))
    icmp_packets = build_icmp_pairs(binary_data, start_time)

    # Merge and sort chronologically
    combined = list(captured_packets) + icmp_packets
    combined.sort(key=lambda p: p.time)

    # Write to a temporary pcap first (so we can call editcap to add comment)
    tmpdir = tempfile.mkdtemp(prefix="make_challenge_")
    TMP_PCAP = os.path.join(tmpdir, "tmp_challenge.pcap")
    try:
        wrpcap(TMP_PCAP, combined)
        print(f"[*] Wrote temporary PCAP: {TMP_PCAP} ({len(combined)} packets)")
    except Exception as e:
        print(f"[!] Failed to write temporary PCAP: {e}")
        shutil.rmtree(tmpdir, ignore_errors=True)
        sys.exit(1)

    # Try to add capture comment using editcap -> produce OUTPUT_PCAP
    success = add_capture_comment_with_editcap(TMP_PCAP, OUTPUT_PCAP, CAPTURE_COMMENT)
    if success:
        print(f"[+] Capture comment added and final PCAP created: {OUTPUT_PCAP}")
        # clean up temp
        try:
            os.remove(TMP_PCAP)
            os.rmdir(tmpdir)
        except Exception:
            pass
    else:
        # If editcap failed, fall back to writing the temporary file as the final file (without capture comment)
        try:
            shutil.move(TMP_PCAP, OUTPUT_PCAP)
            shutil.rmtree(tmpdir, ignore_errors=True)
            print(f"[!] editcap unavailable or failed — wrote PCAP without capture comment: {OUTPUT_PCAP}")
            print(f"[!] If you want the capture comment embedded, install 'editcap' (part of Wireshark/tshark).")
        except Exception as e:
            print(f"[!] Failed to move temporary PCAP into place: {e}")
            shutil.rmtree(tmpdir, ignore_errors=True)
            sys.exit(1)

    print(f"[+] Challenge PCAP ready: {OUTPUT_PCAP} ({len(combined)} packets total)")
    print("\n[✓] Done — live capture merged with ICMP encoding traffic.")

if __name__ == "__main__":
    main()
