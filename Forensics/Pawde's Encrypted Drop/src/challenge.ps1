<#
Title: SMB3 Encrypted Share Setup for CTF (Pawde's Encrypted Drop)
Run as Administrator on a Windows VM.
#>

Write-Host "=== Setting up SMB3 CTF Environment ===" -ForegroundColor Cyan

# === 1. Variables ===
$ShareName = "PawdeShare"
$FolderPath = "C:\PawdeDrop"
$UserName = "ctf_pawde"
$UserPasswordPlain = "blackie1189"
$Flag = "CHC{p4wd3_3ncryp73d_dr0p}"

# === 2. Create local folder and flag ===
Write-Host "[*] Creating share folder and flag file..."
Try {
    New-Item -Path $FolderPath -ItemType Directory -Force -ErrorAction Stop | Out-Null
    Set-Content -Path (Join-Path $FolderPath "flag.txt") -Value $Flag -ErrorAction Stop
    Write-Host "[+] Folder and flag created at $FolderPath"
} Catch {
    Write-Host "[-] Failed to create folder or flag: $_" -ForegroundColor Red
    exit 1
}

# === 3. Create local user for SMB ===
Write-Host "[*] Creating local user $UserName ..."
try {
    $existing = Get-LocalUser -Name $UserName -ErrorAction SilentlyContinue
} catch {
    $existing = $null
}
if ($null -ne $existing) {
    Write-Host "[-] User already exists, skipping creation."
} else {
    $pw = ConvertTo-SecureString $UserPasswordPlain -AsPlainText -Force
    try {
        New-LocalUser -Name $UserName -Password $pw -FullName "CTF Pawde User" -PasswordNeverExpires -ErrorAction Stop
        Add-LocalGroupMember -Group "Users" -Member $UserName -ErrorAction Stop
        Write-Host "[+] Created user: $UserName / Password: $UserPasswordPlain"
    } catch {
        Write-Host "[-] Failed to create local user: $_" -ForegroundColor Red
        exit 1
    }
}

# === 4. Set NTFS permissions ===
Write-Host "[*] Setting NTFS permissions..."
try {
    icacls $FolderPath /grant "${UserName}:(OI)(CI)F" | Out-Null
    Write-Host "[+] NTFS permissions granted to $UserName"
} catch {
    Write-Host "[-] Failed to set NTFS permissions: $_" -ForegroundColor Red
}

# === 5. Create SMB share and require encryption ===
Write-Host "[*] Creating SMB share '$ShareName'..."
try {
    $existingShare = Get-SmbShare -Name $ShareName -ErrorAction SilentlyContinue
} catch {
    $existingShare = $null
}
if ($null -ne $existingShare) {
    Write-Host "[-] Share already exists, skipping creation."
} else {
    try {
        New-SmbShare -Name $ShareName -Path $FolderPath -FullAccess $UserName -ErrorAction Stop | Out-Null
        Write-Host "[+] Created SMB share $ShareName"
    } catch {
        Write-Host "[-] Failed to create SMB share: $_" -ForegroundColor Red
        exit 1
    }
}

# Require encryption on the share and server
try {
    Set-SmbShare -Name $ShareName -EncryptData $true -ErrorAction Stop
    Set-SmbServerConfiguration -EncryptData $true -Force -ErrorAction Stop
    Write-Host "[+] SMB encryption required on share and server"
} catch {
    Write-Host "[-] Failed to set SMB encryption: $_" -ForegroundColor Yellow
    # not fatal — continue
}

# === 6. Ensure NTLMv2 only ===
Write-Host "[*] Enforcing NTLMv2 authentication (LmCompatibilityLevel = 5)..."
try {
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LmCompatibilityLevel /t REG_DWORD /d 5 /f | Out-Null
    Write-Host "[+] NTLMv2 enforced"
} catch {
    Write-Host "[-] Failed to set registry value: $_" -ForegroundColor Yellow
}

# === 7. Enable SMB inbound traffic (Firewall) ===
Write-Host "[*] Configuring firewall for SMB (port 445)..."
try {
    if (-not (Get-NetFirewallRule -DisplayName "Allow SMB Inbound" -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule -DisplayName "Allow SMB Inbound" -Direction Inbound -Protocol TCP -LocalPort 445 -Action Allow | Out-Null
        Write-Host "[+] Firewall rule created: Allow SMB Inbound"
    } else {
        Write-Host "[-] Firewall rule 'Allow SMB Inbound' already exists"
    }
} catch {
    Write-Host "[-] Failed to create firewall rule: $_" -ForegroundColor Yellow
}

# Build the UNC path safely
$computerName = $env:COMPUTERNAME
$shareUNC = "\\$computerName\$ShareName"

Write-Host "`n[+] SMB3 CTF Environment ready!" -ForegroundColor Green
Write-Host "Share: $shareUNC"
Write-Host "User: $UserName"
Write-Host "Password: $UserPasswordPlain"
Write-Host "Folder: $FolderPath"
Write-Host "`n[*] Next steps:"
Write-Host "1. Start Wireshark or tcpdump on this host."
Write-Host "2. From another VM: connect using -> net use \\<server-ip>\$ShareName /user:$UserName $UserPasswordPlain"
Write-Host "3. Copy the flag file or upload a file to trigger SMB3 encryption."
Write-Host "4. Stop capture and save challenge.pcapng."
