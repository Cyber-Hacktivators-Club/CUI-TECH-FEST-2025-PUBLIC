# Pawde's Resume Challenge - Solution [Inspired by RomCom]

## Solution Steps

### Step 1: Analyze the RAR File for ADS

Run `strings` on the RAR file to find the Alternate Data Stream reference:

```bash
strings resume.rar | grep -i "startup"
# or
strings resume.rar | grep ".bat"
```

**Finding:** You'll discover a reference to a batch file path in the startup directory with an ADS marker.

---

### Step 2: Locate the Obfuscated Batch File

In the KAPE output, navigate to the startup folder and find the dropped batch file:

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
```

---

### Step 3: Deobfuscate the Batch File

The batch file uses BatchCrypt obfuscation. Use the given deobfuscator.py on the Startup.bat

Run it:

```bash
python deobfuscate.py payload.bat
```

---

### Step 4: Extract the Hex String

In the deobfuscated file, find the hex-encoded variable:

```batch
set "p1=64 64 63 75 57 76 36 62 61 36 59 65 56 49 67 51 52 57 50 47 70 31 64 52 79 5a 48 5a"
```

Decode the hex:

```python
hex_data = "64 64 63 75 57 76 36 62 61 36 59 65 56 49 67 51 52 57 50 47 70 31 64 52 79 5a 48 5a"
decoded = bytes.fromhex(hex_data.replace(' ', '')).decode('ascii')
print(decoded)
# Output: ddcuWv6ba6YeVIgQ4W2Gp1d4yZHZ
```

---

### Step 5: Decode Base62

The hex output is Base62-encoded. Decode it to get the flag or just do cyberchef hhh:

```python
def base62_decode(encoded):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    num = 0
    for char in encoded:
        num = num * 62 + alphabet.index(char)
    hex_str = hex(num)[2:]
    if len(hex_str) % 2:
        hex_str = '0' + hex_str
    return bytes.fromhex(hex_str).decode('ascii')

flag = base62_decode("ddcuWv6ba6YeVIgQ4W2Gp1d4yZHZ")
print(f"Flag: {flag}")
```

---

## Tools Used

- `strings` - Find ADS references in RAR
- Python 3 - Deobfuscation and decoding
- CyberChef (optional) - For hex/base62 decoding
