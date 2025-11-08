#!/usr/bin/env python3
# run_and_decode_smeow.py
# Minimal runner + decoder for the simplified .smeow programs above.
# It implements tiny semantics for the opcodes we used:
# 2 N -> PUSH N (onto a simple stack)
# 1   -> MEOW: print (simulate) stack[-1] cat emojis to current line
# 0   -> RET: finish current line (newline)
#
# After running, each non-empty output line contains a run of cat emojis whose
# length is the ASCII code of one character. We decode by counting length -> chr.

import sys

CAT = "🐱"

def run_smeow_file(path):
    # load numbers
    with open(path, "r", encoding="utf-8") as f:
        nums = [int(line.strip()) for line in f if line.strip() != ""]

    ip = 0
    stack = []
    lines = []    # list of output lines (strings)
    current = ""  # building current line

    while ip < len(nums):
        opcode = nums[ip]
        if opcode == 2:   # PUSH: next number is N
            if ip+1 >= len(nums):
                raise SystemExit("Malformed: PUSH without operand")
            n = nums[ip+1]
            stack.append(n)
            ip += 2
        elif opcode == 1: # MEOW: print stack[-1] cats to current line
            if not stack:
                raise SystemExit("Runtime error: MEOW with empty stack")
            t = stack[-1]
            current += CAT * t
            ip += 1
        elif opcode == 0: # RET: newline
            lines.append(current)
            current = ""
            ip += 1
        else:
            # We didn't use other opcodes; treat as NOP
            ip += 1

    # if something left in current, flush
    if current:
        lines.append(current)

    return lines

def decode_lines_to_text(lines):
    chars = []
    for line in lines:
        # count cats (non-empty lines usually)
        if not line:
            # preserve newlines (or ignore)
            continue
        count = line.count(CAT)
        try:
            chars.append(chr(count))
        except Exception:
            chars.append('?')
    return "".join(chars)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_and_decode_smeow.py <file.smeow>")
        sys.exit(1)
    path = sys.argv[1]
    lines = run_smeow_file(path)
    decoded = decode_lines_to_text(lines)
    print(decoded)
