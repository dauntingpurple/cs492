import tkinter as tk
from tkinter import messagebox
import pandas as pd
from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df


class TeacherManagement:
    def __init__(self, show_callback=None):
        self.root = tk.Toplevel()
        self.root.title("Teacher Management")
        self.show_callback = show_callback  # Store the callback for later use

    def add_teacher(self, first_name, last_name, dob, qualifications):
        """
        Adds a new teacher to the database.
        """
        if not all([first_name, last_name, dob, qualifications]):
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            from datetime import datetime
            try:
                dob = datetime.strptime(dob, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Input Error", "Invalid Date of Birth format! Use YYYY-MM-DD.")
                return

            teachers_df = read_from_df('teachers')
            new_index = (teachers_df.index[-1]) + 1 if not teachers_df.empty else 1
            new_teacher = {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": dob,
                "qualifications": qualifications,
                "teacher_id": new_index
            }

            teachers_df = teachers_df.append(new_teacher, ignore_index=True)
            save_df_to_db('teachers', teachers_df, new_index)

            messagebox.showinfo("Success", "Teacher added successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def display_teachers(self):
        """
        Displays all teacher records in a scrollable GUI window.
        """
        display_window = tk.Toplevel(self.root)
        display_window.title("Teacher List")
        display_window.geometry("500x400")

        teachers_df = read_from_df('teachers')

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

        for idx, teacher in teachers_df.iterrows():
            teacher_info = (
                f"ID: {teacher['teacher_id']}, "
                f"Name: {teacher['first_name']} {teacher['last_name']}, "
                f"DOB: {teacher['date_of_birth']}, "
                f"Qualifications: {teacher['qualifications']}"
            )
            tk.Label(inner_frame, text=teacher_info).pack(anchor="w", padx=10, pady=2)

        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def open_grade_entry(self):
        """
        Opens the Grade Entry GUI.
        """
        GradeEntry()  # Opens a new window for grade entry

    def run(self):
        tk.Label(self.root, text="First Name").grid(row=0, column=0)
        first_name_entry = tk.Entry(self.root)
        first_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Last Name").grid(row=1, column=0)
        last_name_entry = tk.Entry(self.root)
        last_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Date of Birth (YYYY-MM-DD)").grid(row=2, column=0)
        dob_entry = tk.Entry(self.root)
        dob_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Qualification").grid(row=3, column=0)
        qual_entry = tk.Entry(self.root)
        qual_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Add Teacher", command=lambda: self.add_teacher(
            first_name_entry.get(),
            last_name_entry.get(),
            dob_entry.get(),
            qual_entry.get()
        )).grid(row=4, column=1, pady=10)

        tk.Button(self.root, text="Display Teachers", command=self.display_teachers).grid(row=5, column=1, pady=10)
        tk.Button(self.root, text="Enter Grades", command=self.open_grade_entry).grid(row=6, column=1, pady=10)
        tk.Button(self.root, text="Exit", command=self.root.destroy).grid(row=7, column=1, pady=10)

        self.root.mainloop()


class GradeEntry:
    def __init__(self):
        """
        Initializes the Grade Entry GUI.
        """
        self.root = tk.Toplevel()
        self.root.title("Enter Grades")
        self.setup_gui()

    def setup_gui(self):
        """
        Sets up the GUI for entering grades.
        """
        tk.Label(self.root, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        self.student_id_entry = tk.Entry(self.root)
        self.student_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Course ID:").grid(row=1, column=0, padx=10, pady=10)
        self.course_id_entry = tk.Entry(self.root)
        self.course_id_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Grade:").grid(row=2, column=0, padx=10, pady=10)
        self.grade_entry = tk.Entry(self.root)
        self.grade_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Submit Grade", command=self.submit_grade).grid(row=3, column=1, pady=10)
        tk.Button(self.root, text="Display Grades", command=self.display_grades).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Close", command=self.root.destroy).grid(row=5, column=1, pady=10)

    def submit_grade(self):
        """
        Handles grade submission.
        """
        student_id = self.student_id_entry.get()
        course_id = self.course_id_entry.get()
        grade = self.grade_entry.get()

        if not student_id or not course_id or not grade:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
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

    def display_grades(self):
        """
        Opens a window to display all grades with student names, course names, and grades.
        """
        try:
            grades_df = read_from_df('grades')
            students_df = read_from_df('students')
            courses_df = read_from_df('courses')

            print("Grades DataFrame Columns:", grades_df.columns)
            print("Students DataFrame Columns:", students_df.columns)
            print("Courses DataFrame Columns:", courses_df.columns)

            if grades_df.empty:
                messagebox.showinfo("Info", "No grades available to display.")
                return

            grades_df = grades_df.merge(
                students_df[['student_id', 'first_name', 'last_name']],
                on='student_id',
                how='left'
            )
            grades_df = grades_df.merge(
                courses_df[['course_id', 'course_name']],
                on='course_id',
                how='left'
            )

            display_window = tk.Toplevel(self.root)
            display_window.title("Grades List")
            display_window.geometry("600x400")

            tk.Label(display_window, text="Grades List", font=("Helvetica", 14, "bold")).pack(pady=10)

            frame = tk.Frame(display_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=canvas.yview)

            inner_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            for idx, grade in grades_df.iterrows():
                grade_info = (
                    f"Student: {grade['first_name']} {grade['last_name']} (ID: {grade['student_id']}), "
                    f"Course: {grade['course_name']} (ID: {grade['course_id']}), "
                    f"Grade: {grade['grade']}"
                )
                tk.Label(inner_frame, text=grade_info).pack(anchor="w", padx=10, pady=2)

            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        except KeyError as e:
            messagebox.showerror("Error", f"Missing column: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch grades: {e}")


if __name__ == "__main__":
    app = TeacherManagement()
    app.run()
