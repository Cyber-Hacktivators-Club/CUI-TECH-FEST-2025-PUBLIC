#!/bin/bash
# Build and run CloudDoc Converter standalone container
#
# Usage:
#   ./build-standalone.sh [FLAG]
#
# Examples:
#   ./build-standalone.sh
#   ./build-standalone.sh "CHC{my_custom_flag_12345}"

FLAG="${1:-CHC{cl0ud_m3t4d4t4_ssrf_ch41n_3xpl01t4t10n_by_4b_f4t1r}}"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        CloudDoc Converter - Standalone Build                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Flag: $FLAG"
echo ""

# Build the image
echo "[*] Building Docker image..."
docker build \
    --build-arg FLAG="$FLAG" \
    -f Dockerfile.standalone \
    -t clouddoc-converter:latest \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  ✓ Build successful!                                         ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "To run the container:"
    echo "  docker run -d -p 3000:3000 --name clouddoc clouddoc-converter:latest"
    echo ""
    echo "To stop and remove:"
    echo "  docker stop clouddoc && docker rm clouddoc"
else
    echo ""
    echo "✗ Build failed!"
    exit 1
fi
