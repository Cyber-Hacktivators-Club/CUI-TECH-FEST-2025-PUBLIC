#!/usr/bin/env python3
"""
CloudDoc Converter - Document Conversion Microservice
Challenge by Ab_Fatir for CHC CTF
"""

from flask import Flask, request, jsonify, send_file, render_template_string
import requests
import pdfkit
import io
from urllib.parse import urlparse

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Complete SEO Toolkit</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(180deg, #1a0b3d 0%, #0a0520 100%);
            color: white;
            overflow-x: hidden;
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 60px;
            position: relative;
            z-index: 10;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 18px;
            font-weight: 600;
        }

        .logo svg {
            width: 24px;
            height: 24px;
        }

        .nav-links {
            display: flex;
            gap: 30px;
            list-style: none;
        }

        .nav-links a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s;
        }

        .nav-links a:hover {
            color: white;
        }

        .nav-actions {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .login-btn {
            color: white;
            text-decoration: none;
            font-size: 14px;
        }

        .get-started-btn {
            background: linear-gradient(135deg, #6c3aed 0%, #8b5cf6 100%);
            color: white;
            padding: 10px 24px;
            border-radius: 25px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: transform 0.2s;
        }

        .get-started-btn:hover {
            transform: translateY(-2px);
        }

        .hero {
            text-align: center;
            padding: 80px 20px 40px;
            position: relative;
        }

        .hero-badge {
            display: inline-block;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 30px;
            color: #a78bfa;
        }

        h1 {
            font-size: 64px;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-subtitle {
            font-size: 18px;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 40px;
            line-height: 1.6;
        }

        .email-form {
            display: flex;
            gap: 10px;
            max-width: 500px;
            margin: 0 auto 60px;
        }

        .email-input {
            flex: 1;
            padding: 16px 24px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.05);
            color: white;
            font-size: 14px;
            outline: none;
        }

        .email-input::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }

        .demo-btn {
            padding: 16px 32px;
            border-radius: 30px;
            background: linear-gradient(135deg, #6c3aed 0%, #8b5cf6 100%);
            color: white;
            border: none;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .demo-btn:hover {
            transform: scale(1.05);
        }

        .dashboard-preview {
            position: relative;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 40px;
        }

        .preview-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }

        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card h3 {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: 12px;
        }

        .card .value {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .card .label {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.5);
        }

        .stars {
            color: #fbbf24;
            margin-bottom: 12px;
        }

        .google-preview {
            display: flex;
            align-items: center;
            gap: 12px;
            background: white;
            color: #333;
            padding: 16px;
            border-radius: 8px;
            margin-top: 16px;
        }

        .competitor-card {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: #1a0b3d;
        }

        .chart {
            width: 100%;
            height: 80px;
            margin-top: 16px;
        }

        .companies {
            text-align: center;
            padding: 60px 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .companies p {
            color: rgba(255, 255, 255, 0.5);
            margin-bottom: 30px;
            font-size: 14px;
        }

        .company-logos {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 60px;
            flex-wrap: wrap;
        }

        .company-logo {
            font-size: 24px;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.6);
        }

        #result {
            max-width: 500px;
            margin: 20px auto;
            padding: 15px;
            border-radius: 30px;
            display: none;
            text-align: center;
        }

        .success {
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid rgba(34, 197, 94, 0.4);
            color: #4ade80;
        }

        .error {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #f87171;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 40px;
            }

            .preview-grid {
                grid-template-columns: 1fr;
            }

            nav {
                padding: 20px 30px;
            }

            .nav-links {
                display: none;
            }
        }
    </style>
