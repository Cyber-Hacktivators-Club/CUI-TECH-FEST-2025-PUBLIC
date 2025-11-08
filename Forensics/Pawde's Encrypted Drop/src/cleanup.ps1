<#
Title: Cleanup SMB CTF Environment (Pawde)
Run as Administrator on the same host where setup was run.
#>

Write-Host "=== Cleaning up SMB3 CTF Environment ===" -ForegroundColor Cyan

$ShareName = "PawdeShare"
$FolderPath = "C:\PawdeDrop"
$UserName = "ctf_pawde"
$FirewallRuleName = "Allow SMB Inbound"

# Remove SMB share
try {
    if (Get-SmbShare -Name $ShareName -ErrorAction SilentlyContinue) {
        Remove-SmbShare -Name $ShareName -Force -ErrorAction Stop
        Write-Host "[+] Removed SMB share: $ShareName"
    } else {
        Write-Host "[-] SMB share not found: $ShareName"
    }
} catch {
    Write-Host "[-] Failed to remove SMB share: $_" -ForegroundColor Yellow
}

# Remove local user
try {
    if (Get-LocalUser -Name $UserName -ErrorAction SilentlyContinue) {
        Remove-LocalUser -Name $UserName -ErrorAction Stop
        Write-Host "[+] Removed local user: $UserName"
    } else {
        Write-Host "[-] Local user not found: $UserName"
    }
} catch {
    Write-Host "[-] Failed to remove local user: $_" -ForegroundColor Yellow
}

# Remove firewall rule
try {
    if (Get-NetFirewallRule -DisplayName $FirewallRuleName -ErrorAction SilentlyContinue) {
        Remove-NetFirewallRule -DisplayName $FirewallRuleName -ErrorAction Stop
        Write-Host "[+] Removed firewall rule: $FirewallRuleName"
    } else {
        Write-Host "[-] Firewall rule not found: $FirewallRuleName"
    }
} catch {
    Write-Host "[-] Failed to remove firewall rule: $_" -ForegroundColor Yellow
}

# Remove folder (prompt)
if (Test-Path $FolderPath) {
    try {
        Remove-Item -Path $FolderPath -Recurse -Force -ErrorAction Stop
        Write-Host "[+] Removed folder: $FolderPath"
    } catch {
        Write-Host "[-] Failed to remove folder: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "[-] Folder not found: $FolderPath"
}

Write-Host "`n[+] Cleanup complete."
