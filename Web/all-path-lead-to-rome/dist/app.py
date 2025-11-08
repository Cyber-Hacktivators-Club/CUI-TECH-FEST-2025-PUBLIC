from flask import Flask, render_template, request, redirect, url_for, session, flash
from lxml import etree
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Simple XML user store (vulnerable to XPath injection)
USERS_XML = "users.xml"

def authenticate(username, password):
    # Vulnerable XPath construction (no sanitization)
    try:
        tree = etree.parse(USERS_XML)
        # The following line is intentionally vulnerable for the challenge:
        query = "//user[username/text()='{u}' and password/text()='{p}']".format(u=username, p=password)
        res = tree.xpath(query)
        return len(res) > 0
    except Exception as e:
        return False

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username','')
        pw = request.form.get('password','')
        if authenticate(user, pw):
            # show flag when 'admin' is authenticated
            if user.strip().lower() == 'admin' or 'admin' in user.lower():
                return render_template('admin.html')
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
