#!/bin/sh

get_flag(){
    echo $FLAG
}

# Ensure flag and temporary file are removed
rm -f /flag /app/flag.txt

# Get the flag and save it to a file
file_name="/flag.txt"
get_flag > "$file_name"

# Start two services:
# 1. The quiz on port 8080
echo "Starting quiz on port 8080..."
socat TCP-LISTEN:8080,reuseaddr,fork EXEC:"python3 /app/quiz.py"