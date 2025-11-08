# **Pawde’s Encrypted Drop**

**Goal:** From `challenge.pcapng` recover the uploaded file and read the flag.

---

## Quick summary (one line)

Open the capture → extract NTLM Type-2 (challenge) + Type-3 (response) fields → build Net-NTLMv2 hash → crack password (or NTLMv2 hash) → Use it as NT password → export the file → read the flag.

---

## Steps (clean, actionable)

### 1. Open the capture

Load `challenge.pcapng` in **Wireshark** (or `tshark`).

### 2. Confirm you have what you need

* Verify there are **SMB2/3** packets and later packets have `Encrypted` set.
* Verify you have both **NTLMSSP CHALLENGE (Type-2)** and **NTLMSSP AUTH (Type-3)** frames in the capture.

### 3. Pull required fields from the packets

* From  **Type-2 (Challenge)** : copy the **Server Challenge** (8 bytes, hex).
* From  **Type-3 (Auth / Response)** : copy:
  * **User name** (exact casing from the packet)
  * **Domain name** (Domain name from the packet)
  * **NTProofStr** (first 16 bytes of the NTLMv2 response)
  * **Client blob** (the remainder of the NTLMv2 response blob; starts with `01010000...`)

### 4. Build the Net-NTLMv2 cracking line

Use the hashcat/John format. Fields are colon-separated:

```
USER::DOMAIN_NAME:SERVER_CHALLENGE:NTProofStr:Rest_of_the_response_blob...
```

Save that single line to `netntlm.hash`.

### 5. Crack the Net-NTLMv2 hash

Use a cracker configured for Net-NTLMv2:

* **Hashcat** (mode `5600`):

```bash
hashcat -m 5600 netntlm.hash rockyou.txt
```

### 6. Use the NT Password

Open the preferences in the wireshark, Go to protocols and then look NTLMSSP tab and you will have an empty field there named NT password, Enter the password that you cracked using NTLMv2 hash.

### 7. Export/reconstruct the file

* From the decrypted SMB stream, reconstruct the transferred file:
  * In Wireshark (after decryption) use **File → Export Objects → SMB** (or extract the file from decrypted READ/WRITE frames), **or**
  * Reassemble the SMB file payload bytes and save to disk.

### 8. Read the flag

Open the recovered file — the flag is plain text inside.

---
