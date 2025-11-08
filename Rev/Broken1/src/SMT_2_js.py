#!/usr/bin/env python3
import sys
import random
from textwrap import dedent

PRINTABLE = [i for i in range(0x20, 0x7f)]
L = 32

def rol8(x, n):
    n &= 7
    return ((x << n) | (x >> (8 - n))) & 0xFF

def make_constraints(secret_bytes):
    rng = random.Random(0xBEEF)
    ops = []
    L = 32

    # Step 1: ensure each byte appears at least once
    for i in range(L):
        a = i
        b = rng.randrange(L)
        if b == a:
            b = (b + 1) % L
        val = (secret_bytes[a] ^ secret_bytes[b]) & 0xFF
        ops.append(dict(type="xor", a=a, b=b, val=val))

    # Step 2: add extra random mixed constraints
    for _ in range(20):
        a, b, c = rng.randrange(L), rng.randrange(L), rng.randrange(L)
        while len({a,b,c}) < 2:
            a, b, c = rng.randrange(L), rng.randrange(L), rng.randrange(L)
        r = rng.randrange(1, 7)
        m = rng.choice([2,3,5,7,11])
        k = rng.randrange(1, 50)
        t = rng.choice(["sum", "mul", "rolxor", "mix"])

        if t == "sum":
            val = (secret_bytes[a] + secret_bytes[b] + k) & 0xFF
            ops.append(dict(type="sum", a=a, b=b, k=k, val=val))
        elif t == "mul":
            val = ((secret_bytes[a] * m) + secret_bytes[b]) & 0xFF
            ops.append(dict(type="mul", a=a, b=b, m=m, val=val))
        elif t == "rolxor":
            val = (rol8(secret_bytes[a], r) ^ secret_bytes[b]) & 0xFF
            ops.append(dict(type="rolxor", a=a, b=b, r=r, val=val))
        elif t == "mix":
            val = (rol8(secret_bytes[a], r) + (secret_bytes[b] ^ secret_bytes[c])) & 0xFF
            ops.append(dict(type="mix", a=a, b=b, c=c, r=r, val=val))
    return ops

def emit_js(secret_inner, ops, filenameA):
    js = dedent(f"""\
    'use strict';

    const v8 = require('v8');
    const readline = require('readline');

    function rol8(x, n) {{
      n &= 7;
      return (((x << n) | (x >>> (8 - n))) & 0xFF) >>> 0;
    }}

    function check(flag) {{
      if (!flag.startsWith("CHC{{") || !flag.endsWith("}}")) {{
        console.log("Bad format");
        return false;
      }}
      const inner = flag.slice(4, -1);
      if (inner.length !== 32) {{
        console.log("Flag must have 32 characters inside braces.");
        return false;
      }}
      const bytes = Array.from(Buffer.from(inner));

      
      let ok = true;
    """)

    for op in ops:
        t = op["type"]
        if t == "xor":
            expr = f"((bytes[{op['a']}] ^ bytes[{op['b']}]) & 0xFF)"
        elif t == "sum":
            expr = f"((bytes[{op['a']}] + bytes[{op['b']}] + {op['k']}) & 0xFF)"
        elif t == "mul":
            expr = f"(((bytes[{op['a']}] * {op['m']}) + bytes[{op['b']}]) & 0xFF)"
        elif t == "rolxor":
            expr = f"((rol8(bytes[{op['a']}], {op['r']}) ^ bytes[{op['b']}]) & 0xFF)"
        elif t == "mix":
            expr = f"((rol8(bytes[{op['a']}], {op['r']}) + (bytes[{op['b']}] ^ bytes[{op['c']}])) & 0xFF)"
        else:
            continue
        js += f"  ok = ok && (({expr}) === 0x{op['val']:02x});\n"

    js += dedent("""\
      if (ok)
        console.log("✅ Correct! Flag accepted.");
      else
        console.log("❌ Wrong flag.");
      return ok;
    }
    function main(){
        const arg = process.argv[2];
        if (arg) check(arg.trim());
        else {
          const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
          rl.question("Enter flag: ", (f) => { check(f.trim()); rl.close(); });
        }
    }
                 
    if (v8.startupSnapshot && v8.startupSnapshot.isBuildingSnapshot()) {
        v8.startupSnapshot.setDeserializeMainFunction(main);
    } else {
        main();
    }
    """)

    with open(filenameA, "w", encoding="utf8") as f:
        f.write(js)
    print(f"✅ {filenameA} written.")

def emit_solver(ops):
    solver_py = dedent("""\
    # solver.py -- Z3 solver for challenge.js (Generated)
    # Requires: pip install z3-solver
    from z3 import Solver, BitVec, BitVecVal, RotateLeft, And, sat

    s = Solver()
    bytes = [BitVec(f'b{i}', 8) for i in range(32)]

    # printable constraint: 0x20 .. 0x7e
    for b in bytes:
        s.add(And(b >= BitVecVal(0x20, 8), b <= BitVecVal(0x7e, 8)))
    """)

    # append each constraint in structured form
    for op in ops:
        t = op["type"]
        a = f"bytes[{op['a']}]"
        if t == "xor":
            z = f"({a} ^ {f'bytes[{op['b']}]'})"
            solver_py += f"s.add(({z}) == BitVecVal({op['val']}, 8))\n"
        elif t == "sum":
            z = f"(({a} + bytes[{op['b']}] + BitVecVal({op['k']}, 8)) )"
            # mask is automatic for 8-bit bitvec arithmetic
            solver_py += f"s.add(({z}) == BitVecVal({op['val']}, 8))\n"
        elif t == "mul":
            z = f"(({a} * BitVecVal({op['m']}, 8) + bytes[{op['b']}]) )"
            solver_py += f"s.add(({z}) == BitVecVal({op['val']}, 8))\n"
        elif t == "rolxor":
            # rotate left then xor
            solver_py += f"s.add((RotateLeft({a}, {op['r']}) ^ bytes[{op['b']}]) == BitVecVal({op['val']}, 8))\n"
        elif t == "mix":
            solver_py += f"s.add((RotateLeft({a}, {op['r']}) + (bytes[{op['b']}] ^ bytes[{op['c']}])) == BitVecVal({op['val']}, 8))\n"

    solver_py += dedent("""
    if s.check() == sat:
        m = s.model()
        inner = ''.join(chr(m[b].as_long()) for b in bytes)
        print("Recovered inner:", inner)
        print("Flag: CHC{" + inner + "}")
    else:
        print("Unsat!")
    """)

    with open("solver.py", "w", encoding="utf8") as f:
        f.write(solver_py)
    print("✅ solver.py written.")

def main():
    if len(sys.argv) > 1:
        secret_inner = sys.argv[1]
        
        if len(secret_inner) != 32:
            print("Secret inner must be exactly 32 chars.")
            sys.exit(1)
    else:
        secret_inner = ''.join(chr(random.choice(PRINTABLE)) for _ in range(32))
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    else:
        filename = "challenge_default.js"

    secret_bytes = list(secret_inner.encode('latin1'))  # ensure 0-255 bytes
    ops = make_constraints(secret_bytes)
    emit_js(secret_inner, ops, filename)
    if not (filename == "challenge_default.js"):
        emit_solver(ops)
    print(f"\n🔐 Secret inner: {secret_inner}")
    print("Run: node challenge.js 'CHC{...}'   or   python solver.py")

if __name__ == "__main__":
    main()