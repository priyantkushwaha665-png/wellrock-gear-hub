import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB_FILE = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Products Table
    cur.execute('''CREATE TABLE IF NOT EXISTS products 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, real_price TEXT, 
                    discount_price TEXT, img_url TEXT, buy_link TEXT, category TEXT, 
                    wrx_review TEXT, rating INTEGER)''')
    # User Reviews Table
    cur.execute('''CREATE TABLE IF NOT EXISTS user_reviews 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, 
                    user_name TEXT, user_text TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    cat = request.args.get('cat')
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    if cat:
        cur.execute("SELECT * FROM products WHERE category = ?", (cat,))
    else:
        cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template('index.html', products=products)

# --- NAYA PRODUCT PAGE ROUTE ---
@app.route('/product/<int:id>')
def product_page(id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = cur.fetchone()
    cur.execute("SELECT * FROM user_reviews WHERE product_id = ?", (id,))
    reviews = cur.fetchall()
    conn.close()
    return render_template('product.html', product=product, reviews=reviews)

@app.route('/submit_review', method=['POST'])
def submit_review():
    p_id = request.form['product_id']
    name = request.form['user_name']
    text = request.form['user_text']
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO user_reviews (product_id, user_name, user_text) VALUES (?, ?, ?)", (p_id, name, text))
    conn.commit()
    conn.close()
    return redirect(f'/product/{p_id}')

if __name__ == '__main__':
    app.run(debug=True)
