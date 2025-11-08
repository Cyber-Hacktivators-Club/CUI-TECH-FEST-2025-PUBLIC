#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long, getPrime
import random

def gen_challenge(flag: str, n_steps=6, extra_bits=32):
    Q0 = bytes_to_long(flag.encode())    
    # Pick modulus M larger than Q0
    M_bits = Q0.bit_length() + extra_bits
    M = getPrime(M_bits)
    A = random.randint(2, M-2)
    B = random.randint(2, M-2)
    C = random.randint(2, M-2)
    Q = [Q0]
    for i in range(1, n_steps+1):
        Q.append((A * Q[-1]**2 + B * Q[-1] + C) % M)

    with open("challenge.txt", "w") as f:
        f.write(f"M = {M}\nA = {A}\nB = {B}\nC = {C}\n")
        f.write(f"Q3 = {Q[3]}\nQ4 = {Q[4]}\nQ5 = {Q[5]}\n")
    print("Challenge written to challenge.txt")

if __name__ == "__main__":
    gen_challenge("CHC{test_flag_for_faking_lol}")
