#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long, getPrime
import random
import re
import os

def read_flag(file_path="/flag.txt"):
    """Reads the flag from /flag.txt"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Flag file not found at {file_path}")
    with open(file_path, "r") as f:
        flag = f.read().strip()
    return flag

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

def read_challenge(file_path="challenge.txt"):
    """Reads challenge.txt and returns a dictionary of values."""
    with open(file_path, "r") as f:
        data = f.read()

    # Extract values using regex
    values = dict(re.findall(r"(\w+)\s*=\s*(\d+)", data))
    
    # Convert string numbers to integers
    for k in values:
        values[k] = int(values[k])
    
    return values

if __name__ == "__main__":
    # Read the flag from /flag.txt
    flag = read_flag()

    # Generate the challenge
    gen_challenge(flag)

    # Example of reading the challenge back
    challenge_data = read_challenge()
    print("\nRead from challenge.txt:")
    for key, val in challenge_data.items():
        print(f"{key} = {val}")
