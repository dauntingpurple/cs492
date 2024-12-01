import tkinter as tk
from tkinter import ttk, messagebox
from src.db_handling.openDatabase import students_df
import pandas as pd

class StudentManagement:
    def __init__(self, go_back_callback):
        self.go_back_callback = go_back_callback
        self.root = tk.Toplevel()  # Use Toplevel for the student management window
        self.root.title("Student Management")

    def add_student(self, first_name, last_name, dob):
        global students_df
        try:
            new_id = students_df['student_id'].max() + 1 if not students_df.empty else 0
            new_student = {
                'student_id': new_id,
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': dob
            }
            students_df = pd.concat([students_df, pd.DataFrame([new_student])], ignore_index=True)
            
    def add_student(self, first_name, last_name, dob, address, email):
        """
        Adds a new student to the database.
        """
        # Validate input fields
        if not first_name or not last_name or not dob:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            new_index = (students_df.index[-1]) + 1
            new_student = {first_name, last_name, dob, address, email, new_index}
            students_df = students_df.append(new_student)
            """
            # Connect to the database
            session = Session()

            # Use text() to explicitly declare the SQL query
            insert_query = text(
                "INSERT INTO students (first_name, last_name, date_of_birth) VALUES (:first_name, :last_name, :dob)"
            )
            session.execute(insert_query, {"first_name": first_name, "last_name": last_name, "dob": dob})
            session.commit()
            session.close()
            """
            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {e}")

    def display_students(self):
        display_window = tk.Toplevel(self.root)
        display_window.title("Students List")
        display_window.geometry("600x400")

        tree = ttk.Treeview(display_window, columns=("Student ID", "First Name", "Last Name", "Date of Birth"), show="headings")
        tree.heading("Student ID", text="Student ID")
        tree.heading("First Name", text="First Name")
        tree.heading("Last Name", text="Last Name")
        tree.heading("Date of Birth", text="Date of Birth")
        tree.column("Student ID", width=100, anchor="center")
        tree.column("First Name", width=150, anchor="center")
        tree.column("Last Name", width=150, anchor="center")
        tree.column("Date of Birth", width=150, anchor="center")

        for _, row in students_df.iterrows():
            tree.insert("", "end", values=(row["student_id"], row["first_name"], row["last_name"], row["date_of_birth"]))

        scrollbar = ttk.Scrollbar(display_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")
        tk.Button(display_window, text="Close", command=display_window.destroy).pack(pady=10)

    def go_back(self):
        self.root.destroy()
        self.go_back_callback()  # Call the go-back callback to show the dashboard

    def run(self):
        tk.Label(self.root, text="Student Management", font=("Arial", 16)).pack(pady=20)

        # Form to add a student
        tk.Label(self.root, text="First Name").pack(pady=5)
        first_name_entry = tk.Entry(self.root)
        first_name_entry.pack(pady=5)

        tk.Label(self.root, text="Last Name").pack(pady=5)
        last_name_entry = tk.Entry(self.root)
        last_name_entry.pack(pady=5)

        tk.Label(self.root, text="Date of Birth (YYYY-MM-DD)").pack(pady=5)
        dob_entry = tk.Entry(self.root)
        dob_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Add Student",
            command=lambda: self.add_student(first_name_entry.get(), last_name_entry.get(), dob_entry.get())
        ).pack(pady=5)

        # Button to show all students
        tk.Button(self.root, text="Show Students", command=self.display_students).pack(pady=5)

        # Back button
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=10)

        self.root.mainloop()
