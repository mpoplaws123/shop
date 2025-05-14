import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

from product import fetch_products, add_product, delete_product, product_in_cart, get_stock
from cart import add_to_cart, clear_cart, get_cart_items
from utils import save_order_to_csv

root = ttk.Window(themename="cyborg")
root.title("Modern Shop GUI")
root.geometry("700x600")

def refresh_product_list():
    product_list.delete(0, tk.END)
    for name, price, stock in fetch_products():
        product_list.insert(tk.END, f"{name} - {price:.2f} PLN (Stock: {stock})")

def add_to_cart_gui():
    selection = product_list.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Select a product.")
        return

    product = product_list.get(selection[0]).split(" - ")[0]
    if not add_to_cart(product):
        messagebox.showwarning("Out of stock", f"{product} is out of stock.")
        return

    refresh_product_list()
    show_cart()

def show_cart():
    cart_list.delete(0, tk.END)
    items = get_cart_items()
    total = 0
    for product, quantity in items:
        price = [p for p in fetch_products() if p[0] == product][0][1]
        subtotal = price * quantity
        total += subtotal
        cart_list.insert(tk.END, f"{product} x{quantity} = {subtotal:.2f} PLN")
    total_label.config(text=f"Total: {total:.2f} PLN")

def clear_cart_gui():
    clear_cart()
    refresh_product_list()
    show_cart()
    messagebox.showinfo("Cart cleared", "Cart has been cleared.")

def save_order_gui():
    if save_order_to_csv():
        messagebox.showinfo("Saved", "Order saved to 'order.csv'")
    else:
        messagebox.showinfo("Empty", "Cart is empty.")

def add_new_product_gui():
    name = simpledialog.askstring("New product", "Enter product name:", parent=root)
    if not name:
        return
    try:
        price = float(simpledialog.askstring("Price", f"Price of {name}:"))
        stock = int(simpledialog.askstring("Stock", f"Stock of {name}:"))
        add_product(name, price, stock)
        refresh_product_list()
    except:
        messagebox.showerror("Invalid", "Price or stock not valid.")

def delete_product_gui():
    selection = product_list.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Select a product to delete.")
        return

    product = product_list.get(selection[0]).split(" - ")[0]
    if product_in_cart(product):
        messagebox.showwarning("In cart", "Cannot delete a product in cart.")
        return

    delete_product(product)
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
