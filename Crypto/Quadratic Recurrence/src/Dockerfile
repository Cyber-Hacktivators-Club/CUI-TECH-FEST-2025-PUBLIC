FROM alpine:latest

# Install Python and dependencies
RUN apk update && \
    apk add --no-cache python3 py3-pip socat && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir pycryptodome

# Make sure the venv Python is used by default
ENV PATH="/opt/venv/bin:$PATH"

# Working directory
WORKDIR /app

# Copy files
COPY File.py /app/File.py
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Permissions
RUN chmod +x /docker-entrypoint.sh /app/File.py
RUN mkdir -p /app/dist

# Expose port
EXPOSE 8080

# Entry point
ENTRYPOINT ["/docker-entrypoint.sh"]
