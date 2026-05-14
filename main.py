import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "wellrock_secure_2026"

basedir = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(basedir, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Updated Schema: added real_price and public_reviews
    cur.execute('''CREATE TABLE IF NOT EXISTS products 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, real_price TEXT, discount_price TEXT, img TEXT, 
                    affiliate_link TEXT, category TEXT, review TEXT, rating INTEGER)''')
    
    # Table for Public Reviews
    cur.execute('''CREATE TABLE IF NOT EXISTS user_reviews 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    product_id INTEGER, user_name TEXT, user_text TEXT)''')
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

@app.route('/submit_review', methods=['POST'])
def submit_review():
    p_id = request.form.get('product_id')
    name = request.form.get('user_name')
    msg = request.form.get('user_text')
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO user_reviews (product_id, user_name, user_text) VALUES (?, ?, ?)", (p_id, name, msg))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'login_btn' in request.form:
            user = request.form.get('username')
            pwd = request.form.get('password')
            if user == "wellrock27" and pwd == "wellrockgearhab":
                session['logged_in'] = True
                return redirect(url_for('admin'))
        
        elif 'add_product' in request.form and session.get('logged_in'):
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("INSERT INTO products (name, real_price, discount_price, img, affiliate_link, category, review, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                        (request.form.get('name'), request.form.get('real_price'), request.form.get('discount_price'),
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
