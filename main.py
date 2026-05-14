import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "wellrock_secret_key_123" # Session secure karne ke liye

basedir = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(basedir, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS products 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, price TEXT, img TEXT, affiliate_link TEXT, category TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    init_db()
    cat = request.args.get('cat')
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    if cat:
        cur.execute("SELECT * FROM products WHERE category = ?", (cat,))
    else:
        cur.execute("SELECT * FROM products")
    items = cur.fetchall()
    conn.close()
    return render_template('index.html', products=items)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Login Check
    if request.method == 'POST':
        # Agar login form submit hua hai
        if 'login_btn' in request.form:
            user = request.form.get('username')
            pwd = request.form.get('password')
            if user == "wellrock27" and pwd == "wellrockgearhab":
                session['logged_in'] = True
                return redirect(url_for('admin'))
            else:
                return "Galat Username ya Password!"
        
        # Agar Product add form submit hua hai
        elif 'add_product' in request.form and session.get('logged_in'):
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("INSERT INTO products (name, price, img, affiliate_link, category) VALUES (?, ?, ?, ?, ?)", 
                        (request.form.get('name'), request.form.get('price'), 
                         request.form.get('img'), request.form.get('affiliate_link'), 
                         request.form.get('category')))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))

    # Admin page view logic
    items = []
    if session.get('logged_in'):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        items = cur.fetchall()
        conn.close()
    
    return render_template('admin.html', products=items, logged_in=session.get('logged_in'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete_product(id):
    if session.get('logged_in'):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
