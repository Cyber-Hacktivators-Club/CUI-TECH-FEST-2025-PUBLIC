#!/bin/sh

# Save flag
echo "$FLAG" > /flag.txt

# Compile file.c and extract the base64 string


# Compile the patched target
gcc -fno-stack-protector -z execstack -no-pie -o busquets busquets.c 
chmod +x /app/busquets



# Start socat listener
PORT=8082
echo "Listening on port $PORT..."
exec socat TCP-LISTEN:$PORT,reuseaddr,fork EXEC:/app/busquets,pty,raw,echo=0
