import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(basedir, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS products 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, price TEXT, img TEXT, affiliate_link TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    items = cur.fetchall()
    conn.close()
    return render_template('index.html', products=items)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "wellrockgearhab":
            name = request.form.get('name')
            price = request.form.get('price')
            img = request.form.get('img')
            affiliate_link = request.form.get('affiliate_link')
            
            cur.execute("INSERT INTO products (name, price, img, affiliate_link) VALUES (?, ?, ?, ?)", 
                        (name, price, img, affiliate_link))
            conn.commit()
            return redirect(url_for('admin'))
            
    cur.execute("SELECT * FROM products")
    items = cur.fetchall()
    conn.close()
    return render_template('admin.html', products=items)

# Ye naya function hai delete karne ke liye
@app.route('/delete/<int:id>')
def delete_product(id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
