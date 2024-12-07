import tkinter as tk
from tkinter import messagebox
from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df
import pandas as pd  # Ensure pandas is imported
from src.db_handling.tables import audit_log_df



class StudentManagement:
    def __init__(self, show_callback=None):
        self.root = tk.Toplevel()
        self.root.title("Student Management")
        self.show_callback = show_callback

    def add_student(self, first_name, last_name, dob, address, email):
        """
        Adds a new student to the database.
        """
        try:
            # Validate inputs
            if not all([first_name, last_name, dob, address, email]):
                messagebox.showerror("Input Error", "All fields are required!")
                return

            if "@" not in email:
                messagebox.showerror("Input Error", "Invalid email format!")
                return

            # Fetch the students DataFrame
            students_df = read_from_df('students')

            # Create a new row as a DataFrame
            new_student = pd.DataFrame([{
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": dob,
                "address": address,
                "email": email,
                "student_id": students_df['student_id'].max() + 1 if not students_df.empty else 1
            }])

            # Concatenate the new student to the DataFrame
            students_df = pd.concat([students_df, new_student], ignore_index=True)

            # Save the updated DataFrame to the database
            save_df_to_db('students', students_df, new=True, who="Admin", index=new_student.loc[0, "student_id"])

            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {e}")

    def run(self):
        """
        Starts the GUI application for managing students.
        """
        # Test input and format labels
        tk.Label(self.root, text="Enter details for the new student").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="First Name (e.g., John)").grid(row=1, column=0)
        first_name_entry = tk.Entry(self.root)
        first_name_entry.insert(0, "John")  # Test input
        first_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Last Name (e.g., Doe)").grid(row=2, column=0)
        last_name_entry = tk.Entry(self.root)
        last_name_entry.insert(0, "Doe")  # Test input
        last_name_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Date of Birth (YYYY-MM-DD)").grid(row=3, column=0)
        dob_entry = tk.Entry(self.root)
        dob_entry.insert(0, "2000-01-01")  # Test input
        dob_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Address (e.g., 123 Main St)").grid(row=4, column=0)
        address_entry = tk.Entry(self.root)
        address_entry.insert(0, "123 Main St, Springfield, IL")  # Test input
        address_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Email (e.g., john.doe@example.com)").grid(row=5, column=0)
        email_entry = tk.Entry(self.root)
        email_entry.insert(0, "john.doe@example.com")  # Test input
        email_entry.grid(row=5, column=1)

        # Add buttons
        tk.Button(
            self.root,
            text="Add Student",
            command=lambda: self.add_student(
                first_name_entry.get(),
                last_name_entry.get(),
                dob_entry.get(),
                address_entry.get(),
                email_entry.get()
            ),
        ).grid(row=6, column=1, pady=10)

        tk.Button(self.root, text="Back", command=self.back_to_dashboard).grid(row=7, column=1, pady=10)

    def back_to_dashboard(self):
        if self.show_callback:
            self.show_callback()
        self.root.destroy()
