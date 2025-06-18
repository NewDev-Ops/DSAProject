import tkinter as tk
from tkinter import messagebox

inventory = [
    {"name": "Panadol", "quantity": 50, "price": 100, "expiry": "2026-01-01"},
    {"name": "Amoxicillin", "quantity": 30, "price": 150, "expiry": "2025-12-01"},
    {"name": "Diclofenac", "quantity": 20, "price": 80, "expiry": "2025-05-01"}
]
deleted_stack = []

def show_inventory():
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory:")
    for i, med in enumerate(inventory, 1):
        print(f"{i}. {med['name']} | Qty: {med['quantity']} | Price: {med['price']} | Exp: {med['expiry']}")

def delete_medicine(name):
    global inventory, deleted_stack

    for i, med in enumerate(inventory):
        if med["name"].lower() == name.lower():
            deleted_stack.append(med)
            del inventory[i]
            print(f"{name} deleted.")
            return
    print(f"Medicine '{name}' not found.")

def undo_delete():
    global inventory, deleted_stack

    if deleted_stack:
        med = deleted_stack.pop()
        inventory.append(med)
        print(f"{med['name']} restored to inventory.")
    else:
        print("Nothing to undo.")

def menu():
    while True:
        print("\n=== Pharmacy Inventory Menu ===")
        print("1. View Inventory")
        print("2. Delete Medicine")
        print("3. Undo Delete")
        print("4. Exit")

        choice = input("Select option (1-4): ")

        if choice == '1':
            show_inventory()
        elif choice == '2':
            name = input("Enter medicine name to delete: ")
            delete_medicine(name)
        elif choice == '3':
            undo_delete()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Run the menu
menu()
