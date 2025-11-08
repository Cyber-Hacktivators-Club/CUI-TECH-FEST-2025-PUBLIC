# Pawde's Persistent Problem - Solution

## Challenge Info

**Category:** Forensics

**Files:** Registry hives (SYSTEM, SOFTWARE, NTUSER.DAT)

## Solution

### Step 1: Load Registry Hives

Open the provided registry files using Registry Explorer or similar tool.

### Step 2: Check Common Persistence Locations

Navigate to common registry persistence keys:

**Location 1:**

```
HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\
```

**Location 2:**

```
HKCU\Environment\UserInitMprLogonScript
```

**Location 3:**

```
HKLM\SOFTWARE\Microsoft\Netsh
```

**Location 4:**

```
HKLM\SYSTEM\CurrentControlSet\Services\Evil Service
```

### Step 3: Find Suspicious Entry

Examine each location for suspicious values. One of these registry paths contains Pawde's persistence mechanism:

```
Key: [PLACEHOLDER_SUSPICIOUS_KEY_PATH]
Value Name: [PLACEHOLDER_VALUE_NAME]
Value Data: [PLACEHOLDER_VALUE_DATA]
```

### Step 4: Extract Base64 Values

Check the registry values at each location. You'll find Base64 encoded strings in the data fields:

**From Location 1:**

```
[PLACEHOLDER_BASE64_PART_1]
```

**From Location 2:**

```
[PLACEHOLDER_BASE64_PART_2]
```

**From Location 3:**

```
[PLACEHOLDER_BASE64_PART_3]
```

**From Location 4:**

```
[PLACEHOLDER_BASE64_PART_4]
```

### Step 5: Decode and Combine

Decode each Base64 string:

```bash
echo "[PLACEHOLDER_BASE64_PART_1]" | base64 -d
echo "[PLACEHOLDER_BASE64_PART_2]" | base64 -d
echo "[PLACEHOLDER_BASE64_PART_3]" | base64 -d
echo "[PLACEHOLDER_BASE64_PART_4]" | base64 -d
```

Combine the decoded parts to get the flag.

---
