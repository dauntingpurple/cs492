import tkinter as tk
from tkinter import messagebox
from gui.dashboard import Dashboard

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

    def authenticate(self, username, password):
        # Check if the username exists and the password matches
        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
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