import tkinter as tk
from tkinter import messagebox
from src.saveChangeToDatabase import save_df_to_db, read_from_df
import pandas as pd


class CourseManagement:
    def __init__(self, parent):
        """
        Initialize the Course Management GUI within the parent frame.
        """
        self.parent = parent
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.parent, text="Course Name").grid(row=0, column=0, padx=10, pady=10)
        course_name_entry = tk.Entry(self.parent)
        course_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.parent, text="Credits").grid(row=1, column=0, padx=10, pady=10)
        credits_entry = tk.Entry(self.parent)
        credits_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(
            self.parent,
            text="Add Course",
            command=lambda: self.add_course(
                course_name_entry.get(),
                credits_entry.get()
            )
        ).grid(row=2, column=1, pady=10)

        tk.Button(self.parent, text="Display Courses", command=self.display_courses).grid(row=3, column=1, pady=10)

    def add_course(self, course_name, credits):
        try:
            if not course_name or not credits:
                messagebox.showerror("Input Error", "Both fields are required!")
                return

            if not credits.isdigit() or int(credits) <= 0:
                messagebox.showerror("Input Error", "Credits must be a positive number!")
                return

            courses_df = read_from_df('courses')

            new_course = {
                "course_id": courses_df['course_id'].max() + 1 if not courses_df.empty else 1,
                "course_name": course_name,
                "credits": int(credits)
            }
            courses_df = pd.concat([courses_df, pd.DataFrame([new_course])], ignore_index=True)

            # Convert the new course record to a DataFrame
            new_course_df = pd.DataFrame([new_course])

            # Append the new course DataFrame to the existing DataFrame
            courses_df = pd.concat([courses_df, new_course_df], ignore_index=True)

            # Save the updated DataFrame to the database
            save_df_to_db('courses', courses_df, new_index)


            messagebox.showinfo("Success", "Course added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {e}")

    def display_courses(self):
        try:
            courses_df = read_from_df('courses')

            display_window = tk.Toplevel(self.parent)
            display_window.title("Course List")
            display_window.geometry("500x400")

            tk.Label(display_window, text="Course List", font=("Helvetica", 14, "bold")).pack(pady=10)

            frame = tk.Frame(display_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=canvas.yview)

            inner_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            for idx, course in courses_df.iterrows():
                course_info = f"ID: {course['course_id']}, Name: {course['course_name']}, Credits: {course['credits']}"
                tk.Label(inner_frame, text=course_info).pack(anchor="w", padx=10, pady=2)

            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display courses: {e}")
