# get_flag_with_domain.ps1 — minimal SMB fetch with domain included
$server = "192.168.42.129"
$share  = "PawdeShare"
$user   = "ctf_pawde"
$domain = "DESKTOP-ECFV9MR"
$pass   = "blackie1189"

$remote = "\\$server\$share\flag.txt"
$dest   = "$env:USERPROFILE\Downloads\flag_pawde.txt"

# map using DOMAIN\user, copy, unmap
net use "\\$server\$share" $pass /user:"$domain\$user" | Out-Null
Copy-Item $remote $dest -Force
net use "\\$server\$share" /delete | Out-Null

Write-Host "Saved flag to: $dest"
Get-Content $dest
