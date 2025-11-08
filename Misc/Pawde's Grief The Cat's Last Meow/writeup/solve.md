# Solve - Pawde's Grief: The Cat's Last Meow

## Step 1: Analyze the MKV files

First, check what's inside both MKV files:

```bash
mkvmerge -i sewy_with_subs.mkv
mkvmerge -i SUIIIIII_with_subs.mkv
```

Look for attachments in the output. You'll notice `SUIIIIII.mkv` has an attachment named `subs_bhi_h.srt`.

## Step 2: Extract the attachment

Extract all attachments from `SUIIIIII.mkv`:

```bash
mkvextract SUIIIIII_with_subs.mkv attachments 1 2 3
```

Or extract specific attachment by ID (check the ID from the `-i` output):

```bash
mkvextract SUIIIIII_with_subs.mkv attachments 3:subs_bhi_h.srt
```

## Step 3: Convert hex to PNG

The `subs_bhi_h.srt` file contains hexadecimal data of an image. Convert it back to a PNG:

```bash
xxd -r -p subs_bhi_h.srt screaming_recovered.png
```

## Step 4: Extract hidden data with OpenStego

Use OpenStego to extract the embedded file from the PNG:

```bash
openstego extract -sf screaming_recovered.png -xf output/
```

Or with GUI, open OpenStego and:

* Select "Extract Data"
* Choose `screaming_recovered.png` as the input
* Extract to get the hidden `.smeow` file

## Step 5: Decompile the Meowlang code

You'll find a `.smeow` file (Meowlang source code). Decompile it using python:

```bash
# If you have a Meowlang decompiler
python3 decompile screaming.smeow
```

Or manually analyze the Meowlang code to extract the flag.

## Step 6: Get the flag

After decompiling the `.smeow` file, you'll find the flag hidden in the code!

```
CHC{...}
```

---

## Summary

1. Check MKV attachments → Find `subs_bhi_h.srt` in `SUIIIIII.mkv`
2. Extract attachment from MKV
3. Convert hex data to PNG image
4. Use OpenStego to extract hidden `.smeow` file
5. Decompile Meowlang code to reveal the flag

**Tools needed:**

* `mkvmerge` / `mkvextract` (MKVToolNix)
* `xxd` (hex converter)
* OpenStego
* Meowlang decompiler

---
