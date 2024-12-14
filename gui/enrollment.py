import tkinter as tk
from tkinter import messagebox, ttk
from src.saveChangeToDatabase import save_df_to_db, read_from_df
import pandas as pd


class EnrollmentManagement:
    def __init__(self, parent):
        """
        Initialize the Enrollment Management GUI within the parent frame.
        """
        self.parent = parent
        self.setup_gui()

    def setup_gui(self):
        enrollments_df = read_from_df('enrollments')
        tk.Label(self.parent, text="Student ID").grid(row=0, column=0, padx=10, pady=10)
        student_id_entry = ttk.Combobox(self.parent)
        student_id_entry['values'] = enrollments_df['student_id'].tolist()
        student_id_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.parent, text="Course ID").grid(row=1, column=0, padx=10, pady=10)
        course_id_entry = ttk.Combobox(self.parent)
        course_id_entry['values'] = enrollments_df['course_id'].tolist()
        course_id_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(
            self.parent,
            text="Enroll",
            command=lambda: self.enroll_student(
                student_id_entry.get(),
                course_id_entry.get()
            )
        ).grid(row=2, column=1, pady=10)

        tk.Button(self.parent, text="Display Enrollments", command=self.display_enrollments).grid(row=3, column=1, pady=10)

    def enroll_student(self, student_id, course_id):
        try:
            if not student_id or not course_id:
                messagebox.showerror("Input Error", "Both fields are required!")
                return

            enrollments_df = read_from_df('enrollments')

            new_enrollment = {
                "enrollment_id": enrollments_df['enrollment_id'].max() + 1 if not enrollments_df.empty else 1,
                "student_id": int(student_id),
                "course_id": int(course_id)
            }

            # Convert the new enrollment to a DataFrame
            new_enrollment_df = pd.DataFrame([new_enrollment])

            # Append the new enrollment to the existing DataFrame
            enrollments_df = pd.concat([enrollments_df, new_enrollment_df], ignore_index=True)

            # Save the updated DataFrame to the database
            save_df_to_db('enrollments', enrollments_df, new_enrollment_id)


            messagebox.showinfo("Success", "Student enrolled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll student: {e}")

    def display_enrollments(self):
        try:
            enrollments_df = read_from_df('enrollments')

            display_window = tk.Toplevel(self.parent)
            display_window.title("Enrollment List")
            display_window.geometry("500x400")

            tk.Label(display_window, text="Enrollment List", font=("Helvetica", 14, "bold")).pack(pady=10)

            frame = tk.Frame(display_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree = ttk.Treeview(frame, columns=('enrollment_id', 'student_id', 'course_id'), show='headings')
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=tree.yview)

            tree.heading('enrollment_id', text='Enrollment ID')
            tree.heading('student_id', text='Student ID')
            tree.heading('course_id', text='Course ID')

            tree.column('enrollment_id', anchor='center', width=100)
            tree.column('student_id', anchor='center', width=100)
            tree.column('course_id', anchor='center', width=100)

            for _, enrollment in enrollments_df.iterrows():
                tree.insert('', 'end', values=(enrollment['enrollment_id'], enrollment['student_id'], enrollment['course_id']))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display enrollments: {e}")
