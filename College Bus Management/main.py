import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *

def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e5.delete(0, END)
    e4.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.item(row_id)
    e1.insert(0, select['values'][0])  # Reg No
    e2.insert(0, select['values'][1])  # Student Name
    e3.insert(0, select['values'][2])  # Mobile
    e4.insert(0, select['values'][3])  # Email
    e5.insert(0, select['values'][4])  # Fee

def Add():
    Reg_id = e1.get()
    studname = e2.get()
    Mobile = e3.get()
    email = e4.get()
    feee = e5.get()

    mysqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Ved727",
        database="registation")
    mycursor = mysqldb.cursor()

    try:
        sql = "INSERT INTO student (id, sname, mob, email, fee) VALUES (%s, %s, %s, %s, %s)"
        val = (Reg_id, studname, Mobile, email, feee)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Student inserted successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e1.focus_set()
    except Exception as e:
        print(e)
        mysqldb.rollback()
    finally:
        mysqldb.close()

def update():
    studid = e1.get()
    sname = e2.get()
    mob = e3.get()
    email = e4.get()
    feee = e5.get()

    mysqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Ved727",
        database="registation")
    mycursor = mysqldb.cursor()

    try:
        sql = "UPDATE student SET sname=%s, mob=%s, fee=%s, email=%s WHERE id=%s"
        val = (sname, mob, feee, email, studid)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Record updated successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e1.focus_set()
    except Exception as e:
        print(e)
        mysqldb.rollback()
    finally:
        mysqldb.close()

def delete():
    studid = e1.get()

    mysqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Ved727",
        database="registation")
    mycursor = mysqldb.cursor()

    try:
        sql = "DELETE FROM student WHERE id=%s"
        val = (studid,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Record deleted successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e1.focus_set()
    except Exception as e:
        print(e)
        mysqldb.rollback()
    finally:
        mysqldb.close()

def show():
    global records
    mysqldb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Ved727",
        database="registation")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT id, sname, mob, email, fee FROM student")
    records = mycursor.fetchall()
    for row in listBox.get_children():
        listBox.delete(row)

    for record in records:
        listBox.insert("", "end", values=record)
    mysqldb.close()

def refresh():
    show()

root = Tk()
root.title("Bus Registration")
root.geometry("825x500")
root.resizable(False, False)

global e1, e2, e3, e4, e5

tk.Label(root, text="Bus Registration", fg="white", background="black", font=("courier", 25, "bold"), border=10).place(x=370, y=45)

tk.Label(root, text="Reg ID").place(x=40, y=10)
Label(root, text="Student Name").place(x=40, y=40)
Label(root, text="Mobile").place(x=40, y=70)
Label(root, text="Email").place(x=40, y=100)
Label(root, text="Fee").place(x=40, y=130)

e1 = Entry(root)
e1.place(x=150, y=10)

e2 = Entry(root)
e2.place(x=150, y=40)

e3 = Entry(root)
e3.place(x=150, y=70)

e4 = Entry(root)
e4.place(x=150, y=100)

e5 = Entry(root)
e5.place(x=150, y=130)

Button(root, text="Add", command=Add, height=3, width=13).place(x=30, y=160)
Button(root, text="Update", command=update, height=3, width=13).place(x=140, y=160)
Button(root, text="Delete", command=delete, height=3, width=13).place(x=250, y=160)
Button(root, text="Refresh", command=refresh, height=3, width=13).place(x=360, y=160)

cols = ('Reg No', 'Student Name', 'Mobile', 'Email', 'Fee')
listBox = ttk.Treeview(root, columns=cols, show='headings',)

for col in cols:
    listBox.heading(col, text=col, anchor="center")
    listBox.column(col, anchor=CENTER, width=160)

listBox.place(x=10, y=230)

show()

listBox.bind('<Double-1>', GetValue)

root.mainloop()
