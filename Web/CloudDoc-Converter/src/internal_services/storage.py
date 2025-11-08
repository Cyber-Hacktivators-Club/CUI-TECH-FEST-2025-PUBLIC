#!/usr/bin/env python3
"""
Internal Document Storage Service
Part of CloudDoc Converter infrastructure
"""

from flask import Flask, send_file, jsonify
import io

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "document-storage",
        "status": "operational",
        "version": "2.1.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/documents')
def documents():
    return jsonify({
        "total_documents": 1247,
        "storage_used": "45.2GB",
        "last_backup": "2025-11-02T14:30:00Z"
    })

@app.route('/internal/admin/flag.txt')
def get_flag():
    """Internal administrative endpoint - should not be accessible externally"""
    try:
        with open('/flag.txt', 'r') as f:
            flag_content = f.read().strip()
        return flag_content, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return "CHC{flag_file_not_found}", 500, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
