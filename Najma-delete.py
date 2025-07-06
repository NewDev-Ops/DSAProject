import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Stack for undo
deleted_stack = []

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="medicines"
    )

# Get all medicine entries from database
def get_inventory():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Name, Quantity, Price, Expiry FROM meddata")
    rows = cur.fetchall()
    conn.close()
    return rows

# Delete medicine by name
def delete_medicine():
    name = entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a medicine name.")
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Check if medicine exists
        cur.execute("SELECT Name, Quantity, Price, Expiry FROM meddata WHERE Name = %s", (name,))
        result = cur.fetchone()

        if result:
            deleted_stack.append(result)  # Save for undo
            cur.execute("DELETE FROM meddata WHERE Name = %s", (name,))
            conn.commit()
            messagebox.showinfo("Deleted", f"{name} deleted from DB.")
        else:
            messagebox.showerror("Error", f"Medicine '{name}' not found.")
        conn.close()
        update_listbox()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Undo last deleted medicine
def undo_delete():
    if deleted_stack:
        name, qty, price, expiry = deleted_stack.pop()
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO meddata (Name, Quantity, Price, Expiry) VALUES (%s, %s, %s, %s)",
                (name, qty, price, expiry)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Undo", f"{name} restored.")
            update_listbox()
        except Exception as e:
            messagebox.showerror("Undo Error", str(e))
    else:
        messagebox.showinfo("Undo", "Nothing to undo.")

# Update the listbox with current medicine list
def update_listbox():
    listbox.delete(0, tk.END)
    for med in get_inventory():
        display = f"{med[0]}: Qty={med[1]}, Price={med[2]}, Exp={med[3]}"
        listbox.insert(tk.END, display)

# GUI 
root = tk.Tk()
root.title("Pharmacy Inventory - Delete (MySQL)")
root.geometry("500x400")

tk.Label(root, text="Enter Medicine Name to Delete:").pack(pady=5)
entry = tk.Entry(root)
entry.pack()

tk.Button(root, text="Delete", command=delete_medicine).pack(pady=5)
tk.Button(root, text="Undo Delete", command=undo_delete).pack(pady=5)

listbox = tk.Listbox(root, width=60)
listbox.pack(pady=10)

update_listbox()
root.mainloop()

    
       
