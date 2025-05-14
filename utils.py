import csv
from db import cursor

def save_order_to_csv(filename="order.csv"):
    cursor.execute("SELECT product, quantity FROM cart")
    items = cursor.fetchall()
    if not items:
        return False

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product", "Quantity", "Unit Price", "Total"])
        total = 0
        for product, quantity in items:
            cursor.execute("SELECT price FROM products WHERE name = ?", (product,))
            price = cursor.fetchone()[0]
            subtotal = price * quantity
            total += subtotal
            writer.writerow([product, quantity, f"{price:.2f}", f"{subtotal:.2f}"])
        writer.writerow(["", "", "Total", f"{total:.2f}"])
    return True
