import sqlite3

conn = sqlite3.connect("cart.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    name TEXT PRIMARY KEY,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    product TEXT PRIMARY KEY,
    quantity INTEGER NOT NULL
)
""")

conn.commit()
conn.close()
print("Database initialized.")
