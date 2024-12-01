import tkinter as tk
from tkinter import ttk, messagebox
from src.db_handling.openDatabase import courses_df
import pandas as pd

class CourseManagement:
    def __init__(self, go_back_callback):
        self.go_back_callback = go_back_callback
        self.root = tk.Toplevel()  # Use Toplevel for the course management window
        self.root.title("Course Management")

    def add_course(self, course_name, credits):
        global courses_df
        try:
            new_id = courses_df['course_id'].max() + 1 if not courses_df.empty else 101
            new_course = {
                'course_id': new_id,
                'course_name': course_name,
                'credits': int(credits)
            }
            courses_df = pd.concat([courses_df, pd.DataFrame([new_course])], ignore_index=True)
            messagebox.showinfo("Success", "Course added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {e}")

    def display_courses(self):
        display_window = tk.Toplevel(self.root)
        display_window.title("Courses List")
        display_window.geometry("600x400")

        tree = ttk.Treeview(display_window, columns=("Course ID", "Course Name", "Credits"), show="headings")
        tree.heading("Course ID", text="Course ID")
        tree.heading("Course Name", text="Course Name")
        tree.heading("Credits", text="Credits")
        tree.column("Course ID", width=100, anchor="center")
        tree.column("Course Name", width=300, anchor="center")
        tree.column("Credits", width=100, anchor="center")

        for _, row in courses_df.iterrows():
            tree.insert("", "end", values=(row["course_id"], row["course_name"], row["credits"]))

        scrollbar = ttk.Scrollbar(display_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")
        tk.Button(display_window, text="Close", command=display_window.destroy).pack(pady=10)

    def go_back(self):
        self.root.destroy()
        self.go_back_callback()  # Call the go-back callback to show the dashboard

    def run(self):
        tk.Label(self.root, text="Course Management", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Add Course", command=lambda: self.add_course("New Course", 3)).pack(pady=5)
        tk.Button(self.root, text="Show Courses", command=self.display_courses).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=10)
        self.root.mainloop()