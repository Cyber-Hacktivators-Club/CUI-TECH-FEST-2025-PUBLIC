#!/usr/bin/env sage
"""
solve.sage - Pawde's Broadcast solver (Franklin-Reiter attack)
"""
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long

# Paste the public keys here (PEM format)
PUBLIC_KEYS = [
"""-----BEGIN PUBLIC KEY-----
Paste pub1 here
-----END PUBLIC KEY-----""",

"""-----BEGIN PUBLIC KEY-----
Paste pub2 here
-----END PUBLIC KEY-----""",

"""-----BEGIN PUBLIC KEY-----
Paste pub3 here
-----END PUBLIC KEY-----"""
]

# Paste the ciphertexts here (hex format)
CIPHERTEXTS_HEX = [
    "paste_c1_hex_here",
    "paste_c2_hex_here",
    "paste_c3_hex_here"
]

def parse_public_key(pem_str):
    """Parse PEM string to get n and e"""
    key = RSA.import_key(pem_str.strip())
    return key.n, key.e

def polynomial_gcd(g1, g2):
    """Euclidean algorithm for polynomial GCD"""
    while g2:
        g1, g2 = g2, g1 % g2
    return g1.monic()

def franklin_reiter(n, e, c1, c2):
    """Franklin-Reiter attack when m2 = m1 + diff"""
    P.<x> = PolynomialRing(Zmod(n))
    
    for diff in [1, -1, 256, -256, 65536, -65536, 16777216, -16777216]:
        g1 = x^e - c1
        g2 = (x + diff)^e - c2
        result = polynomial_gcd(g1, g2)
        
        if result.degree() == 1:
            coeffs = result.list()
            if len(coeffs) >= 2 and coeffs[1] != 0:
                root = -coeffs[0] / coeffs[1]
                m = int(root)
                if pow(m, e, n) == c1:
                    plaintext = long_to_bytes(m)
                    if b"CHC{" in plaintext:
                        return plaintext
    return None

def solve_challenge():
    print("="*60)
    print("Solving Pawde's Broadcast Challenge...")
    print("="*60)
    
    # Parse keys and ciphertexts
    moduli = []
    ciphertexts = []
    e = None
    
    for i, pem in enumerate(PUBLIC_KEYS):
        n, exp = parse_public_key(pem)
        c = bytes_to_long(bytes.fromhex(CIPHERTEXTS_HEX[i]))
        moduli.append(n)
        ciphertexts.append(c)
        if e is None:
            e = exp
        print(f"[+] Loaded key {i+1}")
    
    print(f"\n[*] Exponent e = {e}")
    print(f"[*] Running Franklin-Reiter attack...\n")
    
    # Try Franklin-Reiter on each pair
    for i in range(len(ciphertexts)-1):
        print(f"[*] Trying pair ({i+1}, {i+2})...")
        result = franklin_reiter(moduli[i], e, ciphertexts[i], ciphertexts[i+1])
        if result:
            print(f"\n{'='*60}")
            print(f"[+] FLAG FOUND: {result.decode()}")
            print(f"{'='*60}")
            return result
    
    print("\n[!] Attack failed")
    return None

if __name__ == "__main__":
    solve_challenge()