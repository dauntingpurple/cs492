import tkinter as tk
import hashlib
from tkinter import messagebox
from gui.dashboard import Dashboard
from src.saveChangeToDatabase import read_from_df

# Sample users for authentication
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "teacher": {"password": "teacher123", "role": "Teacher"},
    "registrar": {"password": "registrar123", "role": "Registrar"},
    "student": {"password": "student123", "role": "Student"},
}

class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("School Management System - Login")
        self.root.geometry("300x200")

    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username, password):
        # Check if the username exists in the DataFrame
        user_df = read_from_df('users')
        user = user_df[user_df['username'] == username]

        if not user.empty:
            stored_hash = user['password_hash'].values[0]
            # Verify the password hash
            if self.hash_password(password) == stored_hash:
                role = user['role'].values[0]  # Assuming 'role' is in the DataFrame
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.root.destroy()  # Close the login window
                Dashboard(role).run()  # Pass the role to the dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def run(self):
        tk.Label(self.root, text="Username").grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(self.root)
        username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password").grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=lambda: self.authenticate(username_entry.get(), password_entry.get())).grid(row=2, column=1, pady=20)
        self.root.mainloop()