#!/bin/bash
# Entrypoint script for CloudDoc Converter standalone container

# Add localhost aliases for internal services
echo "127.0.0.1 metadata-service" >> /etc/hosts
echo "127.0.0.1 internal-storage" >> /etc/hosts

# Start supervisor
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
