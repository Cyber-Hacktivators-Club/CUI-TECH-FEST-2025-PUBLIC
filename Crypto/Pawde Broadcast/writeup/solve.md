
# Pawde Broadcast - Solution

## Challenge Overview

We're given 3 RSA public keys and 3 ciphertexts. The same message (with slight padding differences) is encrypted using the same small exponent `e=3` across different moduli.

## Vulnerability

**RSA Broadcast Attack with Related Messages (Franklin-Reiter Attack)**

The challenge encrypts related messages:

- `m1 = FLAG + pad1`
- `m2 = FLAG + pad2`
- `m3 = FLAG + pad3`

Where the padding is just sequential bytes (`0x00000000`, `0x00000001`, `0x00000008`).

Since the messages differ by a small known value and use the same exponent `e=3`, we can use the **Franklin-Reiter Related Message Attack**.

## Attack Method

The Franklin-Reiter attack works when:

1. Two messages `m1` and `m2` are related by `m2 = m1 + diff` for some known `diff`
2. Both are encrypted with the same exponent `e` (but different moduli)
3. We have both ciphertexts `c1` and `c2`

### Mathematical Basis

Given:

- `c1 ≡ m1^e (mod n1)`
- `c2 ≡ (m1 + diff)^e (mod n2)`

We construct two polynomials over `Zmod(n1)`:

- `g1(x) = x^e - c1`
- `g2(x) = (x + diff)^e - c2`

Both polynomials share the root `m1`, so their GCD will be `(x - m1)`. We can extract `m1` from this linear factor.

## Solution Steps

1. **Parse the public keys** to extract moduli and exponent
2. **Convert hex ciphertexts** to integers
3. **Try Franklin-Reiter attack** on consecutive pairs with different padding differences
4. **Extract the plaintext** from the polynomial GCD
5. **Verify and decode** the flag

## Running the Solution

```bash
sage solve.sage
```

The script tries multiple padding differences:

- `[1, -1, 256, -256, 65536, -65536, 16777216, -16777216]`

These correspond to different byte-level padding values.

## Flag

```
CHC{P@wd3_R3it3r_n33ds_l@tt1c3s}
```

## Key Takeaway

Never encrypt related messages with the same low exponent, even with different RSA keys. The Franklin-Reiter attack can recover plaintexts when messages differ by small known values.
