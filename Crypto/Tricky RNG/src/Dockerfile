FROM alpine:latest

RUN apk update && \
    apk add --no-cache python3 py3-pip socat && \
    pip install --no-cache-dir --upgrade pip --break-system-packages

WORKDIR /app

COPY File.py /app/File.py
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh /app/File.py
RUN mkdir -p /app/dist

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]
