import tkinter as tk
from tkinter import ttk, messagebox
from src.db_handling.openDatabase import enrollments_df, students_df, courses_df
import pandas as pd

class EnrollmentManagement:
    def __init__(self, go_back_callback):
        self.go_back_callback = go_back_callback
        self.root = tk.Toplevel()  # Use Toplevel for the enrollment management window
        self.root.title("Enrollment Management")

    def enroll_student(self, student_id, course_id):
        global enrollments_df
        try:
            new_id = enrollments_df['enrollment_id'].max() + 1 if not enrollments_df.empty else 0
            new_enrollment = {
                'enrollment_id': new_id,
                'student_id': int(student_id),
                'course_id': int(course_id)
            }
            enrollments_df = pd.concat([enrollments_df, pd.DataFrame([new_enrollment])], ignore_index=True)
            messagebox.showinfo("Success", "Student enrolled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll student: {e}")

    def display_enrollments(self):
        display_window = tk.Toplevel(self.root)
        display_window.title("Enrollments List")
        display_window.geometry("600x400")

        tree = ttk.Treeview(display_window, columns=("Enrollment ID", "Student ID", "Course ID"), show="headings")
        tree.heading("Enrollment ID", text="Enrollment ID")
        tree.heading("Student ID", text="Student ID")
        tree.heading("Course ID", text="Course ID")
        tree.column("Enrollment ID", width=100, anchor="center")
        tree.column("Student ID", width=100, anchor="center")
        tree.column("Course ID", width=100, anchor="center")

        for _, row in enrollments_df.iterrows():
            tree.insert("", "end", values=(row["enrollment_id"], row["student_id"], row["course_id"]))

        scrollbar = ttk.Scrollbar(display_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")
        tk.Button(display_window, text="Close", command=display_window.destroy).pack(pady=10)

    def go_back(self):
        self.root.destroy()
        self.go_back_callback()  # Call the go-back callback to show the dashboard

    def run(self):
        tk.Label(self.root, text="Enrollment Management", font=("Arial", 16)).pack(pady=20)

        # Form to enroll a student
        tk.Label(self.root, text="Student ID").pack(pady=5)
        student_id_entry = tk.Entry(self.root)
        student_id_entry.pack(pady=5)

        tk.Label(self.root, text="Course ID").pack(pady=5)
        course_id_entry = tk.Entry(self.root)
        course_id_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Enroll Student",
            command=lambda: self.enroll_student(student_id_entry.get(), course_id_entry.get())
        ).pack(pady=5)

        # Button to show all enrollments
        tk.Button(self.root, text="Show Enrollments", command=self.display_enrollments).pack(pady=5)

        # Back button
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=10)

        self.root.mainloop()
