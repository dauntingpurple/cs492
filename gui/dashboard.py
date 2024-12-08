import tkinter as tk
from gui.student import StudentManagement  # Import the Student Management GUI
from gui.course import CourseManagement  # Import the Course Management GUI
from gui.enrollment import EnrollmentManagement  # Import the Enrollment Management GUI


class Dashboard:
    def __init__(self, role):
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {role}")
        self.role = role

    def open_student_management(self):
        StudentManagement()  # Directly instantiate the class

    def open_course_management(self):
        CourseManagement()  # Directly instantiate the class

    def open_enrollment_management(self):
        EnrollmentManagement()  # Directly instantiate the class

    def run(self):
        # Add welcome label
        tk.Label(self.root, text=f"Welcome to the {self.role} Dashboard!", font=("Arial", 16)).pack(pady=20)

        # Add buttons based on the role
        if self.role == "Admin":
            tk.Button(self.root, text="Manage Students", command=self.open_student_management).pack(pady=5)
            tk.Button(self.root, text="Manage Courses", command=self.open_course_management).pack(pady=5)
            tk.Button(self.root, text="Manage Enrollments", command=self.open_enrollment_management).pack(pady=5)
        elif self.role == "Teacher":
            tk.Button(self.root, text="Enter Grades", command=self.enter_grades).pack(pady=5)
        elif self.role == "Registrar":
            tk.Button(self.root, text="Manage Enrollments", command=self.open_enrollment_management).pack(pady=5)
        elif self.role == "Student":
            tk.Button(self.root, text="View Grades", command=self.view_grades).pack(pady=5)

        # Add logout button
        tk.Button(self.root, text="Logout", command=self.root.destroy).pack(pady=20)

        # Start the mainloop
        self.root.mainloop()

    # Placeholder methods for functionality
    def enter_grades(self):
        print("Teacher: Entering Grades")

    def view_grades(self):
        print("Student: Viewing Grades")


if __name__ == "__main__":
    dashboard = Dashboard(role="Admin")  # Example: Start as Admin
    dashboard.run()
