import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x600+100+50")
        self.root.title("Supplier Management")
        self.root.configure(bg='white')
        
        self.create_database()
        self.create_widgets()

    def create_database(self):
        # Connect to SQLite database (or create one if it doesn't exist)
        self.conn = sqlite3.connect("supplier.db")
        self.cursor = self.conn.cursor()
        
        # Create a table for suppliers if it doesn't already exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                                invoice INTEGER PRIMARY KEY,
                                name TEXT,
                                contact TEXT,
                                description TEXT)''')
        self.conn.commit()

    def create_widgets(self):
        supplier_frame = Frame(self.root, width=1070, height=567, bg='white', relief=RIDGE, bd=2)
        supplier_frame.place(x=200, y=100)
        supplier_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        heading_label = Label(supplier_frame, text='Manage Supplier Details',
                              font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
        heading_label.place(x=0, y=0, relwidth=1)
        
        left_frame = Frame(supplier_frame, bg='white')
        left_frame.place(x=10, y=50)
        
        Label(left_frame, text='Invoice No.', font=('times new roman', 14, 'bold'), bg='white').grid(row=0, column=0, padx=(20, 40), sticky='w')
        self.invoice_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
        self.invoice_entry.grid(row=0, column=1)
        
        Label(left_frame, text='Supplier Name', font=('times new roman', 14, 'bold'), bg='white').grid(row=1, column=0, padx=(20, 40), pady=10, sticky='w')
        self.name_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
        self.name_entry.grid(row=1, column=1)
        
        Label(left_frame, text='Supplier Contact', font=('times new roman', 14, 'bold'), bg='white').grid(row=2, column=0, padx=(20, 40), sticky='w')
        self.contact_entry = Entry(left_frame, font=('times new roman', 14), bg='lightyellow')
        self.contact_entry.grid(row=2, column=1)
        
        Label(left_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white').grid(row=3, column=0, padx=(20, 40), sticky='nw', pady=10)
        self.description_text = Text(left_frame, width=25, height=5, bd=2, bg='lightyellow')
        self.description_text.grid(row=3, column=1, pady=10)
        
        button_frame = Frame(left_frame, bg='white')
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        Button(button_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.add_supplier).grid(row=0, column=0, padx=10)
        Button(button_frame, text='Update', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#2d7d0f', command=self.update_supplier).grid(row=0, column=1, padx=10)
        Button(button_frame, text='Delete', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#7d0f0f', command=self.delete_supplier).grid(row=0, column=2, padx=10)
        Button(button_frame, text='Clear', font=('times new roman', 14), width=10, cursor='hand2', fg='black', bg='#d4d4d4', command=self.clear_entries).grid(row=0, column=3, padx=10)
        
        right_frame = Frame(supplier_frame, bg='white')
        right_frame.place(x=520, y=50, width=500, height=400)
        
        search_frame = Frame(right_frame, bg='white')
        search_frame.pack(pady=10)
        
        Label(search_frame, text='Invoice No.', font=('times new roman', 14, 'bold'), bg='white').grid(row=0, column=0, padx=10, sticky='w')
        self.search_entry = Entry(search_frame, font=('times new roman', 14), bg='lightyellow', width=10)
        self.search_entry.grid(row=0, column=1)
        
        Button(search_frame, text='Search', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#d4d4d4', command=self.search_supplier).grid(row=0, column=2, padx=10)
        Button(search_frame, text='Show All', font=('times new roman', 14), width=8, cursor='hand2', fg='black', bg='#d4d4d4', command=self.show_all_suppliers).grid(row=0, column=3)
        
        scrolly = Scrollbar(right_frame, orient=VERTICAL)
        scrollx = Scrollbar(right_frame, orient=HORIZONTAL)
        
        self.treeview = ttk.Treeview(right_frame, columns=('invoice', 'name', 'contact', 'description'), show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.config(command=self.treeview.yview)
        scrollx.config(command=self.treeview.xview)
        
        self.treeview.pack(fill=BOTH, expand=1)
        
        self.treeview.heading('invoice', text='Invoice Id')
        self.treeview.heading('name', text='Supplier Name')
        self.treeview.heading('contact', text='Supplier Contact')
        self.treeview.heading('description', text='Description')
        
        self.treeview.column('invoice', width=80)
        self.treeview.column('name', width=140)
        self.treeview.column('contact', width=120)
        self.treeview.column('description', width=300)

    def add_supplier(self):
        invoice = self.invoice_entry.get()
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        description = self.description_text.get("1.0", END)
        
        if invoice == '' or name == '' or contact == '' or description == '':
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Insert supplier into the database
        self.cursor.execute("INSERT INTO suppliers (invoice, name, contact, description) VALUES (?, ?, ?, ?)",
                            (invoice, name, contact, description))
        self.conn.commit()
        messagebox.showinfo("Success", "Supplier added successfully!")
        self.clear_entries()
        self.show_all_suppliers()

    def update_supplier(self):
        invoice = self.invoice_entry.get()
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        description = self.description_text.get("1.0", END)
        
        if invoice == '' or name == '' or contact == '' or description == '':
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Update supplier in the database
        self.cursor.execute("UPDATE suppliers SET name=?, contact=?, description=? WHERE invoice=?",
                            (name, contact, description, invoice))
        self.conn.commit()
        messagebox.showinfo("Success", "Supplier updated successfully!")
        self.clear_entries()
        self.show_all_suppliers()

    def delete_supplier(self):
        invoice = self.invoice_entry.get()
        
        if invoice == '':
            messagebox.showerror("Error", "Invoice number is required!")
            return
        
        # Delete supplier from the database
        self.cursor.execute("DELETE FROM suppliers WHERE invoice=?", (invoice,))
        self.conn.commit()
        messagebox.showinfo("Success", "Supplier deleted successfully!")
        self.clear_entries()
        self.show_all_suppliers()

    def search_supplier(self):
        invoice = self.search_entry.get()
        
        if invoice == '':
            messagebox.showerror("Error", "Invoice number is required!")
            return
        
        # Search supplier in the database
        self.cursor.execute("SELECT * FROM suppliers WHERE invoice=?", (invoice,))
        result = self.cursor.fetchone()
        
        if result:
            self.clear_entries()
            self.invoice_entry.insert(0, result[0])
            self.name_entry.insert(0, result[1])
            self.contact_entry.insert(0, result[2])
            self.description_text.insert(END, result[3])
        else:
            messagebox.showerror("Error", "Supplier not found!")

    def show_all_suppliers(self):
        # Fetch all suppliers from the database
        self.cursor.execute("SELECT * FROM suppliers")
        rows = self.cursor.fetchall()
        
        # Clear the existing data in the treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        
        # Populate the treeview with the data from the database
        for row in rows:
            self.treeview.insert('', END, values=row)

    def clear_entries(self):
        self.invoice_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.description_text.delete("1.0", END)
        self.search_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()
