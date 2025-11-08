
# Solve

To solve the challenge, analyze the provided **MFT** file using **mftecmd** by Eric Zimmerman (EZ Tools).

---

### Step 1: Analyze the MFT

Run the following command to list file records:

```bash
mftecmd -f $MFT --csv .
```

Look through the output and find a file under the **Documents** directory named `update.ps1`.

---

### Step 2: Extract the Script

Use `mftecmd` (or any suitable method like hex editor) to extract the resident data or view the contents of  `levi\Documents\update.ps1`.

---

### Step 3: Decode the Base64

Inside `update.ps1`, you’ll find a long Base64 string. Decode it using PowerShell or a base64 utility or use cyberchef:

**Linux / macOS:**

```bash
echo '<BASE64_STRING>' | base64 -d
```

**Windows PowerShell:**

```powershell
$b = '<BASE64_STRING>'
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($b))
```

---

### Step 4: Get the Flag

The decoded text will reveal the  **flag** , usually in the format:

```
CHC{something_here}
```

---

✅ **Summary:**

Use `mftecmd` → find `Documents\update.ps1` → extract Base64 → decode → read the flag.
