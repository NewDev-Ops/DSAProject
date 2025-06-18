import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# -------------------- Theme Setup --------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# -------------------- Main Window --------------------
app = ctk.CTk()
app.title("Pharmacy Inventory Management System")

# Apply full-screen dimensions
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}+0+0")

# -------------------- Title Frame --------------------
title_frame = ctk.CTkFrame(app, fg_color="white")
title_frame.pack(side="top", fill="x")

title_label = ctk.CTkLabel(
    title_frame,
    text="PHARMACY INVENTORY SYSTEM",
    font=ctk.CTkFont("Arial", size=35, weight="bold"),
    text_color="blue"
)
title_label.pack(pady=20)

# -------------------- Form Frame --------------------
form_frame = ctk.CTkFrame(app)
form_frame.pack(pady=10, padx=30, fill="x")

fields = [
    ("Name", 0),
    ("Quantity", 1),
    ("Price", 2),
    ("Expiry Date", 3)
]

entries = {}

for field, row in fields:
    lbl = ctk.CTkLabel(
        form_frame,
        text=field + ":",
        font=ctk.CTkFont("Arial", 15, "bold")
    )
    lbl.grid(row=row, column=0, sticky="w", pady=5, padx=10)

    ent = ctk.CTkEntry(
        form_frame,
        font=ctk.CTkFont("Arial", 14),
        width=300
    )
    ent.grid(row=row, column=1, pady=5, padx=10)
    entries[field] = ent

# -------------------- Button Frame --------------------
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

buttons = ["ADD DATA", "SHOW DATA", "UPDATE", "DELETE", "RESET", "EXIT"]
for btn_text in buttons:
    btn = ctk.CTkButton(
        button_frame,
        text=btn_text,
        width=130,
        font=ctk.CTkFont("Arial", 15, "bold")
    )
    btn.pack(side="left", padx=10)

# -------------------- Table Frame --------------------
table_frame = ctk.CTkFrame(app)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
scroll_y = ttk.Scrollbar(table_frame, orient="vertical")

product_table = ttk.Treeview(
    table_frame,
    columns=("name", "qty", "price", "expiry"),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
scroll_x.config(command=product_table.xview)
scroll_y.config(command=product_table.yview)

# Table Headings
product_table.heading("name", text="Name")
product_table.heading("qty", text="Quantity")
product_table.heading("price", text="Price")
product_table.heading("expiry", text="Expiry Date")
product_table['show'] = 'headings'

# Column widths
product_table.column("name", width=250)
product_table.column("qty", width=120)
product_table.column("price", width=120)
product_table.column("expiry", width=180)

product_table.pack(fill="both", expand=True)

# -------------------- Table Font Styling --------------------
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 15, "bold"))
style.configure("Treeview", font=("Arial", 14))

# -------------------- Launch --------------------
app.mainloop()
