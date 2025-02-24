from tkinter import *
import time
from employee import employeeClass 
from Supplier import SupplierClass  
from Product import ProductClass  
from Category import categoryClass  

class management:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Stock Sage")
        self.root.config(bg="#ADD8E6")

        title = Label(self.root, text="Stock Sage", font=("Times new roman", 40, "bold"), bg="darkblue", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        btn_logout = Button(self.root, text="Logout", font=("Times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2", command=self.root.quit)
        btn_logout.place(x=1100, y=10)

        self.lbl_clock = Label(self.root, font=("Times new roman", 15, "bold"), bg="darkblue", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_time()

        LeftMenu = Frame(self.root, bd=3, relief=RIDGE, bg="#87CEFA")
        LeftMenu.place(x=0, y=102, width=200, height=320)

        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="White")
        lbl_menu.pack(side=TOP, fill=X)

        btn_employee = Button(LeftMenu, text="Employee", command=self.open_employee_window, font=("times new roman", 20, "bold"), bg="red", bd=3, cursor="hand2")
        btn_employee.pack(side=TOP, fill=X)

        btn_supplier = Button(LeftMenu, text="Supplier", command=self.open_supplier_window, font=("times new roman", 20, "bold"), bg="green", bd=3, cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X)

        btn_category = Button(LeftMenu, text="Category", command=self.open_category_window, font=("times new roman", 20, "bold"), bg="yellow", bd=3, cursor="hand2")
        btn_category.pack(side=TOP, fill=X)

        btn_product = Button(LeftMenu, text="Product", command=self.open_product_window, font=("times new roman", 20, "bold"), bg="pink", bd=3, cursor="hand2")
        btn_product.pack(side=TOP, fill=X)

        btn_exit = Button(LeftMenu, text="Exit", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2", command=self.root.quit)
        btn_exit.pack(side=TOP, fill=X)

        self.lbl_employee = Label(self.root, text="Total Employee\n[ 0 ]", bd=5, relief=RIDGE, bg="#FF4500", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n[ 0 ]", bd=5, relief=RIDGE, bg="#32CD32", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=650, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total Product\n[ 0 ]", bd=5, relief=RIDGE, bg="#4682B4", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=1000, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[ 0 ]", bd=5, relief=RIDGE, bg="#8A2BE2", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=300, y=300, height=150, width=300)

    def update_time(self):
        current_time = time.strftime("%d-%m-%Y %H:%M:%S")
        self.lbl_clock.config(text=f"\u0938\u094D\u091F\u0949\u0915 \u0938\u0947\u091C\u092E\u093E \u0938\u094D\u0935\u093E\u0917\u0924 \u091B\u0947\t\t Date: {current_time[:10]}\t\t Time: {current_time[11:]}", bg='green')
        self.root.after(1000, self.update_time)

    def open_employee_window(self):
        new_win = Toplevel(self.root)
        employeeClass(new_win)

    def open_supplier_window(self):
        new_win = Toplevel(self.root)
        SupplierClass(new_win)

    def open_category_window(self):
        new_win = Toplevel(self.root)
        categoryClass(new_win)

    def open_product_window(self):
        new_win = Toplevel(self.root)
        ProductClass(new_win)

if __name__ == "__main__":
    root = Tk()
    obj = management(root)
    root.mainloop()
