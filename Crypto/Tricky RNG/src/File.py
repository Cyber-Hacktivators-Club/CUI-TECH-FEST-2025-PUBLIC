#!/usr/bin/env python3
"""
challenge.py - per-connection program for Tricky RNG

Reads /flag.txt, picks a random UTC timestamp (±~6 days), derives a seed,
XOR-encrypts the flag with a 12-byte key derived from that seed, and prints
only the banner + lore + Recorded time + ciphertext (hex) to stdout.

Designed to be executed per-connection by socat:
  socat TCP-LISTEN:8082,reuseaddr,fork EXEC:"python3 /app/challenge.py"
"""
import os
import random
import sys
from datetime import datetime, timezone, timedelta

FLAG_PATH = "/flag.txt"
KEY_LEN = 12


def generate_ciphertext(flag: str):
    """Generate a ciphertext hex and return (cipher_hex, datetime_used)."""
    # Choose a random offset around now (± ~6 days)
    now = datetime.now(timezone.utc)
    offset = random.randint(-500000, 500000)  # seconds
    dt = now + timedelta(seconds=offset)

    # seed from timestamp (seconds)
    seed = int(dt.timestamp())

    # local RNG based on seed so the key is reproducible if seed is known
    rnd = random.Random(seed)

    # build key and encrypt
    key = [rnd.randint(0, 255) for _ in range(KEY_LEN)]
    flag_bytes = flag.encode("utf-8")
    cipher = bytes([b ^ key[i % KEY_LEN] for i, b in enumerate(flag_bytes)])
    return cipher.hex(), dt


def banner_text():
    return r"""

     /$$$$$$$$        /$$           /$$                       /$$$$$$$  /$$   /$$  /$$$$$$ 
|__  $$__/       |__/          | $$                      | $$__  $$| $$$ | $$ /$$__  $$
   | $$  /$$$$$$  /$$  /$$$$$$$| $$   /$$ /$$   /$$      | $$  \ $$| $$$$| $$| $$  \__/
   | $$ /$$__  $$| $$ /$$_____/| $$  /$$/| $$  | $$      | $$$$$$$/| $$ $$ $$| $$ /$$$$
   | $$| $$  \__/| $$| $$      | $$$$$$/ | $$  | $$      | $$__  $$| $$  $$$$| $$|_  $$
   | $$| $$      | $$| $$      | $$_  $$ | $$  | $$      | $$  \ $$| $$\  $$$| $$  \ $$
   | $$| $$      | $$|  $$$$$$$| $$ \  $$|  $$$$$$$      | $$  | $$| $$ \  $$|  $$$$$$/
   |__/|__/      |__/ \_______/|__/  \__/ \____  $$      |__/  |__/|__/  \__/ \______/ 
                                          /$$  | $$                                    
                                         |  $$$$$$/                                    
                                          \______/                                     
    """


def main():
    # ensure flag exists
    if not os.path.exists(FLAG_PATH):
        # Friendly message for players/platform — no secret leakage
        print("ERROR: flag not found. Ensure /flag.txt is mounted or FLAG env provided.")
        sys.exit(1)

    try:
        with open(FLAG_PATH, "r") as f:
            flag = f.read().strip()
    except Exception as e:
        print("ERROR: failed to read /flag.txt:", e)
        sys.exit(1)

    # generate ciphertext & timestamp
    cipher_hex, dt = generate_ciphertext(flag)

    # print only the allowed output
    print(banner_text())
    print("Tricky RNG — A cryptographic oddity in time and chance")
    print("------------------------------------------------------\n")
    print("Detective Aerys recovered a hex-encoded scrap from clockmaker Pawde's desk;")
    print("the ink trails look deliberate.\n")
    print(f"Recorded: [ {dt.strftime('%a %b %d %Y %H:%M:%S UTC+0000')} ]")
    print("Aerys left only one note for you: \"just a little exclusive notch.\"\n")
    print("Ciphertext (hex):")
    print(cipher_hex)
    print("\nGood luck, detective.")
    # exit cleanly
    sys.exit(0)


if __name__ == "__main__":
    main()
