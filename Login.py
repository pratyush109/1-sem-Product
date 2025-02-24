import tkinter as tk
from tkinter import messagebox
from management import management
import sqlite3
import hashlib


class LoginClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Form")
        self.root.geometry("1000x440")
        self.root.configure(bg='#9e0000')
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())

        self.create_db()
        self.add_test_user()
        self.build_ui()

    def create_db(self):
       
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    email TEXT,
                    phone TEXT,
                    failed_attempts INTEGER DEFAULT 0,
                    account_locked BOOLEAN DEFAULT FALSE
                )
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def add_test_user(self):
        """Adds a test user if it doesn't already exist in the database."""
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", ("Pratyush",))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("Pratyush", self.hash_password("12345")))
                conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while adding the test user: {e}")

    def hash_password(self, password):
        """Hashes the password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_connection(self):
        """Create and return a database connection."""
        return sqlite3.connect('users.db')

    def build_ui(self):
        """Sets up the login form UI."""
        frame = tk.Frame(self.root, bg='#EAEAEA', padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        welcome_label = tk.Label(self.root, text="Welcome to Stock Sage", fg="#FFFFFF", bg="#9e0000", font=("Arial", 60, "bold"))
        welcome_label.place(x=20, y=20)

        login_label = tk.Label(frame, text="Employee Login", bg='#EAEAEA', fg="#2C3E50", font=("Arial", 30))
        username_label = tk.Label(frame, text="Username", bg='#EAEAEA', fg="#2C3E50", font=("Arial", 16))
        self.username_entry = tk.Entry(frame, font=("Arial", 16), fg='#333333')

        password_label = tk.Label(frame, text="Password", bg='#EAEAEA', fg="#2C3E50", font=("Arial", 16))
        self.password_entry = tk.Entry(frame, font=("Arial", 16), fg='#333333', show='*')

        login_button = tk.Button(frame, text="Login", bg="#4CAF50", font=("Arial", 16), command=self.login)
        forget_button = tk.Button(frame, text="Forgot Password", bg="#FF5733", font=("Arial", 12), command=self.forgot_password)
        create_button = tk.Button(frame, text="Create Account", bg="#FF5733", font=("Arial", 12), command=self.create_account)

        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)
        username_label.grid(row=1, column=0, pady=5)
        self.username_entry.grid(row=1, column=1, pady=10)
        password_label.grid(row=2, column=0, pady=5)
        self.password_entry.grid(row=2, column=1, pady=10)
        login_button.grid(row=3, column=0, columnspan=2, pady=15)
        forget_button.grid(row=4, column=0, columnspan=2, pady=10)
        create_button.grid(row=5, column=0, columnspan=2, pady=10)

    

    def login(self):
        """Validates the user credentials and opens the dashboard if correct."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = self.hash_password(password)

        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                stored_password = user[2]  # Password is stored in the 3rd column of the database
                failed_attempts = user[5]
                account_locked = user[6]

                if account_locked:
                    messagebox.showinfo("Account Locked", "Your account is locked due to too many failed attempts. Try again later.")
                elif stored_password == hashed_password:
                    # Reset failed attempts on successful login
                    cursor.execute("UPDATE users SET failed_attempts = 0 WHERE username = ?", (username,))
                    conn.commit()
                    self.open_dashboard()
                else:
                    # Increment failed attempts count
                    cursor.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?", (username,))
                    conn.commit()
                    messagebox.showinfo("Invalid Login", "Invalid username or password.")

                conn.close()
            else:
                messagebox.showinfo("Invalid Login", "Invalid username or password.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred during login: {e}")

    def open_dashboard(self):
        """Closes the login window and opens the IMS dashboard."""
        self.root.destroy()  # Close the login window
        root_dashboard = tk.Tk()  # Create a new root window for the dashboard
        # ims_dashboard = ims(root_dashboard)  # Open the ims dashboard window
        root_dashboard.mainloop()  # Run the dashboard window

    def forgot_password(self):
        """Opens a password recovery window."""
        recovery_window = tk.Toplevel(self.root)
        recovery_window.title("Password Recovery")
        recovery_window.geometry("400x300")
        recovery_window.configure(bg='#2C3E50')

        username_label = tk.Label(recovery_window, text="Enter your username:", bg='#2C3E50', fg="#FFFFFF", font=("Arial", 12))
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(recovery_window, font=("Arial", 12), fg='#333333')
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        def recover_password():
            username = username_entry.get()

            try:
                conn = self.create_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Password Recovery", "Password recovery instructions sent.")
                else:
                    messagebox.showinfo("Password Recovery", "No account found with that username.")
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred during password recovery: {e}")

        recover_button = tk.Button(recovery_window, text="Recover Password", bg="#FF5733", font=("Arial", 12), command=recover_password)
        recover_button.grid(row=1, column=0, columnspan=2, pady=20)

    def create_account(self):
        """Opens a sign-up window to create an account."""
        def register_account():
            username = new_username_entry.get()
            password = new_password_entry.get()
            hashed_password = self.hash_password(password)

            try:
                conn = self.create_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                messagebox.showinfo("Account Created", f"Account for {username} created successfully!")
                create_account_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists. Choose a different one.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                conn.close()

        create_account_window = tk.Toplevel(self.root)
        create_account_window.title("Create Account")
        create_account_window.geometry("600x500")

        frame = tk.Frame(create_account_window, bg='#EAEAEA', padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        account_label = tk.Label(frame, text="Create Account", bg='#EAEAEA', fg="#2C3E50", font=("Arial", 30))
        account_label.grid(row=0, column=0, columnspan=2, pady=20)

        new_username_label = tk.Label(frame, text="Username", bg='#EAEAEA', fg="#2C3E50", font=("Arial", 16))
        new_username_label.grid(row=1, column=0, pady=5)
        new_username_entry = tk.Entry(frame, font=("Arial", 16), fg='#333333')
        new_username_entry.grid(row=1, column=1, pady=10)

        new_password_label = tk.Label(frame, text="Password", bg='#EAEAEA', fg="#2C3E50", font=("Arial", 16))
        new_password_label.grid(row=2, column=0, pady=5)
        new_password_entry = tk.Entry(frame, font=("Arial", 16), fg='#333333', show='*')
        new_password_entry.grid(row=2, column=1, pady=10)

        register_button = tk.Button(frame, text="Create Account", bg="#4CAF50", font=("Arial", 16), command=register_account)
        register_button.grid(row=4, column=0, columnspan=2, pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    obj = LoginClass(root)
    root.mainloop()
