import tkinter as tk
from tkinter import messagebox
from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df
import pandas as pd


class StudentManagement:
    def __init__(self, close_callback=None):
        self.root = tk.Toplevel()  # Use Toplevel for the secondary window
        self.root.title("Student Management")
        self.close_callback = close_callback  # Store the callback for cleanup when this window closes
        self.setup_gui()  # Directly set up the GUI upon instantiation

    def setup_gui(self):
        """
        Sets up the GUI for student management.
        """
        tk.Label(self.root, text="Enter details for the new student").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="First Name").grid(row=1, column=0)
        first_name_entry = tk.Entry(self.root)
        first_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Last Name").grid(row=2, column=0)
        last_name_entry = tk.Entry(self.root)
        last_name_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Date of Birth (YYYY-MM-DD)").grid(row=3, column=0)
        dob_entry = tk.Entry(self.root)
        dob_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Address").grid(row=4, column=0)
        address_entry = tk.Entry(self.root)
        address_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Email").grid(row=5, column=0)
        email_entry = tk.Entry(self.root)
        email_entry.grid(row=5, column=1)

        tk.Button(
            self.root,
            text="Add Student",
            command=lambda: self.add_student(
                first_name_entry.get(),
                last_name_entry.get(),
                dob_entry.get(),
                address_entry.get(),
                email_entry.get()
            )
        ).grid(row=6, column=1, pady=10)

        tk.Button(self.root, text="Display Students", command=self.display_students).grid(row=7, column=1, pady=10)
        tk.Button(self.root, text="Close", command=self.root.destroy).grid(row=8, column=1, pady=10)

    def add_student(self, first_name, last_name, dob, address, email):
        """
        Adds a new student to the database.
        """
        try:
            if not all([first_name, last_name, dob, address, email]):
                messagebox.showerror("Input Error", "All fields are required!")
                return

            if "@" not in email:
                messagebox.showerror("Input Error", "Invalid email format!")
                return

            students_df = read_from_df('students')
            new_student = pd.DataFrame([{
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": dob,
                "address": address,
                "email": email,
                "student_id": students_df['student_id'].max() + 1 if not students_df.empty else 1
            }])
            students_df = pd.concat([students_df, new_student], ignore_index=True)
            save_df_to_db('students', students_df)

            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {e}")

    def display_students(self):
        """
        Displays all students in a scrollable GUI window.
        """
        try:
            # Create a new window for displaying student data
            display_window = tk.Toplevel(self.root)
            display_window.title("Student List")
            display_window.geometry("600x400")

            students_df = read_from_df('students')

            # Add a title label
            tk.Label(display_window, text="Student List", font=("Helvetica", 14, "bold")).pack(pady=10)

            # Create a scrollable frame
            frame = tk.Frame(display_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=canvas.yview)

            inner_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            # Add student data to the scrollable frame
            for idx, student in students_df.iterrows():
                student_info = (
                    f"ID: {student['student_id']}, "
                    f"Name: {student['first_name']} {student['last_name']}, "
                    f"DOB: {student['date_of_birth']}, "
                    f"Address: {student['address']}, "
                    f"Email: {student['email']}"
                )
                tk.Label(inner_frame, text=student_info, anchor="w").pack(anchor="w", padx=10, pady=2)

            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display students: {e}")
