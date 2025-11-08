#!/usr/bin/env python3
"""
challenge.py - RSA broadcast challenge (Pawde's Broadcast)

Fixed issues:
- imported missing modules (sys)
- read the flag as bytes instead of accidentally overwriting it with the path
- ensured msg is bytes before using bytes_to_long
- ensured ciphertext hex is output with fixed length matching modulus size
- added checks so m < N (otherwise encryption would be invalid)
- improved friendly error messages
- allowed FLAG to be supplied via environment variable for easier testing
"""
import os
import sys
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

KEY_BITS = 2048
E = 3
NUM_SHARES = 3
PAD_BYTES = 4
FLAG_PATH = "/flag.txt"

# allow overriding flag path with environment variable (useful for testing)
FLAG_PATH = os.environ.get("FLAG_PATH", FLAG_PATH)

if not os.path.exists(FLAG_PATH):
    # Friendly message for players/platform — no secret leakage
    print("ERROR: flag not found. Ensure /flag.txt is mounted or FLAG_PATH env provided.")
    sys.exit(1)

try:
    # read as bytes and strip trailing newline(s)
    with open(FLAG_PATH, "rb") as f:
        flag_bytes = f.read().rstrip(b"\r\n")
        if len(flag_bytes) == 0:
            raise ValueError("flag file is empty")
except Exception as e:
    print("ERROR: failed to read flag file:", e)
    sys.exit(1)

print("=" * 60)
print("""
 ██████╗  █████╗ ██╗    ██╗██████╗ ███████╗
 ██╔══██╗██╔══██╗██║    ██║██╔══██╗██╔════╝
 ██████╔╝███████║██║ █╗ ██║██║  ██║█████╗  
 ██╔═══╝ ██╔══██║██║███╗██║██║  ██║██╔══╝  
 ██║     ██║  ██║╚███╔███╔╝██████╔╝███████╗
 ╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═════╝ ╚══════╝
        Pawde's Broadcast Challenge
""")
print("=" * 60)

for i in range(NUM_SHARES):
    key = RSA.generate(KEY_BITS, e=E)

    pub_pem = key.publickey().export_key().decode()

    # Simple deterministic padding: append index bytes (big-endian)
    pad = i.to_bytes(PAD_BYTES, "big")
    msg = flag_bytes + pad

    m = bytes_to_long(msg)

    N = key.n
    # safety check: message must be less than modulus
    if m >= N:
        print(f"ERROR: message (flag + pad) is too large for modulus (share {i+1}).")
        print(f" modulus bit-length: {N.bit_length()}, message byte-length: {len(msg)}")
        sys.exit(1)

    c = pow(m, E, N)

    # ensure ciphertext hex has fixed length equal to modulus byte-length (big-endian)
    mod_len = (N.bit_length() + 7) // 8
    c_bytes = c.to_bytes(mod_len, "big")
    c_hex = c_bytes.hex()

    print(f"\n--- Public Key {i+1} ---")
    print(pub_pem)
    print(f"\n--- Ciphertext {i+1} (hex) ---")
    print(c_hex)
    print()

print("=" * 60)
print("Good Luck!!!")
print("=" * 60)
