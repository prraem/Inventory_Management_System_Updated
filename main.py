import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import json
import os

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class InventoryItem:
    def __init__(self, product_id, name, quantity, price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price
        }

class InventoryManagementSystem:
    def __init__(self):
        self.users = self.load_users()
        self.inventory = self.load_inventory()
        self.current_user = None

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                users_data = json.load(file)
                return [User(**user) for user in users_data]
        return []

    def load_inventory(self):
        if os.path.exists("inventory.json"):
            with open("inventory.json", "r") as file:
                inventory_data = json.load(file)
                return {item['product_id']: InventoryItem(**item) for item in inventory_data}
        return {}

    def save_inventory(self):
        with open("inventory.json", "w") as file:
            json.dump([item.to_dict() for item in self.inventory.values()], file)

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                return True
        return False

    def add_item(self, product_id, name, quantity, price):
        if product_id in self.inventory:
            return False
        self.inventory[product_id] = InventoryItem(product_id, name, quantity, price)
        self.save_inventory()
        return True

    def edit_item(self, product_id, name, quantity, price):
        if product_id in self.inventory:
            self.inventory[product_id] = InventoryItem(product_id, name, quantity, price)
            self.save_inventory()
            return True
        return False

    def delete_item(self, product_id):
        if product_id in self.inventory:
            del self.inventory[product_id]
            self.save_inventory()
            return True
        return False

