import tkinter as tk
from gui.student import StudentManagement
from gui.course import CourseManagement
from gui.enrollment import EnrollmentManagement
from gui.communication import CommunicationSystem
from gui.teacher import GradeEntry  # Import GradeEntry from teacher.py


class Dashboard:
    def __init__(self, role):
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {role}")
        self.role = role

    def open_student_management(self):
        StudentManagement()

    def open_course_management(self):
        CourseManagement()

    def open_enrollment_management(self):
        EnrollmentManagement()

    def open_communication_system(self):
        communication_window = tk.Toplevel(self.root)
        CommunicationSystem(communication_window, current_user=self.role)

    def enter_grades(self):
        """
        Opens the Grade Entry GUI for teachers.
        """
        GradeEntry()  # Initializes and opens the grade entry window

    def run(self):
        tk.Label(self.root, text=f"Welcome to the {self.role} Dashboard!", font=("Arial", 16)).pack(pady=20)

        if self.role == "Admin":
            tk.Button(self.root, text="Manage Students", command=self.open_student_management).pack(pady=5)
            tk.Button(self.root, text="Manage Courses", command=self.open_course_management).pack(pady=5)
            tk.Button(self.root, text="Manage Enrollments", command=self.open_enrollment_management).pack(pady=5)
            tk.Button(self.root, text="Messaging System", command=self.open_communication_system).pack(pady=5)
        elif self.role == "Teacher":
            tk.Button(self.root, text="Enter Grades", command=self.enter_grades).pack(pady=5)
            tk.Button(self.root, text="Messaging System", command=self.open_communication_system).pack(pady=5)
        elif self.role == "Registrar":
            tk.Button(self.root, text="Manage Enrollments", command=self.open_enrollment_management).pack(pady=5)
        elif self.role == "Student":
            tk.Button(self.root, text="View Grades", command=self.view_grades).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.root.destroy).pack(pady=20)

        self.root.mainloop()

    def view_grades(self):
        print("Student: Viewing Grades")


if __name__ == "__main__":
    dashboard = Dashboard(role="Teacher")  # Example: Start as Teacher
    dashboard.run()
