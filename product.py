from db import cursor, conn

def fetch_products():
    cursor.execute("SELECT name, price, stock FROM products")
    return cursor.fetchall()

def add_product(name, price, stock):
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name.lower(), price, stock))
    conn.commit()

def delete_product(name):
    cursor.execute("DELETE FROM products WHERE name = ?", (name,))
    conn.commit()

def product_in_cart(name):
    cursor.execute("SELECT 1 FROM cart WHERE product = ?", (name,))
    return cursor.fetchone() is not None

def update_stock(name, delta):
    cursor.execute("UPDATE products SET stock = stock + ? WHERE name = ?", (delta, name))
    conn.commit()

def get_stock(name):
    cursor.execute("SELECT stock FROM products WHERE name = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else 0
