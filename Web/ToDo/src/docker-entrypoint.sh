#!/bin/sh

get_flag() {
    echo "$FLAG"
}

# Ensure flag and temporary file are removed
rm -f /flag /app/flag.txt

# Get the flag and save it to a file
file_name="/flag.txt"
get_flag > "$file_name"

# Remove the script itself
rm -- "$0"

DEFAULT_PORT=8080
DEFAULT_FILE="/app/index.js"


# Set default values if variables are not set
PORT="${PORT:-$DEFAULT_PORT}"

# Ensure the file exists
[ ! -f "$file_name" ] && { echo "File not found: $file_name"; exit 1; }

# Use socat to listen on the port and send the file contents
# Use tee to also print the file contents to stdout
echo "Listening on port $PORT and starting express server..."
node seeds.js
node index.js
