from db import cursor, conn
from product import update_stock

def add_to_cart(product):
    if get_stock(product) < 1:
        return False

    cursor.execute("SELECT quantity FROM cart WHERE product = ?", (product,))
    if cursor.fetchone():
        cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE product = ?", (product,))
    else:
        cursor.execute("INSERT INTO cart (product, quantity) VALUES (?, ?)", (product, 1))

    cursor.execute("UPDATE products SET stock = stock - 1 WHERE name = ?", (product,))
    conn.commit()
    return True

def clear_cart():
    cursor.execute("SELECT product, quantity FROM cart")
    items = cursor.fetchall()
    for product, quantity in items:
        update_stock(product, quantity)
    cursor.execute("DELETE FROM cart")
    conn.commit()

def get_cart_items():
    cursor.execute("SELECT product, quantity FROM cart")
    return cursor.fetchall()

def get_stock(product):
    cursor.execute("SELECT stock FROM products WHERE name = ?", (product,))
    result = cursor.fetchone()
    return result[0] if result else 0
