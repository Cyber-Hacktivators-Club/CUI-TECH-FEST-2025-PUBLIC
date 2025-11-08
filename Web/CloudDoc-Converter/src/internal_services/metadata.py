#!/usr/bin/env python3
"""
Cloud Metadata Service Simulator
Mimics AWS Instance Metadata Service
"""

from flask import Flask, Response, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return Response("""1.0
2021-01-03
latest
""", mimetype='text/plain')

@app.route('/latest')
def latest():
    return Response("""meta-data
user-data
dynamic
""", mimetype='text/plain')

@app.route('/latest/meta-data')
@app.route('/latest/meta-data/')
def metadata_index():
    return Response("""ami-id
instance-id
instance-type
local-hostname
local-ipv4
iam/
placement/
""", mimetype='text/plain')

@app.route('/latest/meta-data/ami-id')
def ami_id():
    return "ami-0abcdef1234567890"

@app.route('/latest/meta-data/instance-id')
def instance_id():
    return "i-0123456789abcdef0"

@app.route('/latest/meta-data/instance-type')
def instance_type():
    return "t3.medium"

@app.route('/latest/meta-data/local-hostname')
def local_hostname():
    return "ip-172-31-45-67.ec2.internal"

@app.route('/latest/meta-data/local-ipv4')
def local_ipv4():
    return "172.31.45.67"

@app.route('/latest/meta-data/iam')
@app.route('/latest/meta-data/iam/')
def iam_index():
    return Response("""info
security-credentials/
""", mimetype='text/plain')

@app.route('/latest/meta-data/iam/security-credentials')
@app.route('/latest/meta-data/iam/security-credentials/')
def security_credentials_index():
    return Response("""clouddoc-service-role
""", mimetype='text/plain')

@app.route('/latest/meta-data/iam/security-credentials/clouddoc-service-role')
def service_role():
    credentials = {
        "Code": "Success",
        "LastUpdated": "2025-11-03T12:00:00Z",
        "Type": "AWS-HMAC",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "Token": "AQoEXAMPLEH4aoAH0gNCAPyJxz4BlCFFxWNE1OPTgk5TthT+FvwqnKwRcOIfrRh3c4/...TRUNCATED",
        "Expiration": "2025-11-03T18:00:00Z",
        "InternalNote": "Service role has access to internal-storage service on port 8080"
    }
    return jsonify(credentials)

@app.route('/latest/user-data')
def user_data():
    return Response("""#!/bin/bash
# Cloud-init configuration
echo "Initializing CloudDoc Converter service..."
export STORAGE_ENDPOINT="internal-storage:8080"
export ADMIN_PATH="/internal/admin"
""", mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
