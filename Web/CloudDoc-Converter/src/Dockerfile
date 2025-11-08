# CloudDoc Converter - Standalone Docker Image
# All services in one container for easy deployment
FROM python:3.11-slim

# Build argument for dynamic flag
ARG FLAG="CHC{cl0ud_m3t4d4t4_ssrf_ch41n_3xpl01t4t10n_by_4b_f4t1r}"

# Install system dependencies including wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    fontconfig \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    xfonts-75dpi \
    xfonts-base \
    xfonts-encodings \
    xfonts-utils \
    && rm -rf /var/lib/apt/lists/*

# Download and install wkhtmltopdf from GitHub releases
RUN wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && apt-get update \
    && apt-get install -y ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && rm wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Install supervisor to manage multiple processes
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Copy internal services
RUN mkdir -p /app/internal_services
COPY internal_services/storage.py /app/internal_services/storage.py
COPY internal_services/metadata.py /app/internal_services/metadata.py

# Create flag file
RUN echo "${FLAG}" > /flag.txt && chmod 644 /flag.txt

# Create supervisor configuration
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose main web port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:3000/health', timeout=5)" || exit 1

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
