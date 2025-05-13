import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
import sqlite3
import csv

# === Database connection ===
conn = sqlite3.connect("cart.db")
cursor = conn.cursor()

# === Bootstrap window ===
root = ttk.Window(themename="cyborg")  # inne motywy: "flatly", "darkly", "morph", "superhero"
root.title("Modern Shop GUI")
root.geometry("700x600")

# === Helper Functions ===
def fetch_products():
    cursor.execute("SELECT name, price, stock FROM products")
    return cursor.fetchall()

def refresh_product_list():
    product_list.delete(0, tk.END)
    for name, price, stock in fetch_products():
        product_list.insert(tk.END, f"{name} - {price:.2f} PLN (Stock: {stock})")

def add_to_cart_gui():
    selection = product_list.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Select a product.")
        return

    line = product_list.get(selection[0])
    product = line.split(" - ")[0]

    cursor.execute("SELECT stock FROM products WHERE name = ?", (product,))
    stock = cursor.fetchone()[0]
    if stock < 1:
        messagebox.showwarning("Out of stock", f"{product} is out of stock.")
        return

    cursor.execute("SELECT quantity FROM cart WHERE product = ?", (product,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE product = ?", (product,))
    else:
        cursor.execute("INSERT INTO cart (product, quantity) VALUES (?, ?)", (product, 1))
    cursor.execute("UPDATE products SET stock = stock - 1 WHERE name = ?", (product,))
    conn.commit()
    refresh_product_list()
    show_cart()

def show_cart():
    cart_list.delete(0, tk.END)
    cursor.execute("SELECT product, quantity FROM cart")
    items = cursor.fetchall()

    total = 0
    for product, quantity in items:
        cursor.execute("SELECT price FROM products WHERE name = ?", (product,))
        price = cursor.fetchone()[0]
        subtotal = price * quantity
        total += subtotal
        cart_list.insert(tk.END, f"{product} x{quantity} = {subtotal:.2f} PLN")

    total_label.config(text=f"Total: {total:.2f} PLN")

def clear_cart_gui():
    cursor.execute("SELECT product, quantity FROM cart")
    items = cursor.fetchall()
    for product, quantity in items:
        cursor.execute("UPDATE products SET stock = stock + ? WHERE name = ?", (quantity, product))
    cursor.execute("DELETE FROM cart")
    conn.commit()
    show_cart()
    refresh_product_list()
    messagebox.showinfo("Cart cleared", "Cart has been cleared.")

def save_order_gui():
    cursor.execute("SELECT product, quantity FROM cart")
    items = cursor.fetchall()
    if not items:
        messagebox.showinfo("Empty", "Cart is empty.")
        return

    with open("order.csv", "w", newline="", encoding="utf-8") as file:
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
    messagebox.showinfo("Saved", "Order saved to 'order.csv'")

def add_new_product_gui():
    name = simpledialog.askstring("New product", "Enter product name:", parent=root)
    if not name:
        return
    try:
        price = float(simpledialog.askstring("Price", f"Price of {name}:"))
        stock = int(simpledialog.askstring("Stock", f"Stock of {name}:"))
    except:
        messagebox.showerror("Invalid", "Price or stock not valid.")
        return

    try:
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name.lower(), price, stock))
        conn.commit()
        refresh_product_list()
    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate", "Product already exists.")

def delete_product_gui():
    selection = product_list.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Select a product to delete.")
        return

    product = product_list.get(selection[0]).split(" - ")[0]
    cursor.execute("SELECT 1 FROM cart WHERE product = ?", (product,))
    if cursor.fetchone():
        messagebox.showwarning("In cart", "Cannot delete a product in cart.")
        return

    cursor.execute("DELETE FROM products WHERE name = ?", (product,))
    conn.commit()
    refresh_product_list()

# === Layout ===

ttk.Label(root, text="Available Products", font=("Helvetica", 14)).pack(pady=5)
product_list = tk.Listbox(root, width=60, height=10, font=("Courier New", 10))
product_list.pack()

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Add to Cart", bootstyle=SUCCESS, command=add_to_cart_gui).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Add New Product", bootstyle=INFO, command=add_new_product_gui).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Delete Product", bootstyle=DANGER, command=delete_product_gui).grid(row=0, column=2, padx=5)

ttk.Label(root, text="Your Cart", font=("Helvetica", 14)).pack(pady=5)
cart_list = tk.Listbox(root, width=60, height=10, font=("Courier New", 10))
cart_list.pack()

ttk.Button(root, text="Clear Cart", bootstyle=WARNING, command=clear_cart_gui).pack(pady=5)
ttk.Button(root, text="Save Order to CSV", bootstyle=PRIMARY, command=save_order_gui).pack(pady=5)

total_label = ttk.Label(root, text="Total: 0.00 PLN", font=("Helvetica", 14, "bold"))
total_label.pack(pady=10)

refresh_product_list()
show_cart()
root.mainloop()