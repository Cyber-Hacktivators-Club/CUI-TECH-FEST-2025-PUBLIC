# 🐾 **Solve — Toaster**

### Challenge Summary

You’re given a compiled Rust binary (`Toaster.exe`).

It asks for a flag and always says *Access denied* unless you type the exact one.

`strings` won’t help — the flag is stored XOR-encoded and only decoded briefly in memory right before the comparison.

---

## 🧠 **Goal**

Recover the flag from memory when it’s decoded, before the comparison.

---

## ⚙️ **Steps**

* **Open the binary in your debugger** (x64dbg, WinDbg, IDA, Cutter, Ghidra + debugger or my favorite binja).
* **Run the program** until it prompts for input and type any string (you don't need the correct flag).
* **Locate the comparison instruction.**

  After the input is read, the program compares your input to an in-memory value. In the disassembly this will appear as a `cmp` instruction (or a call to a small compare routine that contains `cmp` instructions), or as a `memcmp`/`strcmp`-style sequence. Find that `cmp` (or the instruction immediately before it).
* **Set a breakpoint just before the `cmp` executes.**

  The breakpoint must fire **after** the program has decoded/loaded the flag into memory but **before** the compare runs.
* **Run to the breakpoint.**

  When the breakpoint hits, the decoded flag will be in memory (usually on the stack / local buffer).
* **Dump memory around the stack/local buffer.**

  Inspect stack memory near the stack pointer or the local buffer address. The flag appears as an ASCII string.

  * Examples:
    * **x64dbg / x32dbg** : use the Dump window; follow the stack pointer (ESP/RSP) or follow the address of the local buffer, then look for a readable ASCII string.
    * **WinDbg** : `db rsp L80` (or `db esp L80`) to dump bytes; or `db <address> L80`.
    * **Ghidra/IDA** (with debugger): open the memory view / stack frame and dump memory at the buffer address.
    * **Cutter** : run to breakpoint and use the «Memory» view to inspect the stack.
* **Read / copy the ASCII string you find — that is the flag.**
* **Challenge complete.**

  ---
