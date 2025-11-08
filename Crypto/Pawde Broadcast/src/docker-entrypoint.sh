#!/bin/sh

get_flag() {
    # Only user controlled variable.
    #Dont change anything here
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
DEFAULT_FILE="/app/File.py"


# Set default values if variables are not set
PORT="${PORT:-$DEFAULT_PORT}"
FILE="${FILE:-$DEFAULT_FILE}"

# Ensure the file exists
#[ ! -f "$FILE" ] && { echo "File not found: $FILE"; exit 1; }

# Use socat to listen on the port and send the file contents
# Start socat listener
echo "Listening on port 8080..."
socat TCP-LISTEN:8080,reuseaddr,fork EXEC:"python3 /app/File.py"

