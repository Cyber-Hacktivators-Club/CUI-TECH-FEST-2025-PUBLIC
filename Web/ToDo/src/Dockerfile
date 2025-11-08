# Dockerfile
FROM node:16-alpine

RUN mkdir /app
RUN apk update && \
    apk add --no-cache netcat-openbsd curl socat
    # python3 py3-pip \
    # python3 -m venv /venv && \
    # /venv/bin/pip install --upgrade pip 

COPY ./source/ ./app/
COPY docker-entrypoint.sh /docker-entrypoint.sh

WORKDIR /app
# COPY package.json /app

RUN npm install 

RUN chmod +x /app/index.js
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]
