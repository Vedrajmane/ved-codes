import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import mysql.connector  # Correct

# Function to establish database connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="@Ved727",  # Replace with your MySQL password
            database="cafe_db"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to fetch the selected row and fill the entry fields with order data
def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)

    row_id = listBox.selection()[0]
    select = listBox.item(row_id)['values']
    e1.insert(0, select[0])
    e2.insert(0, select[1])
    e3.insert(0, select[2])
    e4.insert(0, select[3])

# Function to add a new order to the database
def Add():
    order_id = e1.get()
    customer_name = e2.get()
    item = e3.get()
    price = e4.get()

    mysqldb = get_db_connection()
    if not mysqldb:
        return

    mycursor = mysqldb.cursor()

    try:
        sql = "INSERT INTO cafe_orders (order_id, customer_name, item, price) VALUES (%s, %s, %s, %s)"
        val = (order_id, customer_name, item, price)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Order inserted successfully...")
        clear_entries()
    except Exception as e:
        print(e)
        mysqldb.rollback()
        messagebox.showerror("Error", "Failed to insert order.")
    finally:
        mysqldb.close()

# Function to update an existing order in the database
def update():
    order_id = e1.get()
    customer_name = e2.get()
    item = e3.get()
    price = e4.get()

    mysqldb = get_db_connection()
    if not mysqldb:
        return

    mycursor = mysqldb.cursor()

    try:
        sql = "UPDATE cafe_orders SET customer_name = %s, item = %s, price = %s WHERE order_id = %s"
        val = (customer_name, item, price, order_id)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Order updated successfully...")
        clear_entries()
    except Exception as e:
        print(e)
        mysqldb.rollback()
        messagebox.showerror("Error", "Failed to update order.")
    finally:
        mysqldb.close()

# Function to delete an order from the database
def delete():
    order_id = e1.get()

    mysqldb = get_db_connection()
    if not mysqldb:
        return

    mycursor = mysqldb.cursor()

    try:
        sql = "DELETE FROM cafe_orders WHERE order_id = %s"
        val = (order_id,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Order deleted successfully...")
        clear_entries()
    except Exception as e:
        print(e)
        mysqldb.rollback()
        messagebox.showerror("Error", "Failed to delete order.")
    finally:
        mysqldb.close()

# Function to display orders in the Treeview widget
def show():
    mysqldb = get_db_connection()
    if not mysqldb:
        return

    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT order_id, customer_name, item, price FROM cafe_orders")
    records = mycursor.fetchall()

    for row in listBox.get_children():
        listBox.delete(row)

    for record in records:
        listBox.insert("", "end", values=record)

    mysqldb.close()

# Function to refresh the order list displayed in Treeview
def refresh():
    show()

# Function to clear all the entry fields
def clear_entries():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e1.focus_set()

# Create main application window
root = Tk()
root.title("Cafe Database Management")
root.geometry("800x600")  # Adjusted for better layout
root.resizable(False, False)
root.config(bg="#F7F7F7")  # Light background color

# Header Label
tk.Label(root, text="Cafe Order Management", fg="#333", bg="#FF7043", font=("Helvetica", 24, "bold"), padx=10, pady=10).pack(fill=X)

# Frame for Entry Fields and Buttons
frame = Frame(root, bg="#F7F7F7")
frame.pack(pady=20)

# Labels and Entry fields for the cafe order details
tk.Label(frame, text="Order ID", font=("Helvetica", 12), bg="#F7F7F7").grid(row=0, column=0, padx=20, pady=10, sticky="e")
e1 = Entry(frame, font=("Helvetica", 12))
e1.grid(row=0, column=1, padx=20, pady=10)

tk.Label(frame, text="Customer Name", font=("Helvetica", 12), bg="#F7F7F7").grid(row=1, column=0, padx=20, pady=10, sticky="e")
e2 = Entry(frame, font=("Helvetica", 12))
e2.grid(row=1, column=1, padx=20, pady=10)

tk.Label(frame, text="Item", font=("Helvetica", 12), bg="#F7F7F7").grid(row=2, column=0, padx=20, pady=10, sticky="e")
e3 = Entry(frame, font=("Helvetica", 12))
e3.grid(row=2, column=1, padx=20, pady=10)

tk.Label(frame, text="Price", font=("Helvetica", 12), bg="#F7F7F7").grid(row=3, column=0, padx=20, pady=10, sticky="e")
e4 = Entry(frame, font=("Helvetica", 12))
e4.grid(row=3, column=1, padx=20, pady=10)

# Buttons for Add, Update, Delete, and Refresh actions
button_frame = Frame(root, bg="#F7F7F7")
button_frame.pack(pady=20)

Button(button_frame, text="Add", command=Add, height=2, width=15, bg="#FF7043", relief="raised", font=("Helvetica", 12), bd=2).grid(row=0, column=0, padx=10, pady=10)
Button(button_frame, text="Update", command=update, height=2, width=15, bg="#FF7043", relief="raised", font=("Helvetica", 12), bd=2).grid(row=0, column=1, padx=10, pady=10)
Button(button_frame, text="Delete", command=delete, height=2, width=15, bg="#FF7043", relief="raised", font=("Helvetica", 12), bd=2).grid(row=0, column=2, padx=10, pady=10)
Button(button_frame, text="Refresh", command=refresh, height=2, width=15, bg="#FF7043", relief="raised", font=("Helvetica", 12), bd=2).grid(row=0, column=3, padx=10, pady=10)

# Table (Treeview) to display cafe orders
cols = ('Order ID', 'Customer Name', 'Item', 'Price')
listBox = ttk.Treeview(root, columns=cols, show='headings', height=10)

for col in cols:
    listBox.heading(col, text=col, anchor="center")
    listBox.column(col, anchor=CENTER, width=100)
listBox.pack(pady=20)

# Fetch and display orders when the application starts
show()

# Bind double-click to select a row and show it in the entry fields
listBox.bind('<Double-1>', GetValue)

# Run the application
root.mainloop()
