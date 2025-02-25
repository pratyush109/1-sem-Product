import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


class Login:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Portal")
        self.master.geometry("1000x440")
        self.master.configure(bg='#800000')
        self.master.eval('tk::PlaceWindow %s center' % self.master.winfo_toplevel())

        self.setup_db()
        self.create_default_user()
        self.setup_ui()

    def setup_db(self):
        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                phone TEXT,
                login_attempts INTEGER DEFAULT 0,
                is_locked BOOLEAN DEFAULT FALSE
            )
        ''')
        connection.commit()
        connection.close()

    def create_default_user(self):
        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", self.encrypt_password("admin123")))
            connection.commit()
        connection.close()

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def connect_to_db(self):
        return sqlite3.connect('user_data.db')

    def setup_ui(self):
        frame = tk.Frame(self.master, bg='#F4F4F4', padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        header_label = tk.Label(self.master, text="Welcome to Stock Manager", fg="#FFFFFF", bg="#800000", font=("Arial", 60, "bold"))
        header_label.place(x=20, y=20)

        login_label = tk.Label(frame, text="User Login", bg='#F4F4F4', fg="#34495E", font=("Arial", 30))
        user_label = tk.Label(frame, text="Username", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        self.username_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50')

        pass_label = tk.Label(frame, text="Password", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        self.password_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50', show='*')

        self.show_pass_var = tk.BooleanVar()
        show_pass_check = tk.Checkbutton(frame, text="Show Password", variable=self.show_pass_var, bg='#F4F4F4', font=("Arial", 12), command=self.toggle_password_visibility)

        login_btn = tk.Button(frame, text="Login", bg="#4CAF50", font=("Arial", 16), command=self.user_login)
        forgot_btn = tk.Button(frame, text="Forgot Password", bg="#FF5733", font=("Arial", 12), command=self.forgot_password_window)
        create_btn = tk.Button(frame, text="Create Account", bg="#FF5733", font=("Arial", 12), command=self.create_account_window)

        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)
        user_label.grid(row=1, column=0, pady=5)
        self.username_input.grid(row=1, column=1, pady=10)
        pass_label.grid(row=2, column=0, pady=5)
        self.password_input.grid(row=2, column=1, pady=10)
        show_pass_check.grid(row=3, column=0, columnspan=2, pady=5)
        login_btn.grid(row=4, column=0, columnspan=2, pady=15)
        forgot_btn.grid(row=5, column=0, columnspan=2, pady=10)
        create_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def toggle_password_visibility(self):
        if self.show_pass_var.get():
            self.password_input.config(show='')  
        else:
            self.password_input.config(show='*')  

    def user_login(self):
        username = self.username_input.get()
        password = self.password_input.get()
        hashed_password = self.encrypt_password(password)

        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            stored_password, attempts, locked = user[2], user[5], user[6]
            if locked:
                messagebox.showerror("Account Locked", "Your account is locked due to multiple failed login attempts.")
            elif stored_password == hashed_password:
                messagebox.showinfo("Login Successful", "Welcome!")
                cursor.execute("UPDATE users SET login_attempts = 0 WHERE username = ?", (username,))
                connection.commit()
                self.redirect_to_dashboard()
            else:
                attempts += 1
                if attempts >= 3:
                    cursor.execute("UPDATE users SET is_locked = 1 WHERE username = ?", (username,))
                    messagebox.showerror("Account Locked", "Too many failed attempts. Your account is now locked.")
                else:
                    cursor.execute("UPDATE users SET login_attempts = ? WHERE username = ?", (attempts, username))
                    messagebox.showerror("Invalid Login", f"Incorrect username or password. Attempt {attempts}/3.")
                connection.commit()
        else:
            messagebox.showerror("Invalid Login", "Username or password is incorrect.")

        connection.close()

    def redirect_to_dashboard(self):
        self.master.destroy()
        dashboard = tk.Tk()
        dashboard.title("Dashboard")
        dashboard.geometry("800x600")
        tk.Label(dashboard, text="Welcome to the Dashboard", font=("Arial", 24)).pack(pady=20)
        dashboard.mainloop()

    def forgot_password_window(self):
        forgot_window = tk.Toplevel(self.master)
        forgot_window.title("Reset Password")
        forgot_window.geometry("400x250")

        frame = tk.Frame(forgot_window, bg='#F4F4F4', padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        username_label = tk.Label(frame, text="Username", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        username_label.grid(row=0, column=0, pady=5)
        username_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50')
        username_input.grid(row=0, column=1, pady=10)


        old_pass_label = tk.Label(frame, text="Old Password", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        old_pass_label.grid(row=1, column=0, pady=5)
        old_pass_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50', show='*')
        old_pass_input.grid(row=1, column=1, pady=10)

        new_pass_label = tk.Label(frame, text="New Password", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        new_pass_label.grid(row=2, column=0, pady=5)
        new_pass_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50', show='*')
        new_pass_input.grid(row=2, column=1, pady=10)

        reset_btn = tk.Button(frame, text="Reset Password", bg="#4CAF50", font=("Arial", 16), command=lambda: self.reset_password(username_input,old_pass_input, new_pass_input, forgot_window))
        reset_btn.grid(row=3, column=0, columnspan=2, pady=15)

    def reset_password(self, username_input,old_pass_input, new_pass_input, window):
        username = username_input.get()
        old_password = old_pass_input.get()
        new_password = new_pass_input.get()
        hashed_new_password = self.encrypt_password(new_password)

        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (self.username_input.get(),))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE users SET password = ?, login_attempts = 0, is_locked = 0 WHERE username = ?",
                           (hashed_new_password, self.username_input.get()))
            connection.commit()
            messagebox.showinfo("Password Reset", "Your password has been successfully updated!")
            window.destroy()
        else:
            messagebox.showerror("Error", "Username not found.")

        connection.close()

    def create_account_window(self):
        create_account_window = tk.Toplevel(self.master)
        create_account_window.title("Create New Account")
        create_account_window.geometry("600x550")

        frame = tk.Frame(create_account_window, bg='#F4F4F4', padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        username_label = tk.Label(frame, text="Username", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        username_label.grid(row=0, column=0, pady=5, sticky="e")
        username_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50')
        username_input.grid(row=0, column=1, pady=10, padx=10)

        password_label = tk.Label(frame, text="Create Password", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        password_label.grid(row=1, column=0, pady=5, sticky="e")
        password_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50', show='*')
        password_input.grid(row=1, column=1, pady=10, padx=10)

        confirm_pass_label = tk.Label(frame, text="Confirm Password", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        confirm_pass_label.grid(row=2, column=0, pady=5, sticky="e")
        confirm_pass_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50', show='*')
        confirm_pass_input.grid(row=2, column=1, pady=10, padx=10)

        email_label = tk.Label(frame, text="Email Address", bg='#F4F4F4', fg="#34495E", font=("Arial", 16))
        email_label.grid(row=3, column=0, pady=5, sticky="e")
        email_input = tk.Entry(frame, font=("Arial", 16), fg='#2C3E50')
        email_input.grid(row=3, column=1, pady=10, padx=10)

        create_btn = tk.Button(frame, text="Create Account", bg="#4CAF50", font=("Arial", 16),
                               command=lambda: self.register_account(username_input, password_input, confirm_pass_input, email_input, create_account_window))
        create_btn.grid(row=4, column=0, columnspan=2, pady=15)

    def register_account(self, username_input, password_input, confirm_pass_input, email_input, window):
        username = username_input.get()
        password = password_input.get()
        confirm_password = confirm_pass_input.get()
        email = email_input.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        hashed_password = self.encrypt_password(password)

        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                       (username, hashed_password, email))
        connection.commit()
        connection.close()
        messagebox.showinfo("Account Created", "Your account has been successfully created!")
        window.destroy()


if __name__ == "__main__":
    main_window = tk.Tk()
    obj = Login(main_window)
    main_window.mainloop() 