</head>
<body>
    <nav>
        <div class="logo">
            <svg viewBox="0 0 24 24" fill="none">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            CloudDoc
        </div>
        <div class="nav-actions">
            <span style="color: rgba(255,255,255,0.3); font-size: 12px;">Enterprise Edition</span>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-badge">ENTERPRISE CLOUD SOLUTION</div>
        <h1>Document Conversion<br>Made Simple</h1>
        <p class="hero-subtitle">Transform any web content into professional PDFs with our<br>enterprise-grade cloud conversion platform.</p>
        
        <form class="email-form" id="pdfForm">
            <input type="text" class="email-input" id="url" name="url" placeholder="Enter URL to convert to PDF (e.g., https://example.com)">
            <button type="submit" class="demo-btn">Convert Now</button>
        </form>
        
        <div id="result"></div>
    </section>

    <section class="dashboard-preview">
        <div class="preview-grid">
            <div class="card">
                <h3>Documents Processed</h3>
                <div class="value">2.4M+</div>
                <div class="label">Last 30 days</div>
                <svg class="chart" viewBox="0 0 200 80">
                    <polyline points="0,60 40,45 80,50 120,30 160,35 200,20" fill="none" stroke="#8b5cf6" stroke-width="2"/>
                </svg>
            </div>

            <div class="card">
                <div class="stars">★★★★★</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 14px; margin-bottom: 16px;">Enterprise Customer</div>
                <div class="google-preview">
                    <svg style="width: 32px; height: 32px;" viewBox="0 0 24 24" fill="none">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" fill="#6c3aed"/>
                        <path d="M14 2v6h6" stroke="white" stroke-width="2"/>
                    </svg>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; font-size: 14px;">PDF Quality</div>
                        <div style="font-size: 12px; color: #666;">High-fidelity rendering</div>
                    </div>
                    <div style="color: #10b981; font-size: 12px; font-weight: 600;">✓ Verified</div>
                </div>
            </div>

            <div class="card competitor-card">
                <h3 style="color: #1a0b3d;">API Performance</h3>
                <div class="value">99.9%</div>
                <div class="label" style="color: rgba(26, 11, 61, 0.7);">uptime guarantee</div>
                <div style="margin-top: 16px; display: flex; gap: 8px;">
                    <span style="background: white; padding: 6px 12px; border-radius: 12px; font-size: 12px;">� REST API</span>
                    <span style="background: white; padding: 6px 12px; border-radius: 12px; font-size: 12px;">� Secure</span>
                </div>
            </div>
        </div>
    </section>

    <section class="companies">
        <p>Trusted by 4,000+ companies worldwide</p>
        <div class="company-logos">
            <div class="company-logo">TechCorp</div>
            <div class="company-logo">DATAFLOW</div>
            <div class="company-logo">nexus</div>
            <div class="company-logo">CloudBase</div>
            <div class="company-logo">DocuSign</div>
            <div class="company-logo">FileSync</div>
        </div>
    </section>

    <section style="max-width: 800px; margin: 60px auto 40px; padding: 0 40px;">
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px; text-align: center;">
            <div style="font-size: 13px; color: rgba(255,255,255,0.5); line-height: 1.8;">
                CloudDoc leverages enterprise-grade infrastructure powered by containerized microservices. 
                All document processing occurs within our secure cloud environment.
            </div>
        </div>
    </section>

    <script>
        document.getElementById('pdfForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = document.getElementById('url').value;
            const resultDiv = document.getElementById('result');
            
            resultDiv.style.display = 'block';
            resultDiv.className = '';
            resultDiv.innerHTML = 'Processing your request...';

            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = downloadUrl;
                    a.download = 'document-conversion.pdf';
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    
                    resultDiv.className = 'success';
                    resultDiv.innerHTML = '✓ Document converted successfully. Download started.';
                } else {
                    const error = await response.text();
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = '✗ Conversion error: ' + error;
                }
            } catch (error) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = '✗ Request failed: ' + error.message;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HOME_HTML)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "clouddoc-converter", "version": "1.2.4"})

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return "Missing required parameter: url", 400
        
        url = data['url'].strip()
        
        if not url:
            return "URL cannot be empty", 400
        
        parsed = urlparse(url)
        if not parsed.scheme:
            return "Invalid URL format", 400
        
        if parsed.scheme.lower() not in ['http', 'https']:
            return "Only HTTP and HTTPS protocols are supported", 403
        
        # Security filtering
        blocked = ['localhost', '127.0.0.1', '0.0.0.0', '169.254.169.254', '::1']
        url_lower = url.lower()
        
        for blocked_term in blocked:
            if blocked_term in url_lower:
                return f"Access to internal resources is not permitted", 403
        
        app.logger.info(f"Processing conversion request: {url}")
        
        try:
            headers = {
                'User-Agent': 'CloudDoc-Converter/1.2.4',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
            html_content = response.text
            
            pdf_bytes = pdfkit.from_string(html_content, False, options={
                'enable-local-file-access': False,
                'quiet': '',
            })
            
            pdf_io = io.BytesIO(pdf_bytes)
            pdf_io.seek(0)
            
            return send_file(
                pdf_io,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='document.pdf'
            )
            
        except requests.exceptions.Timeout:
            return "Request timeout - target server did not respond", 408
            
        except requests.exceptions.ConnectionError:
            return "Connection failed - unable to reach target server", 502
            
        except Exception as e:
            app.logger.error(f"Conversion error: {str(e)}")
            return "PDF conversion failed", 500
            
    except Exception as e:
        app.logger.error(f"Request error: {str(e)}")
        return "Invalid request", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
