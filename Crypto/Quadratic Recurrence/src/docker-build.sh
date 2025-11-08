#!/bin/sh

IMAGE_NAME="ctf_quadratic_recurrence"

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Change to the script's directory (where the Dockerfile is)
cd "$SCRIPT_DIR" || { echo "Failed to change directory to $SCRIPT_DIR"; exit 1; }

# Remove existing image if it exists
if docker images | grep -q "$IMAGE_NAME"; then
    echo "Removing old image: $IMAGE_NAME"
    docker rmi -f "$IMAGE_NAME"
else
    echo "No old image found."
fi

# Build new image
echo "Building new Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" .

echo "Build complete!"
