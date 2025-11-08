FROM python:3.11-slim
WORKDIR /app
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY . /app
RUN pip install flask lxml
EXPOSE 8080
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
