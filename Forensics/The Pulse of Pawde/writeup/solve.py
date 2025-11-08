#!/usr/bin/env python3
from scapy.all import rdpcap, ICMP
import subprocess, re, math
from Crypto.Cipher import AES

PCAP = "challenge.pcapng"

# --- Extract binary bits from ICMP timing ---
pkts = rdpcap(PCAP)
req, bits = {}, []

for p in pkts:
    if ICMP in p:
        icmp = p[ICMP]
        if icmp.type == 8:
            req[(icmp.id, icmp.seq)] = p.time
        elif icmp.type == 0 and (icmp.id, icmp.seq) in req:
            delta = p.time - req[(icmp.id, icmp.seq)]
            bits.append(str(int(math.floor(delta))))

binary = ''.join(bits)
print(f"[+] Extracted {len(binary)} bits")

# --- Convert binary to ASCII string ---
ascii_text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
print(f"[+] Decoded ASCII: {ascii_text[:60]}{'...' if len(ascii_text) > 60 else ''}")

# --- Extract key & IV from pcap comment ---
out = subprocess.run(["capinfos", PCAP], capture_output=True, text=True).stdout
m = re.search(r"Capture comment:\s*.*?([0-9a-f]{32}).*?([0-9a-f]{32})", out, re.I)
if not m:
    raise SystemExit("Key/IV not found in pcap comment!")

key_hex, iv_hex = m.group(1).lower(), m.group(2).lower()
key, iv = bytes.fromhex(key_hex), bytes.fromhex(iv_hex)

print(f"Using key: {key_hex}")
print(f"Using IV : {iv_hex}")

# --- AES-128-CBC decrypt ---
data = bytes.fromhex(ascii_text)
pt = AES.new(key, AES.MODE_CBC, iv).decrypt(data)

# remove PKCS#7 padding
pad = pt[-1]
if 1 <= pad <= 16 and all(x == pad for x in pt[-pad:]): 
    pt = pt[:-pad]

print("[+] Decrypted output:")
print(pt.decode(errors='ignore'))
