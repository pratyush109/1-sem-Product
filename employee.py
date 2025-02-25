from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Stock Sage")
        self.root.config(bg="#2C3E50")  
        self.root.focus_force()

        self.var_emp_id = StringVar()
        self.var_searchby_id = StringVar()
        self.var_searchtxt_id = StringVar()
        self.var_gender_id = StringVar()
        self.var_contact_id = StringVar()
        self.var_name_id = StringVar()
        self.var_dob_id = StringVar()
        self.var_doj_id = StringVar()
        self.var_email_id = StringVar()
        self.var_pass_id = StringVar()
        self.var_utype_id = StringVar()
        self.var_salary_id = StringVar()

        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("Times New Roman", 15, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby_id, values=("Select", "Email", "Name", "Contact"), 
                                  state='readonly', justify=CENTER, font=("Times New Roman", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt_id, font=("Goudy Old Style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10, width=180)

        btn_search = Button(SearchFrame, text="Search", font=("Goudy Old Style", 15), bg="green", fg="white", cursor="hand2", command=self.search_employee)
        btn_search.place(x=410, y=10, width=150, height=30)

        title = Label(self.root, text="Employee Details", font=("Goudy Old Style", 18, "bold"), bg="#34495E", fg="white")
        title.place(x=50, y=100, width=1000, height=40)

        lbl_empid = Label(self.root, text="Emp ID ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_empid.place(x=50, y=160)
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("Goudy Old Style", 15), bg="white")
        txt_empid.place(x=150, y=160, width=180)

        lbl_gender = Label(self.root, text="Gender ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_gender.place(x=350, y=160)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender_id, values=("Select", "Male", "Female", "Other"), 
                                  state='readonly', justify=CENTER, font=("Times New Roman", 15))
        cmb_gender.place(x=500, y=160, width=180)
        cmb_gender.current(0)

        lbl_contact = Label(self.root, text="Contact ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_contact.place(x=750, y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact_id, font=("Goudy Old Style", 15), bg="white")
        txt_contact.place(x=850, y=160, width=180)

        lbl_name = Label(self.root, text="Name ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_name.place(x=50, y=200)
        txt_name = Entry(self.root, textvariable=self.var_name_id, font=("Goudy Old Style", 15), bg="white")
        txt_name.place(x=150, y=200, width=180)

        lbl_dob = Label(self.root, text="D.O.B ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_dob.place(x=350, y=200)
        txt_dob = Entry(self.root, textvariable=self.var_dob_id, font=("Goudy Old Style", 15), bg="white")
        txt_dob.place(x=500, y=200, width=180)

        lbl_doj = Label(self.root, text="D.O.J ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_doj.place(x=750, y=200)
        txt_doj = Entry(self.root, textvariable=self.var_doj_id, font=("Goudy Old Style", 15), bg="white")
        txt_doj.place(x=850, y=200, width=180)

        lbl_email = Label(self.root, text="Email ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_email.place(x=50, y=240)
        txt_email = Entry(self.root, textvariable=self.var_email_id, font=("Goudy Old Style", 15), bg="white")
        txt_email.place(x=150, y=240, width=180)

        lbl_pass = Label(self.root, text="Password ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_pass.place(x=350, y=240)
        txt_pass = Entry(self.root, textvariable=self.var_pass_id, font=("Goudy Old Style", 15), bg="white", show="*")
        txt_pass.place(x=500, y=240, width=180)

        lbl_utype = Label(self.root, text="User Type ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_utype.place(x=750, y=240)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype_id, values=("Admin", "Employee"), 
                                 state='readonly', justify=CENTER, font=("Times New Roman", 15))
        cmb_utype.place(x=850, y=240, width=180)
        cmb_utype.current(0)

        lbl_salary = Label(self.root, text="Salary ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_salary.place(x=350, y=280)
        txt_salary = Entry(self.root, textvariable=self.var_salary_id, font=("Goudy Old Style", 15), bg="white")
        txt_salary.place(x=500, y=280, width=180)

        lbl_address = Label(self.root, text="Address ", font=("Goudy Old Style", 15), bg="#2C3E50", fg="white")
        lbl_address.place(x=50, y=280)
        self.txt_address = Text(self.root, font=("Goudy Old Style", 15), bg="white", height=2, width=25)
        self.txt_address.place(x=150, y=280)

        btn_add = Button(self.root, text="Save", command=self.add, font=("Goudy Old Style", 15), bg="green", fg="white", cursor="hand2")
        btn_add.place(x=50, y=350, width=150, height=40)

        btn_update = Button(self.root, text="Update", font=("Goudy Old Style", 15), bg="blue", fg="white", cursor="hand2")
        btn_update.place(x=220, y=350, width=150, height=40)

        btn_delete = Button(self.root, text="Delete", font=("Goudy Old Style", 15), bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=390, y=350, width=150, height=40)

        btn_Clear = Button(self.root, text="Clear", font=("Goudy Old Style", 15), bg="orange", fg="white", cursor="hand2")
        btn_Clear.place(x=585, y=350, width=150, height=40)

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=400, relwidth=1, height=250)  # Move frame down so buttons are above

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid","name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        self.EmployeeTable.heading("eid", text="EID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=200)

        # Packing the scrollbars and table correctly
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        self.EmployeeTable.pack(fill=BOTH, expand=1)

        scrolly.config(command=self.EmployeeTable.yview)
        scrollx.config(command=self.EmployeeTable.xview)

    def add(self):
        con = sqlite3.connect(database=r'ims')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO employee (eid, name, email, gender, contact, dob, doj, pass, utype, address, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        self.var_emp_id.get(),
                        self.var_name_id.get(),
                        self.var_email_id.get(),
                        self.var_gender_id.get(),
                        self.var_contact_id.get(),
                        self.var_dob_id.get(),
                        self.var_doj_id.get(),
                        self.var_pass_id.get(),
                        self.var_utype_id.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary_id.get(),
                    ))

            con.commit()
            messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search_employee(self):
        search_by = self.var_searchby_id.get()
        search_txt = self.var_searchtxt_id.get()

        if search_by == "Select":
            messagebox.showerror("Error", "Please select a search criteria", parent=self.root)
            return

        con = sqlite3.connect(database=r'ims')
        cur = con.cursor()

        if search_by == "Email":
            cur.execute("SELECT * FROM employee WHERE email LIKE ?", ('%' + search_txt + '%',))
        elif search_by == "Name":
            cur.execute("SELECT * FROM employee WHERE name LIKE ?", ('%' + search_txt + '%',))
        elif search_by == "Contact":
            cur.execute("SELECT * FROM employee WHERE contact LIKE ?", ('%' + search_txt + '%',))

        rows = cur.fetchall()
        if len(rows) == 0:
            messagebox.showinfo("No Data", "No matching records found", parent=self.root)
        else:
            for row in rows:
                print(row)  # You can populate the treeview here if needed

        con.close()


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop() 
