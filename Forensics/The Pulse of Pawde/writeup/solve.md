# 🧩 ICMP AES Challenge — Writeup

## 📘 Overview

This challenge hides an AES-encrypted message inside ICMP traffic of a PCAP file.

The encryption **key** and **IV** are stored inside the PCAP’s **capture comment**.

To solve it, you must decode the binary data from packet timings and decrypt it.

---

## 🕵️ Step-by-Step Solution

### **1. Extract the ICMP Timing Pattern**

The challenge uses ICMP echo **requests and replies** to encode bits based on timing differences:

* Short delay between request and reply → represents a **0**
* Long delay between request and reply → represents a **1**

By analyzing each ICMP request/reply pair and measuring the delay, you can reconstruct the binary stream that encodes the hidden data.

---

### **2. Convert the Binary Stream to Text**

Once all bits are extracted from the timing pattern, group them into 8-bit segments and convert them into ASCII characters.

This reveals a long string of hexadecimal characters — the AES-encrypted ciphertext.

---

### **3. Retrieve the AES Key and IV**

The PCAP file’s **capture comment** (visible via tools like `capinfos` or Wireshark) contains two 16-character hexadecimal strings:

* The first 16 hex characters → **AES Key**
* The second 16 hex characters → **AES IV**

Both values are in hexadecimal format and correspond to a 128-bit AES key and a 128-bit initialization vector.

---

### **4. Decrypt the Data**

Use **AES-128-CBC** decryption with the extracted key and IV on the decoded ciphertext.

After decryption, remove the PKCS#7 padding to reveal the final plaintext message — the **flag**.

---

## 🧩 Summary

| Step | Description                                              |

| ---- | -------------------------------------------------------- |

| 1️⃣  | Measure ICMP request/reply timing to recover binary bits |

| 2️⃣  | Convert binary bits to ASCII (hex-encoded ciphertext)    |

| 3️⃣  | Extract AES key and IV from the capture comment          |

| 4️⃣  | Decrypt ciphertext using AES-128-CBC and remove padding  |

---

**Final Output:**

After successful decryption, the plaintext contains the **challenge flag**.

---
