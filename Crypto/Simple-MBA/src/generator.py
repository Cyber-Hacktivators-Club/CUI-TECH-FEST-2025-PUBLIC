#!/usr/bin/env python3
"""
generator.py

Create linear equations from an input flag where each equation contains
a small, fixed number of variables (by default 3-4 variables per equation).

Usage:
  python generator.py "CHC{g4mb4_s0lv3s_mb4}"
  python generator.py    # interactive prompt

Config at top:
  - COEFF_MIN/COEFF_MAX: coefficient range (small ints)
  - MIN_VARS_PER_EQ / MAX_VARS_PER_EQ: keep equations compact (3..4)
Notes:
  - Supports up to 26 characters (A..Z). If your flag is shorter than MIN_VARS_PER_EQ,
    MIN_VARS_PER_EQ will be reduced to the length of the flag to avoid impossible constraints.
"""

import sys
import random

# ------------------ Configuration ------------------
COEFF_MIN, COEFF_MAX = -3, 3   # small integer coefficients (non-zero)
MIN_VARS_PER_EQ = 3            # minimum variables per equation
MAX_VARS_PER_EQ = 4            # maximum variables per equation
MAX_VARS = 26                  # A..Z
# ---------------------------------------------------

def var_names(n):
    if n <= MAX_VARS:
        return [chr(ord('A') + i) for i in range(n)]
    raise ValueError("Too many characters; supports up to 26 variables.")

def nonzero_rand():
    c = 0
    while c == 0:
        c = random.randint(COEFF_MIN, COEFF_MAX)
    return c

def gen_compact_coeffs(n, min_vars=MIN_VARS_PER_EQ, max_vars=MAX_VARS_PER_EQ):
    """Generate an n x n coefficient matrix where each row has between min_vars..max_vars non-zero columns.
       Row 0 is forced to include column 0 (A) and at least one other column.
       For rows i>0, we try to prefer lower-triangular (include diag j==i) but still keep compact size.
    """
    # adjust min_vars if n is small
    min_vars = min(min_vars, n)
    max_vars = min(max_vars, n)
    mat = [[0]*n for _ in range(n)]

    # create each row
    for i in range(n):
        want = random.randint(min_vars, max_vars)

        if i == 0:
            # ensure row 0 contains A (col 0) and at least one more
            chosen = {0}
            # choose remaining columns from 1..n-1
            while len(chosen) < want:
                chosen.add(random.randint(1, n-1))
        else:
            # bias toward lower-triangular: include diagonal j==i
            chosen = {i}
            # choose remaining from 0..i (lower) with high prob, but allow some >i
            while len(chosen) < want:
                if random.random() < 0.8:
                    # pick from 0..i (lower-triangular bias)
                    j = random.randint(0, i)
                else:
                    # pick from entire range (introduce some upper indices)
                    j = random.randint(0, n-1)
                chosen.add(j)

        # assign non-zero coefficients
        for j in chosen:
            mat[i][j] = nonzero_rand()

    return mat

def ensure_column_coverage(mat, min_vars=MIN_VARS_PER_EQ, max_vars=MAX_VARS_PER_EQ):
    """Make sure every column (variable) appears at least once.
       If a column is unused, try to add it into a row that has < max_vars,
       otherwise replace a random column in a random row.
    """
    n = len(mat)
    # find unused columns
    unused = []
    for j in range(n):
        if not any(mat[i][j] != 0 for i in range(n)):
            unused.append(j)

    for col in unused:
        # try to find a row with space (< max_vars nonzero entries)
        target_row = None
        for i in range(n):
            cnt = sum(1 for x in mat[i] if x != 0)
            if cnt < max_vars:
                target_row = i
                break
        if target_row is None:
            # no row has space: pick a random row and replace a random non-zero column
            i = random.randrange(n)
            nonzero_cols = [idx for idx, val in enumerate(mat[i]) if val != 0]
            if nonzero_cols:
                to_replace = random.choice(nonzero_cols)
                mat[i][to_replace] = 0
                mat[i][col] = nonzero_rand()
            else:
                # row was unexpectedly all-zero; just assign diagonal
                mat[i][col] = nonzero_rand()
        else:
            mat[target_row][col] = nonzero_rand()

    return mat

def format_equation(coeffs_row, vars_letters, rhs):
    terms = []
    for c, v in zip(coeffs_row, vars_letters):
        if c != 0:
            terms.append(f"({c}*{v})")
    lhs = " + ".join(terms) if terms else "0"
    return f"{lhs} == {rhs}"

def main():
    # input
    if len(sys.argv) >= 2:
        flag = sys.argv[1]
    else:
        try:
            flag = input("Enter flag string (e.g. CHC{abcd}): ").strip()
        except EOFError:
            print("No input provided. Exiting.")
            return

    if not flag:
        print("Empty flag. Exiting.")
        return

    n = len(flag)
    if n > MAX_VARS:
        print(f"Flag too long ({n}). Max supported is {MAX_VARS}.")
        return

    # if flag is small, shrink MIN_VARS_PER_EQ to not exceed n
    min_vars = min(MIN_VARS_PER_EQ, n)
    max_vars = min(MAX_VARS_PER_EQ, n)

    vars_letters = var_names(n)
    ascii_vals = [ord(ch) for ch in flag]

    # optional deterministic seed for repeatability
    # random.seed(0)

    coeffs = gen_compact_coeffs(n, min_vars=min_vars, max_vars=max_vars)
    coeffs = ensure_column_coverage(coeffs, min_vars=min_vars, max_vars=max_vars)

    # compute RHS values
    rhs_list = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += coeffs[i][j] * ascii_vals[j]
        rhs_list.append(s)

    # Output equations
    print("\n=== Linear equations (each eq has {}..{} variables) ===\n".format(min_vars, max_vars))
    for i, (row, rhs) in enumerate(zip(coeffs, rhs_list), start=1):
        eq = format_equation(row, vars_letters, rhs)
        print(f"E{i}: {eq}")

    # Print mapping for author
    print("\n=== Variable mapping (secret) ===\n")
    for v, ch in zip(vars_letters, flag):
        print(f"{v} = '{ch}' (ASCII {ord(ch)})")

    print("\nNotes:")
    print(f"- Each equation contains between {min_vars} and {max_vars} variables (inclusive).")
    print("- E1 includes A and at least one other variable, so A is not isolated.")
    print("- Coefficients chosen from range {}..{}.".format(COEFF_MIN, COEFF_MAX))
    print("- Every variable appears in at least one equation.")

if __name__ == "__main__":
    main()
