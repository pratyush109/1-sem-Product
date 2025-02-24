from tkinter import *
from tkinter import ttk
import sqlite3

class ProductClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Management")
        self.root.geometry("1200x600+100+50")
        
        self.create_database()
        
        self.product_frame = Frame(self.root, width=1070, height=567, bg='white')
        self.product_frame.place(x=0, y=0)
        self.product_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.left_frame = Frame(self.product_frame, bg='white', bd=2, relief=RIDGE)
        self.left_frame.place(x=20, y=30, width=400, height=500)

        heading_label = Label(self.product_frame, text='Manage Product Details', 
                              font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
        heading_label.place(x=20, y=0, width=400, height=30)

        
        category_label = Label(self.left_frame, text='Category:', font=('times new roman', 14, 'bold'), bg='white') 
        category_label.grid(row=0, column=0, padx=20, pady=5, sticky='w')
        self.category_combobox = ttk.Combobox(self.left_frame, font=('times new roman', 14, 'bold'), width=18, state='readonly')
        self.category_combobox.grid(row=0, column=1, pady=5)
        self.category_combobox.set('Select Category')

        supplier_label = Label(self.left_frame, text='Supplier:', font=('times new roman', 14, 'bold'), bg='white') 
        supplier_label.grid(row=1, column=0, padx=20, pady=5, sticky='w')
        self.supplier_combobox = ttk.Combobox(self.left_frame, font=('times new roman', 14, 'bold'), width=18, state='readonly')
        self.supplier_combobox.grid(row=1, column=1, pady=5)
        self.supplier_combobox.set('Select Supplier')

        name_label = Label(self.left_frame, text='Name:', font=('times new roman', 14, 'bold'), bg='white') 
        name_label.grid(row=2, column=0, padx=20, pady=5, sticky='w')
        self.name_entry = Entry(self.left_frame, font=('times new roman', 14), bg='lightyellow') 
        self.name_entry.grid(row=2, column=1, pady=5)

        price_label = Label(self.left_frame, text='Price:', font=('times new roman', 14, 'bold'), bg='white') 
        price_label.grid(row=3, column=0, padx=20, pady=5, sticky='w')
        self.price_entry = Entry(self.left_frame, font=('times new roman', 14), bg='lightyellow') 
        self.price_entry.grid(row=3, column=1, pady=5)

        quantity_label = Label(self.left_frame, text='Quantity:', font=('times new roman', 14, 'bold'), bg='white') 
        quantity_label.grid(row=4, column=0, padx=20, pady=5, sticky='w')
        self.quantity_entry = Entry(self.left_frame, font=('times new roman', 14), bg='lightyellow') 
        self.quantity_entry.grid(row=4, column=1, pady=5)

        status_label = Label(self.left_frame, text='Status:', font=('times new roman', 14, 'bold'), bg='white') 
        status_label.grid(row=5, column=0, padx=20, pady=5, sticky='w')
        self.status_combobox = ttk.Combobox(self.left_frame, values=('Active', 'Inactive'), font=('times new roman', 14, 'bold'), width=18, state='readonly')
        self.status_combobox.grid(row=5, column=1, pady=5)
        self.status_combobox.set('Select Status')

        
        button_frame = Frame(self.left_frame, bg='white')
        button_frame.grid(row=6, columnspan=2, pady=10)

        Button(button_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.add_product).grid(row=0, column=0, padx=5)
        Button(button_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.update_product).grid(row=0, column=1, padx=5)
        Button(button_frame, text='Delete', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.delete_product).grid(row=0, column=2, padx=5)

        
        search_frame = LabelFrame(self.product_frame, text='Search Product', font=('times new roman', 14), bg='white')
        search_frame.place(x=480, y=50, width=602, height=60)

        self.search_combobox = ttk.Combobox(search_frame, values=('Category', 'Supplier', 'Name', 'Status'), state='readonly', width=16, font=('times new roman', 14))
        self.search_combobox.grid(row=0, column=0, padx=10, pady=5)

        self.search_entry = Entry(search_frame, font=('times new roman', 14), bg='lightyellow', width=16) 
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        Button(search_frame, text='Search', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.search_product).grid(row=0, column=2, padx=5)
        Button(search_frame, text='Show All', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.show_all_products).grid(row=0, column=3, padx=5)

        
        treeview_frame = Frame(self.product_frame, bg='white')
        treeview_frame.place(x=480, y=125, width=570, height=430)

        scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
        scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

        self.treeview = ttk.Treeview(treeview_frame, columns=('category', 'supplier', 'name', 'price', 'quantity', 'status'),
                                    show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrolly.config(command=self.treeview.yview)
        scrollx.config(command=self.treeview.xview)

        for col in ('category', 'supplier', 'name', 'price', 'quantity', 'status'):
            self.treeview.heading(col, text=col.capitalize())
            self.treeview.column(col, width=100)

        self.treeview.pack(fill=BOTH, expand=1)
        
        self.show_all_products()

    def create_database(self):
        conn = sqlite3.connect('product_db.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            category TEXT,
                            supplier TEXT,
                            name TEXT,
                            price REAL,
                            quantity INTEGER,
                            status TEXT)''')
        conn.commit()
        conn.close()
        
    def add_product(self):
        category = self.category_combobox.get()
        supplier = self.supplier_combobox.get()
        name = self.name_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        status = self.status_combobox.get()

        if category and supplier and name and price and quantity and status:
            self.insert_product_into_db(category, supplier, name, float(price), int(quantity), status)
            self.show_all_products()
            self.clear_entries()
        else:
            print("All fields are required!")

    def insert_product_into_db(self, category, supplier, name, price, quantity, status):
        conn = sqlite3.connect('product_db.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO products (category, supplier, name, price, quantity, status)
                          VALUES (?, ?, ?, ?, ?, ?)''', (category, supplier, name, price, quantity, status))
        conn.commit()
        conn.close()

    def update_product(self):
        selected_item = self.treeview.selection()
        if selected_item:
            product_id = self.treeview.item(selected_item, 'values')[0]
            category = self.category_combobox.get()
            supplier = self.supplier_combobox.get()
            name = self.name_entry.get()
            price = self.price_entry.get()
            quantity = self.quantity_entry.get()
            status = self.status_combobox.get()

            if category and supplier and name and price and quantity and status:
                self.update_product_in_db(product_id, category, supplier, name, float(price), int(quantity), status)
                self.show_all_products()
                self.clear_entries()
            else:
                print("All fields are required!")

    def update_product_in_db(self, product_id, category, supplier, name, price, quantity, status):
        conn = sqlite3.connect('product_db.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE products SET category=?, supplier=?, name=?, price=?, quantity=?, status=? WHERE id=?''', 
                       (category, supplier, name, price, quantity, status, product_id))
        conn.commit()
        conn.close()

    def delete_product(self):
        selected_item = self.treeview.selection()
        if selected_item:
            product_id = self.treeview.item(selected_item, 'values')[0]
            self.delete_product_from_db(product_id)
            self.show_all_products()

    def delete_product_from_db(self, product_id):
        conn = sqlite3.connect('product_db.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()
        conn.close()

    def show_all_products(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        
        products = self.fetch_all_products()
        for product in products:
            self.treeview.insert('', 'end', values=product[1:])

    def fetch_all_products(self):
        conn = sqlite3.connect('product_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def search_product(self):
        column = self.search_combobox.get().lower()
        value = self.search_entry.get()
        
        if column and value:
            products = self.search_products_by(column, value)
            for row in self.treeview.get_children():
                self.treeview.delete(row)
            for product in products:
                self.treeview.insert('', 'end', values=product[1:])
        else:
            print("Please provide both search criteria.")
    
    def search_products_by(self, column, value):
        conn = sqlite3.connect('product_db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM products WHERE {column} LIKE ?", ('%' + value + '%',))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def clear_entries(self):
        self.category_combobox.set('Select Category')
        self.supplier_combobox.set('Select Supplier')
        self.name_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.status_combobox.set('Select Status')


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop() 