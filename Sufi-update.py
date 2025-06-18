import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='medicines'
)

# Linked List Node
class MedicineNode:
    def __init__(self, name, quantity, price, expiry):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.expiry = expiry
        self.next = None

# Linked List
class MedicineLinkedList:
    def __init__(self):
        self.head = None

    def load_from_database(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meddata")
        results = cursor.fetchall()
        cursor.close()

        for name, quantity, price, expiry in results:
            self.append(name, quantity, price, expiry)

    def append(self, name, quantity, price, expiry):
        new_node = MedicineNode(name, quantity, price, expiry)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def update_node(self, name, quantity, price, expiry):
        current = self.head
        while current:
            if current.name == name:
                current.quantity = quantity
                current.price = price
                current.expiry = expiry
                return True  # Found and updated
            current = current.next
        return False  # Not found

    def update_database(self, name, quantity, price, expiry):
        cursor = conn.cursor()
        sql = "UPDATE meddata SET Quantity = %s, Price = %s, Expiry = %s WHERE Name = %s"
        cursor.execute(sql, (quantity, price, expiry, name))
        conn.commit()
        cursor.close()

# Create the linked list and load data
medicine_list = MedicineLinkedList()
medicine_list.load_from_database()

# Tkinter GUI
root = tk.Tk()
root.title("Update Medicine")
root.geometry("400x300")

# Entry Fields
tk.Label(root, text="Medicine Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="New Quantity").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

tk.Label(root, text="New Price").pack()
price_entry = tk.Entry(root)
price_entry.pack()

tk.Label(root, text="New Expiry (YYYY-MM-DD)").pack()
expiry_entry = tk.Entry(root)
expiry_entry.pack()

def update_medicine():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    expiry = expiry_entry.get()

    if not (name and quantity and price and expiry):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    # Try to update in Linked List
    success = medicine_list.update_node(name, quantity, price, expiry)

    if success:
        # If successful, update the database
        try:
            medicine_list.update_database(name, quantity, price, expiry)
            messagebox.showinfo("Success", "Medicine updated successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating DB: {e}")
    else:
        messagebox.showerror("Not Found", f"Medicine '{name}' not found in records.")

tk.Button(root, text="Update", command=update_medicine).pack(pady=10)

root.mainloop()
