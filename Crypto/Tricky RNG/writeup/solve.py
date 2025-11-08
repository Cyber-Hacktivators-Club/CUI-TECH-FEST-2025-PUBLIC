#!/usr/bin/env python3
"""
decrypt_trickyrng.py

Usage:
  python3 decrypt_trickyrng.py --cipher <cipher_hex> --recorded "Wed Oct 24 2025 10:06:29 UTC+0000"

If the exact recorded time is a little off, you can try a brute-force window:
  python3 decrypt_trickyrng.py --cipher <cipher_hex> --recorded "..." --brute -60 60

The script will print any candidate plaintexts that look like CHC{...} and other helpful info.
"""
import argparse
import random
from datetime import datetime, timezone, timedelta
import re
import sys

KEY_LEN = 12
FLAG_RE = re.compile(r"^CHC\{[^\}]+\}$")
FLAG_BYTES_RE = re.compile(b"CHC\\{[^\\}]+\\}")

def parse_recorded(recorded: str) -> datetime:
    """
    Parse the recorded string printed by challenge.py.
    Expected inner format: '%a %b %d %Y %H:%M:%S UTC+0000'
    We'll strip the trailing ' UTC+0000' and parse the rest, set tzinfo=UTC.
    """
    # allow the user to pass either the full bracketed form or just the inner datetime
    s = recorded.strip()
    # if user passed "[ ... ]" or "Recorded: [ ... ]"
    if "[" in s and "]" in s:
        # extract inside the first pair of brackets
        s = s[s.find("[")+1:s.find("]")]
    # strip any leading/trailing whitespace
    s = s.strip()
    # if the trailing timezone token exists, remove it (we set tz to UTC explicitly)
    if s.endswith("UTC+0000"):
        s_no_tz = s[: -len("UTC+0000")].strip()
    else:
        s_no_tz = s
    # The remaining format should be like: 'Wed Oct 24 2025 10:06:29'
    # Use strptime with %a %b %d %Y %H:%M:%S
    try:
        dt = datetime.strptime(s_no_tz, "%a %b %d %Y %H:%M:%S")
    except ValueError as e:
        raise ValueError(f"Could not parse recorded datetime: '{recorded}' ({e})")
    # set timezone to UTC (challenge printed UTC+0000)
    return dt.replace(tzinfo=timezone.utc)

def decrypt_with_seed(seed: int, cipher: bytes) -> bytes:
    rnd = random.Random(seed)
    key = [rnd.randint(0, 255) for _ in range(KEY_LEN)]
    plaintext = bytes([cipher[i] ^ key[i % KEY_LEN] for i in range(len(cipher))])
    return plaintext

def try_exact(cipher_hex: str, recorded: str):
    cipher = bytes.fromhex(cipher_hex)
    dt = parse_recorded(recorded)
    seed = int(dt.timestamp())
    plaintext = decrypt_with_seed(seed, cipher)
    return seed, plaintext

def brute_window(cipher_hex: str, recorded: str, start_offset: int, end_offset: int):
    cipher = bytes.fromhex(cipher_hex)
    base_dt = parse_recorded(recorded)
    base_seed = int(base_dt.timestamp())
    results = []
    for offset in range(start_offset, end_offset + 1):
        seed = base_seed + offset
        plaintext = decrypt_with_seed(seed, cipher)
        # quick checks
        if FLAG_BYTES_RE.search(plaintext):
            results.append((seed, offset, plaintext))
        else:
            # try utf-8 decode full and regex match
            try:
                text = plaintext.decode('utf-8')
                if FLAG_RE.match(text):
                    results.append((seed, offset, plaintext))
            except UnicodeDecodeError:
                # skip
                pass
    return results

def pretty_print(seed: int, offset: int, plaintext: bytes):
    print("=== CANDIDATE ===")
    print(f"seed: {seed} (offset {offset:+d} seconds relative to recorded)")
    print(f"plaintext (repr): {repr(plaintext)}")
    # try safe decode with replacement to view text
    try:
        text = plaintext.decode('utf-8')
        print("plaintext (utf-8):", text)
    except UnicodeDecodeError:
        print("plaintext (utf-8, errors=replace):", plaintext.decode('utf-8', errors='replace'))
    # if ascii-flag present, extract and print
    m = FLAG_BYTES_RE.search(plaintext)
    if m:
        print("extracted flag (ascii):", m.group(0).decode('ascii', errors='replace'))
    print("=================\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cipher", required=True, help="ciphertext hex printed by challenge (no 0x)")
    p.add_argument("--recorded", required=True, help="Recorded datetime string (use exactly what challenge prints inside brackets)")
    p.add_argument("--brute", nargs=2, type=int, metavar=('START','END'), help="Optional offset window in seconds (e.g. -60 60)")
    args = p.parse_args()

    # Try exact first
    try:
        seed, plaintext = try_exact(args.cipher, args.recorded)
    except Exception as e:
        print("Error parsing recorded time:", e, file=sys.stderr)
        sys.exit(2)

    # If exact yields a flag or ascii CHC pattern, print and exit
    if FLAG_BYTES_RE.search(plaintext):
        pretty_print(seed, 0, plaintext)
        return
    # try utf decode full match
    try:
        t = plaintext.decode('utf-8')
        if FLAG_RE.match(t):
            pretty_print(seed, 0, plaintext)
            return
    except UnicodeDecodeError:
        pass

    # No exact hit — if user requested brute window, run it
    if args.brute:
        start, end = args.brute
        print(f"No exact match for seed {seed}. Brute-forcing offsets from {start} to {end} seconds...")
        results = brute_window(args.cipher, args.recorded, start, end)
        if not results:
            print("No candidates found in that window.")
            return
        for s, offset, pt in results:
            pretty_print(s, offset, pt)
        return

    # If we get here, nothing found and no brute requested. Print diagnostic info.
    print("No valid flag found using the exact recorded datetime.")
    print("If you suspect the printed 'Recorded' was altered/rounded or timezone-shifted,")
    print("try using the --brute START END option to search a window of seconds around it.")
    print(f"(seed derived from recorded datetime would be: {seed})")
    print("Plaintext raw bytes (hex):", plaintext.hex())
    try:
        print("Plaintext (utf-8 ignore):", plaintext.decode('utf-8', errors='ignore'))
    except Exception:
        pass

if __name__ == "__main__":
    main()
