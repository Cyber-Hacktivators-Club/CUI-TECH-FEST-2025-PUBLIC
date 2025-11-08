# Solve.md

---

## 1) Find which process opened the `.docm`

List process command lines and identify the Word process that references `*.docm`.

Example (Volatility 3):

```
vol3 -f memory.dmp windows.cmdline
```

(look for `Libre.EXE/Office.exe` / `<name>.docm`). ([volatility3.readthedocs.io](https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.cmdline.html?utm_source=chatgpt.com "volatility3.plugins.windows.cmdline module - Read the Docs"))

---

## 2) Locate the `.docm` file object in memory

Scan memory for file objects and note the physical/virtual address shown for the `.docm`.

```
vol3 -f memory.dmp windows.filescan
```

Then feed that offset to `dumpfiles` to extract the `.docm`. ([volatility3.readthedocs.io](https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.filescan.html?utm_source=chatgpt.com "volatility3.plugins.windows.filescan module"))

---

## 3) Extract the macro from the `.docm`

Open the extracted `.docm` with `olevba` / another Office macro parser and inspect the macro.

You will see the macro opens `flag.txt` via an environment variable, reads/dumps it, derives a key from envvars and runs a decryption routine.

---

## 4) Dump `flag.txt` from memory

Using the same technique as step 2, locate the `flag.txt` file handle/object (or a file cache entry) and use `dumpfiles` to extract it:

```
vol3 -f memory.dmp -o ./extracted windows.dumpfiles --physaddr 0xOFFSET
```

(Replace `0xOFFSET` with the address you found; `-o` specifies output directory). ([volatility3.readthedocs.io](https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.dumpfiles.html?utm_source=chatgpt.com "volatility3.plugins.windows.dumpfiles module"))

---

## 5) Recover the environment variable (the key)

List the environment variables for the Word process and find the variable the macro referenced:

```
vol3 -f memory.dmp windows.envars --pid <PID> 
```

Take the value (this is the key used by the macro). ([volatility3.readthedocs.io](https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.envars.html?utm_source=chatgpt.com "volatility3.plugins.windows.envars module"))

---

## 6) Reproduce the macro’s decryption locally

Copy the macro’s decryption steps exactly (order/operations matter). Apply them to the dumped `flag.txt` using the recovered key — e.g., the macro is doing simple XOR with the env key → output plaintext. Run the same steps locally and read the result: that is the flag.

---

## Final note (one line)

Process `<procname>` (PID `<PID>`) opened `document.docm` → macro referenced env var `<NAME>` → `flag.txt` was dumped from memory → key recovered from envars → apply macro decryption → flag = `CHC{...}`.
