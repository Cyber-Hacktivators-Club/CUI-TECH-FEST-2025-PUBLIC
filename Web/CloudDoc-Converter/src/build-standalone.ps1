# Build and run CloudDoc Converter standalone container
#
# Usage:
#   .\build-standalone.ps1 [FLAG]
#
# Examples:
#   .\build-standalone.ps1
#   .\build-standalone.ps1 "CHC{my_custom_flag_12345}"

param(
    [string]$Flag = "CHC{cl0ud_m3t4d4t4_ssrf_ch41n_3xpl01t4t10n_by_4b_f4t1r}"
)

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        CloudDoc Converter - Standalone Build                 ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "Flag: $Flag`n" -ForegroundColor Yellow

# Build the image
Write-Host "[*] Building Docker image..." -ForegroundColor Blue

docker build `
    --build-arg FLAG="$Flag" `
    -f Dockerfile.standalone `
    -t clouddoc-converter:latest `
    .

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✓ Build successful!                                         ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green
    
    Write-Host "To run the container:" -ForegroundColor Cyan
    Write-Host "  docker run -d -p 3000:3000 --name clouddoc clouddoc-converter:latest`n" -ForegroundColor White
    
    Write-Host "To stop and remove:" -ForegroundColor Cyan
    Write-Host "  docker stop clouddoc; docker rm clouddoc`n" -ForegroundColor White
    
    Write-Host "To view logs:" -ForegroundColor Cyan
    Write-Host "  docker logs -f clouddoc`n" -ForegroundColor White
} else {
    Write-Host "`n✗ Build failed!" -ForegroundColor Red
    exit 1
}
