import tkinter as tk
from tkinter import messagebox
from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df
import pandas as pd


class EnrollmentManagement:
    def __init__(self, close_callback=None):
        self.root = tk.Toplevel()  # Use Toplevel for the secondary window
        self.root.title("Enrollment Management")
        self.close_callback = close_callback  # Store the callback for cleanup when this window closes
        self.setup_gui()  # Directly set up the GUI upon instantiation

    def setup_gui(self):
        """
        Sets up the GUI for enrollment management.
        """
        tk.Label(self.root, text="Student ID").grid(row=0, column=0, padx=10, pady=10)
        student_id_entry = tk.Entry(self.root)
        student_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Course ID").grid(row=1, column=0, padx=10, pady=10)
        course_id_entry = tk.Entry(self.root)
        course_id_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(
            self.root,
            text="Enroll",
            command=lambda: self.enroll_student(
                student_id_entry.get(),
                course_id_entry.get()
            )
        ).grid(row=2, column=1, pady=10)

        tk.Button(self.root, text="Display Enrollments", command=self.display_enrollments).grid(row=3, column=1, pady=10)
        tk.Button(self.root, text="Close", command=self.root.destroy).grid(row=4, column=1, pady=10)

    def enroll_student(self, student_id, course_id):
        """
        Enrolls a student in a course.
        """
        try:
            if not student_id or not course_id:
                messagebox.showerror("Input Error", "Both fields are required!")
                return

            enrollments_df = read_from_df('enrollments')

            # Generate a new enrollment ID
            new_enrollment_id = enrollments_df['enrollment_id'].max() + 1 if not enrollments_df.empty else 1

            # Create a new enrollment record
            new_enrollment = {
                "enrollment_id": new_enrollment_id,
                "student_id": int(student_id),
                "course_id": int(course_id)
            }

            # Convert the new enrollment to a DataFrame
            new_enrollment_df = pd.DataFrame([new_enrollment])

            # Append the new enrollment to the existing DataFrame
            enrollments_df = pd.concat([enrollments_df, new_enrollment_df], ignore_index=True)

            # Save the updated DataFrame to the database
            save_df_to_db('enrollments', enrollments_df)

            messagebox.showinfo("Success", "Student enrolled successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll student: {e}")

    def display_enrollments(self):
        """
        Displays all enrollments in a scrollable GUI window.
        """
        try:
            # Create a new window for displaying enrollment data
            display_window = tk.Toplevel(self.root)
            display_window.title("Enrollment List")
            display_window.geometry("500x400")

            enrollments_df = read_from_df('enrollments')

            # Add a title label
            tk.Label(display_window, text="Enrollment List", font=("Helvetica", 14, "bold")).pack(pady=10)

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

            # Add enrollment data to the scrollable frame
            for idx, enrollment in enrollments_df.iterrows():
                enrollment_info = (
                    f"Enrollment ID: {enrollment['enrollment_id']}, "
                    f"Student ID: {enrollment['student_id']}, "
                    f"Course ID: {enrollment['course_id']}"
                )
                tk.Label(inner_frame, text=enrollment_info).pack(anchor="w", padx=10, pady=2)

            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display enrollments: {e}")
