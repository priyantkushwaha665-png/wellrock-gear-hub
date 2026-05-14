import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "wellrock_secret_2026"

basedir = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(basedir, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Database with Category, Review, and Rating
    cur.execute('''CREATE TABLE IF NOT EXISTS products 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, price TEXT, img TEXT, affiliate_link TEXT, 
                    category TEXT, review TEXT, rating INTEGER)''')
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
    if request.method == 'POST':
        # Login Logic
        if 'login_btn' in request.form:
            user = request.form.get('username')
            pwd = request.form.get('password')
            if user == "wellrock27" and pwd == "wellrockgearhab":
                session['logged_in'] = True
                return redirect(url_for('admin'))
            else:
                return "Invalid Credentials!"
        
        # Add Product Logic
        elif 'add_product' in request.form and session.get('logged_in'):
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("INSERT INTO products (name, price, img, affiliate_link, category, review, rating) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                        (request.form.get('name'), request.form.get('price'), 
                         request.form.get('img'), request.form.get('affiliate_link'), 
                         request.form.get('category'), request.form.get('review'),
                         request.form.get('rating')))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))

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