class IMSInterface:
    def __init__(self, ims):
        self.ims = ims
        self.root = ThemedTk(theme="arc")
        self.root.title("Inventory Management System")
        self.root.geometry("900x700")

        # Configure style
        self.style = ttk.Style(self.root)
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14))
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 14, 'bold'))

        self.create_login_screen()
        self.root.mainloop()

    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30 30 30 30")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Login", font=("Helvetica", 18, 'bold')).grid(row=0, column=1, pady=20)
        ttk.Label(frame, text="Username").grid(row=1, column=0, pady=5, sticky=tk.E)
        username_entry = ttk.Entry(frame, width=25)
        username_entry.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Password").grid(row=2, column=0, pady=5, sticky=tk.E)
        password_entry = ttk.Entry(frame, show="*", width=25)
        password_entry.grid(row=2, column=1, pady=5)
        ttk.Button(frame, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get())).grid(row=3, column=1, pady=10)
        
    def login(self, username, password):
        if self.ims.authenticate(username, password):
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30 30 30 30")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Main Menu", font=("Helvetica", 18, 'bold')).grid(row=0, column=1, pady=20)
        ttk.Button(frame, text="Add Product", command=self.create_add_product_screen).grid(row=1, column=1, pady=10)
        ttk.Button(frame, text="Edit Product", command=self.create_edit_product_screen).grid(row=2, column=1, pady=10)
        ttk.Button(frame, text="Delete Product", command=self.create_delete_product_screen).grid(row=3, column=1, pady=10)
        ttk.Button(frame, text="View Inventory", command=self.create_view_inventory_screen).grid(row=4, column=1, pady=10)
        ttk.Button(frame, text="Generate Reports", command=self.create_reports_screen).grid(row=5, column=1, pady=10)
        ttk.Button(frame, text="Logout", command=self.create_login_screen).grid(row=6, column=1, pady=10)

    def create_add_product_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30 30 30 30")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Add Product", font=("Helvetica", 18, 'bold')).grid(row=0, column=1, pady=20)
        ttk.Label(frame, text="Product ID").grid(row=1, column=0, pady=5, sticky=tk.E)
        product_id_entry = ttk.Entry(frame, width=25)
        product_id_entry.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Name").grid(row=2, column=0, pady=5, sticky=tk.E)
        name_entry = ttk.Entry(frame, width=25)
        name_entry.grid(row=2, column=1, pady=5)
        ttk.Label(frame, text="Quantity").grid(row=3, column=0, pady=5, sticky=tk.E)
        quantity_entry = ttk.Entry(frame, width=25)
        quantity_entry.grid(row=3, column=1, pady=5)
        ttk.Label(frame, text="Price").grid(row=4, column=0, pady=5, sticky=tk.E)
        price_entry = ttk.Entry(frame, width=25)
        price_entry.grid(row=4, column=1, pady=5)
        ttk.Button(frame, text="Add", command=lambda: self.add_product(product_id_entry.get(), name_entry.get(), quantity_entry.get(), price_entry.get())).grid(row=5, column=1, pady=10)
        ttk.Button(frame, text="Back", command=self.create_main_menu).grid(row=6, column=1, pady=10)

    def add_product(self, product_id, name, quantity, price):
        try:
            quantity = int(quantity)
            price = float(price)
            if self.ims.add_item(product_id, name, quantity, price):
                messagebox.showinfo("Success", "Product added successfully.")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Product ID already exists.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price.")

    def create_edit_product_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30 30 30 30")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Edit Product", font=("Helvetica", 18, 'bold')).grid(row=0, column=1, pady=20)
        ttk.Label(frame, text="Product ID").grid(row=1, column=0, pady=5, sticky=tk.E)
        product_id_entry = ttk.Entry(frame, width=25)
        product_id_entry.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Name").grid(row=2, column=0, pady=5, sticky=tk.E)
        name_entry = ttk.Entry(frame, width=25)
        name_entry.grid(row=2, column=1, pady=5)
        ttk.Label(frame, text="Quantity").grid(row=3, column=0, pady=5, sticky=tk.E)
        quantity_entry = ttk.Entry(frame, width=25)
        quantity_entry.grid(row=3, column=1, pady=5)
        ttk.Label(frame, text="Price").grid(row=4, column=0, pady=5, sticky=tk.E)
        price_entry = ttk.Entry(frame, width=25)
        price_entry.grid(row=4, column=1, pady=5)
        ttk.Button(frame, text="Edit", command=lambda: self.edit_product(product_id_entry.get(), name_entry.get(), quantity_entry.get(), price_entry.get())).grid(row=5, column=1, pady=10)
        ttk.Button(frame, text="Back", command=self.create_main_menu).grid(row=6, column=1, pady=10)

    def edit_product(self, product_id, name, quantity, price):
        try:
            quantity = int(quantity)
            price = float(price)
            if self.ims.edit_item(product_id, name, quantity, price):
                messagebox.showinfo("Success", "Product edited successfully.")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Product ID does not exist.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price.")

    def create_delete_product_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30 30 30 30")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Delete Product", font=("Helvetica", 18, 'bold')).grid(row=0, column=1, pady=20)
        ttk.Label(frame, text="Product ID").grid(row=1, column=0, pady=5, sticky=tk.E)
        product_id_entry = ttk.Entry(frame, width=25)
        product_id_entry.grid(row=1, column=1, pady=5)
        ttk.Button(frame, text="Delete", command=lambda: self.delete_product(product_id_entry.get())).grid(row=2, column=1, pady=10)
        ttk.Button(frame, text="Back", command=self.create_main_menu).grid(row=3, column=1, pady=10)

    def delete_product(self, product_id):
        if self.ims.delete_item(product_id):
            messagebox.showinfo("Success", "Product deleted successfully.")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Product ID does not exist.")

    def create_view_inventory_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Inventory", font=("Helvetica", 18, 'bold')).pack(pady=20)
        tree = ttk.Treeview(self.root, columns=("Product ID", "Name", "Quantity", "Price"), show="headings")
        tree.heading("Product ID", text="Product ID")
        tree.heading("Name", text="Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Price", text="Price")
        tree.pack(pady=10)

        for item in self.ims.inventory.values():
            tree.insert("", tk.END, values=(item.product_id, item.name, item.quantity, item.price))

        ttk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def create_reports_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="30 30 30 30")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Reports", font=("Helvetica", 18, 'bold')).grid(row=0, column=1, pady=20)
        low_stock_items = [item for item in self.ims.inventory.values() if item.quantity < 5]

        if low_stock_items:
            ttk.Label(frame, text="Low Stock Items", font=("Helvetica", 14)).grid(row=1, column=1, pady=10)
            tree = ttk.Treeview(frame, columns=("Product ID", "Name", "Quantity"), show="headings")
            tree.heading("Product ID", text="Product ID")
            tree.heading("Name", text="Name")
            tree.heading("Quantity", text="Quantity")
            tree.grid(row=2, column=1, pady=10)

            for item in low_stock_items:
                tree.insert("", tk.END, values=(item.product_id, item.name, item.quantity))

        ttk.Button(frame, text="Back", command=self.create_main_menu).grid(row=3, column=1, pady=10)

if __name__ == "__main__":
    ims = InventoryManagementSystem()
    IMSInterface(ims)
