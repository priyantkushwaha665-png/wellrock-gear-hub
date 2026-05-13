from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DB_FILE = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price TEXT, img_url TEXT)')
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=items)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "wellrockgearhab"
            name = request.form.get('name')
            price = request.form.get('price')
            img_url = request.form.get('img_url')
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, price, img_url) VALUES (?, ?, ?)', (name, price, img_url))
            conn.commit()
            conn.close()
            return redirect('/')
        else:
            return "Galat Password! Dubara try karein."
    
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)