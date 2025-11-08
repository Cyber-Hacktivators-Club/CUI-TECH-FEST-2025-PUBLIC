FROM python:3.11-alpine

WORKDIR /app

# Install necessary packages
RUN apk add --no-cache socat

# Copy application files
COPY app/quiz.py /app/quiz.py
COPY app/questions.json /app/questions.json

# Expose ports
EXPOSE 8080

# Copy entrypoint script
COPY app/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]