import tkinter as tk
from tkinter import messagebox
from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df
import pandas as pd


class TeacherManagement:
    def __init__(self, parent):
        """
        Initialize the Teacher Management GUI within the parent frame.
        """
        self.parent = parent
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.parent, text="First Name").grid(row=0, column=0)
        first_name_entry = tk.Entry(self.parent)
        first_name_entry.grid(row=0, column=1)

        tk.Label(self.parent, text="Last Name").grid(row=1, column=0)
        last_name_entry = tk.Entry(self.parent)
        last_name_entry.grid(row=1, column=1)

        tk.Label(self.parent, text="Date of Birth (YYYY-MM-DD)").grid(row=2, column=0)
        dob_entry = tk.Entry(self.parent)
        dob_entry.grid(row=2, column=1)

        tk.Label(self.parent, text="Qualification").grid(row=3, column=0)
        qual_entry = tk.Entry(self.parent)
        qual_entry.grid(row=3, column=1)

        tk.Button(
            self.parent,
            text="Add Teacher",
            command=lambda: self.add_teacher(
                first_name_entry.get(),
                last_name_entry.get(),
                dob_entry.get(),
                qual_entry.get()
            )
        ).grid(row=4, column=1, pady=10)

        tk.Button(self.parent, text="Display Teachers", command=self.display_teachers).grid(row=5, column=1, pady=10)

    def add_teacher(self, first_name, last_name, dob, qualifications):
        try:
            if not all([first_name, last_name, dob, qualifications]):
                messagebox.showerror("Input Error", "All fields are required!")
                return

            teachers_df = read_from_df('teachers')
            new_teacher = {
                "teacher_id": teachers_df['teacher_id'].max() + 1 if not teachers_df.empty else 1,
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": dob,
                "qualifications": qualifications
            }
            teachers_df = pd.concat([teachers_df, pd.DataFrame([new_teacher])], ignore_index=True)
            save_df_to_db('teachers', teachers_df)

            messagebox.showinfo("Success", "Teacher added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add teacher: {e}")

    def display_teachers(self):
        try:
            teachers_df = read_from_df('teachers')

            display_window = tk.Toplevel(self.parent)
            display_window.title("Teacher List")
            display_window.geometry("500x400")

            tk.Label(display_window, text="Teacher List", font=("Helvetica", 14, "bold")).pack(pady=10)

            frame = tk.Frame(display_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=canvas.yview)

            inner_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            for _, teacher in teachers_df.iterrows():
                teacher_info = (
                    f"ID: {teacher['teacher_id']}, "
                    f"Name: {teacher['first_name']} {teacher['last_name']}, "
                    f"DOB: {teacher['date_of_birth']}, "
                    f"Qualifications: {teacher['qualifications']}"
                )
                tk.Label(inner_frame, text=teacher_info).pack(anchor="w", padx=10, pady=2)

            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display teachers: {e}")


class GradeEntry:
    def __init__(self, parent):
        """
        Initialize the Grade Entry GUI within the parent frame.
        """
        self.parent = parent
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.parent, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        self.student_id_entry = tk.Entry(self.parent)
        self.student_id_entry.grid(row=0, column=1)

        tk.Label(self.parent, text="Course ID:").grid(row=1, column=0, padx=10, pady=10)
        self.course_id_entry = tk.Entry(self.parent)
        self.course_id_entry.grid(row=1, column=1)

        tk.Label(self.parent, text="Grade:").grid(row=2, column=0, padx=10, pady=10)
        self.grade_entry = tk.Entry(self.parent)
        self.grade_entry.grid(row=2, column=1)

        tk.Button(self.parent, text="Submit Grade", command=self.submit_grade).grid(row=3, column=1, pady=10)

    def submit_grade(self):
        try:
            student_id = self.student_id_entry.get()
            course_id = self.course_id_entry.get()
            grade = self.grade_entry.get()

            if not student_id or not course_id or not grade:
                messagebox.showerror("Input Error", "All fields are required!")
                return

            grades_df = read_from_df('grades')
            new_grade = pd.DataFrame([{
                "student_id": int(student_id),
                "course_id": int(course_id),
                "grade": grade
            }])
            grades_df = pd.concat([grades_df, new_grade], ignore_index=True)
            save_df_to_db('grades', grades_df)

            messagebox.showinfo("Success", "Grade submitted successfully!")
            self.student_id_entry.delete(0, tk.END)
            self.course_id_entry.delete(0, tk.END)
            self.grade_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit grade: {e}")
