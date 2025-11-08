#!/bin/sh

get_flag(){
    echo $FLAG
}

# Ensure flag temporary file is removed
rm -f /flag

# Copy template flag into place
cp /app/flag.txt /app/flag.txt.tmp

# Replace CHC{...} in flag.txt.tmp with $FLAG using sed regex
if [ -n "$FLAG" ]; then
    sed -i -E "s/CHC\{[^}]*\}/$FLAG/" /app/flag.txt.tmp
else
    echo "Warning: FLAG variable not set!"
fi

# Rename final file
mv /app/flag.txt.tmp /app/flag.txt

# Start two services:
# 1. The quiz on port 8080
echo "Starting quiz on port 8080..."
socat TCP-LISTEN:8080,reuseaddr,fork EXEC:"python3 /app/quiz.py"
