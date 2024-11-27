import tkinter as tk
from gui.student import StudentManagement  # Import the StudentManagement GUI

class Dashboard:
    def __init__(self, role):
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {role}")
        self.role = role

    def open_student_management(self):
        self.root.destroy()  # Close the dashboard window
        StudentManagement().run()  # Open the Student Management GUI

    def run(self):
        # Add welcome label
        tk.Label(self.root, text=f"Welcome to the {self.role} Dashboard!").pack(pady=20)

        # Add buttons based on the role
        if self.role == "Admin":
            tk.Button(self.root, text="Manage Students", command=self.open_student_management).pack(pady=5)
        elif self.role == "Teacher":
            tk.Button(self.root, text="Enter Grades", command=self.enter_grades).pack(pady=5)
        elif self.role == "Registrar":
            tk.Button(self.root, text="Manage Enrollments", command=self.manage_enrollments).pack(pady=5)
        elif self.role == "Student":
            tk.Button(self.root, text="View Grades", command=self.view_grades).pack(pady=5)

        # Add logout button
        tk.Button(self.root, text="Logout", command=self.root.destroy).pack(pady=20)

        # Start the mainloop
        self.root.mainloop()

    # Placeholder methods for functionality
    def enter_grades(self):
        print("Teacher: Entering Grades")

    def manage_enrollments(self):
        print("Registrar: Managing Enrollments")

    def view_grades(self):
        print("Student: Viewing Grades")
