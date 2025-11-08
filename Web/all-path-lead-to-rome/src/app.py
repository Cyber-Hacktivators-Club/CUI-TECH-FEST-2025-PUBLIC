from flask import Flask, render_template, request, redirect, url_for, session, flash
from lxml import etree
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Simple XML user store (vulnerable to XPath injection)
USERS_XML = "users.xml"
FLAG_FILE = "/flag.txt"   # read flag from this file at runtime

def authenticate(username, password):
    # Vulnerable XPath construction (no sanitization)
    try:
        tree = etree.parse(USERS_XML)
        # The following line is intentionally vulnerable for the challenge:
        query = "//user[username/text()='{u}' and password/text()='{p}']".format(u=username, p=password)
        res = tree.xpath(query)
        return len(res) > 0
    except Exception:
        return False

def read_flag():
    """
    Read the flag from FLAG_FILE.
    If the file is missing or unreadable, return a harmless placeholder message.
    """
    try:
        with open(FLAG_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "FLAG_FILE_NOT_FOUND_OR_UNREADABLE"

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username','')
        pw = request.form.get('password','')
        if authenticate(user, pw):
            # show flag when 'admin' is authenticated
            # Note: keep the same simple check as before to avoid changing exploit logic
            if user.strip().lower() == 'admin' or 'admin' in user.lower():
                flag = read_flag()
                return render_template('admin.html', flag=flag)
            return render_template('success.html', user=user)
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/static/<path:p>')
def static_files(p):
    return app.send_static_file(p)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
