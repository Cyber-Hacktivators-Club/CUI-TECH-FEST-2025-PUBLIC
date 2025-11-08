FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y \
    socat gcc gcc-multilib libc6-dev-i386 \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Copy files

COPY busquets.c  /app/busquets.c 

# Expose port
EXPOSE 8082

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
