#!/usr/bin/env python3
"""
1. Invert the recurrence:
   Each step of the quadratic sequence 
       Q_{n+1} = (A * Q_n^2 + B * Q_n + C) % M
   is treated as a modular quadratic equation. 
   Solve it to get all possible Q_n preimages.

2. Backtrack through steps:
   Start from the highest known Q_k (e.g., Q5) 
   and iteratively compute all candidate preimages down to Q0.

3. Forward-check candidates:
   For each candidate Q0, regenerate the sequence and 
   keep the one(s) that match all provided Qi values.
   The correct Q0 corresponds to the original flag.
"""

from Crypto.Util.number import inverse, long_to_bytes
import sympy as sp
import sys

def mod_sqrt(a, p):
    """Return list of modular square roots of a mod p (empty list if none)."""
    roots = sp.sqrt_mod(a, p)
    if roots is None:
        return []
    if isinstance(roots, int):
        return [roots]
    return list(roots)

def invert_step(q_next, A, B, C, M):
    """Return all possible q such that f(q) = q_next mod M, where
       f(q) = (A*q^2 + B*q + C) % M."""
    D = (B*B - 4*A*(C - q_next)) % M
    sqrtD = mod_sqrt(D, M)
    if not sqrtD:
        return []
    inv2A = inverse((2 * A) % M, M)
    res = set()
    for s in sqrtD:
        q1 = ((-B + s) * inv2A) % M
        q2 = ((-B - s) * inv2A) % M
        res.add(q1)
        res.add(q2)
    return list(res)

def parse_challenge(filename):
    A = B = C = M = None
    Qs = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = [s.strip() for s in line.split("=", 1)]
                if k == "M":
                    M = int(v)
                elif k == "A":
                    A = int(v)
                elif k == "B":
                    B = int(v)
                elif k == "C":
                    C = int(v)
                elif k.startswith("Q"):
                    # parse index Q3, Q4, etc.
                    idx = int(k[1:])
                    Qs[idx] = int(v)
    return M, A, B, C, Qs

def forward_check(q0, A, B, C, M, Qs):
    """Check that starting from q0 the forward sequence matches all given Qs."""
    # produce sequence up to max index in Qs
    seq = {0: q0}
    max_idx = max(Qs.keys())
    q = q0
    for i in range(1, max_idx + 1):
        q = (A * q * q + B * q + C) % M
        seq[i] = q
    # verify all provided Qs
    for idx, target in Qs.items():
        if seq.get(idx, None) != target:
            return False
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solver_fixed.py challenge.txt")
        sys.exit(1)
    fn = sys.argv[1]
    M, A, B, C, Qs = parse_challenge(fn)
    if None in (M, A, B, C) or not Qs:
        print("Couldn't parse challenge file; need M,A,B,C and at least one Qi.")
        sys.exit(2)

    max_idx = max(Qs.keys())
    print("Parsed Q indices:", sorted(Qs.keys()))
    print("Will invert from Q{} back to Q0 ({} steps).".format(max_idx, max_idx))

    # start from Q_max
    start = Qs[max_idx]
    paths = {start}  # set of current candidates
    # invert step-by-step down to index 0
    for step in range(max_idx, 0, -1):
        new_candidates = set()
        for q_next in paths:
            preimages = invert_step(q_next, A, B, C, M)
            for p in preimages:
                new_candidates.add(p)
        paths = new_candidates
        print(f"After inverting to index {step-1}: candidates = {len(paths)}")
        if not paths:
            print("No candidates found during inversion; aborting.")
            sys.exit(3)

    # paths now contains candidates for Q0
    print("Total Q0 candidates:", len(paths))
    solutions = []
    for q0 in paths:
        if forward_check(q0, A, B, C, M, Qs):
            solutions.append(q0)

    if not solutions:
        print("No valid Q0 found that reproduces all provided Qi.")
        sys.exit(4)

    # print solutions (likely one)
    for q0 in solutions:
        try:
            flag_bytes = long_to_bytes(q0)
            print("[+] Recovered Q0 =", q0)
            print("[+] FLAG (bytes) =", flag_bytes)
            # attempt to decode printable ascii if possible
            try:
                print("[+] FLAG (decoded) =", flag_bytes.decode(errors='replace'))
            except:
                pass
        except Exception:
            print("[+] Recovered Q0 (int):", q0)

if __name__ == "__main__":
    main()
