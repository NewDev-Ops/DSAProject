import tkinter as tk
from tkinter import messagebox
import sqlite3

# Stack for undo
deleted_stack = []



def get_inventory():
    conn = sqlite3.connect('pharmacy.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM medicines")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_medicine():
    name = entry.get()
    conn = sqlite3.connect('pharmacy.db')
    cur = conn.cursor()

    # Save deleted for undo
    cur.execute("SELECT * FROM medicines WHERE name = ?", (name,))
    result = cur.fetchone()
    if result:
        deleted_stack.append(result)
        cur.execute("DELETE FROM medicines WHERE name = ?", (name,))
        conn.commit()
        messagebox.showinfo("Deleted", f"{name} deleted from DB.")
    else:
        messagebox.showerror("Error", "Medicine not found.")
    conn.close()
    update_listbox()


def undo_delete():
    if deleted_stack:
        med = deleted_stack.pop()
        conn = sqlite3.connect('pharmacy.db')
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO medicines VALUES (?, ?, ?, ?)", med)
        conn.commit()
        conn.close()
        messagebox.showinfo("Undo", f"{med[0]} restored.")
        update_listbox()
    else:
        messagebox.showinfo("Undo", "Nothing to undo.")


def update_listbox():
    listbox.delete(0, tk.END)
    for med in get_inventory():
        display = f"{med[0]}: Qty={med[1]}, Price={med[2]}, Exp={med[3]}"
        listbox.insert(tk.END, display)


# GUI
root = tk.Tk()
root.title("Pharmacy Inventory - Delete (with DB)")

tk.Label(root,  text="Enter Medicine Name to Delete:").pack()
entry = tk.Entry(root)
entry.pack()

tk.Button(root, text="Delete", command=delete_medicine).pack(pady=5)
tk.Button(root, text="Undo Delete", command=undo_delete).pack(pady=5)

listbox = tk.Listbox(root, width=60)
listbox.pack(pady=10)

update_listbox()

root.mainloop()

    
