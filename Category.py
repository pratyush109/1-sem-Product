import sqlite3
from tkinter import *
from tkinter import ttk

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x600+100+50")
        self.root.title("Category Management")

      
        self.conn = sqlite3.connect('categories.db')
        self.cursor = self.conn.cursor()
        self.create_table()

       
        self.category_frame = Frame(self.root, width=1070, height=567, bg='white')
        self.category_frame.place(x=200, y=100)
        self.category_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        heading_label = Label(self.category_frame, text='Manage Category Details', 
                              font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
        heading_label.place(x=0, y=0, relwidth=1)

        details_frame = Frame(self.category_frame, bg='white')
        details_frame.place(x=500, y=60)

       
        Label(details_frame, text='ID', font=('times new roman', 14, 'bold'), bg='white').grid(row=0, column=0, padx=20, sticky='w')
        self.id_entry = Entry(details_frame, font=('times new roman', 14), bg='lightyellow')
        self.id_entry.grid(row=0, column=1)

       
        Label(details_frame, text='Category Name', font=('times new roman', 14, 'bold'), bg='white').grid(row=1, column=0, padx=20, sticky='w')
        self.category_name_entry = Entry(details_frame, font=('times new roman', 14), bg='lightyellow')
        self.category_name_entry.grid(row=1, column=1, pady=10)

        
        Label(details_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white').grid(row=2, column=0, padx=20, sticky='w')
        self.description_text = Text(details_frame, width=25, height=6, bd=2, bg='lightyellow')
        self.description_text.grid(row=2, column=1, pady=10)

       
        button_frame = Frame(self.category_frame, bg='white')
        button_frame.place(x=600, y=280)

        self.add_button = Button(button_frame, text='Add', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.add_category)
        self.add_button.grid(row=0, column=0, padx=10)

        self.delete_button = Button(button_frame, text='Delete', font=('times new roman', 14), width=10, cursor='hand2', fg='white', bg='#8f4d7d', command=self.delete_category)
        self.delete_button.grid(row=0, column=1, padx=10)

      
        treeview_frame = Frame(self.category_frame)
        treeview_frame.place(x=530, y=340, height=200, width=500)

        scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
        scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

        self.treeview = ttk.Treeview(treeview_frame, columns=('id', 'name', 'description'), show='headings',
                                     yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrolly.config(command=self.treeview.yview)
        scrollx.config(command=self.treeview.xview)

        self.treeview.pack(fill=BOTH, expand=1)

        self.treeview.heading('id', text='Invoice ID')
        self.treeview.heading('name', text='Category Name')
        self.treeview.heading('description', text='Description')

        self.treeview.column('id', width=80)
        self.treeview.column('name', width=140)
        self.treeview.column('description', width=200)

        self.load_categories()

    def create_table(self):
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT
            )
        ''')
        self.conn.commit()

    def add_category(self):
        
        name = self.category_name_entry.get()
        description = self.description_text.get("1.0", "end-1c")

        if name and description:
            self.cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", (name, description))
            self.conn.commit() 
            self.load_categories() 
            self.clear_entries()

    def delete_category(self):
       
        selected_item = self.treeview.selection()

        if selected_item:
            category_id = self.treeview.item(selected_item, 'values')[0]
            self.cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            self.conn.commit()  
            self.load_categories() 

    def load_categories(self):
       
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        self.cursor.execute("SELECT * FROM categories")
        rows = self.cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)

    def clear_entries(self):
        
        self.id_entry.delete(0, END)
        self.category_name_entry.delete(0, END)
        self.description_text.delete(1.0, END)

    def __del__(self):
       
        self.conn.close()

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
