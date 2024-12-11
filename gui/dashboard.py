import tkinter as tk
from gui.student import StudentManagement
from gui.course import CourseManagement
from gui.enrollment import EnrollmentManagement
from gui.communication import CommunicationSystem
from gui.teacher import GradeEntry
from gui.calendar import ClassroomSchedule  # Import Classroom Schedule Management


class Dashboard:
    def __init__(self, role):
        """
        Initializes the main dashboard based on the user's role.
        """
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {role}")
        self.role = role

    def open_student_management(self):
        """
        Opens the Student Management GUI.
        """
        StudentManagement()

    def open_course_management(self):
        """
        Opens the Course Management GUI.
        """
        CourseManagement()

    def open_enrollment_management(self):
        """
        Opens the Enrollment Management GUI.
        """
        EnrollmentManagement()

    def open_communication_system(self):
        """
        Opens the Messaging System GUI.
        """
        communication_window = tk.Toplevel(self.root)
        CommunicationSystem(communication_window, current_user=self.role)

    def enter_grades(self):
        """
        Opens the Grade Entry GUI for teachers.
        """
        GradeEntry()

    def open_classroom_schedule(self):
        """
        Opens the Classroom Schedule Management GUI.
        """
        ClassroomSchedule()

    def run(self):
        """
        Runs the main dashboard GUI.
        """
        tk.Label(self.root, text=f"Welcome to the {self.role} Dashboard!", font=("Arial", 16)).pack(pady=20)

        if self.role == "admin":
            tk.Button(self.root, text="Manage Students", command=self.open_student_management).pack(pady=5)
            tk.Button(self.root, text="Manage Courses", command=self.open_course_management).pack(pady=5)
            tk.Button(self.root, text="Manage Enrollments", command=self.open_enrollment_management).pack(pady=5)
            tk.Button(self.root, text="Messaging System", command=self.open_communication_system).pack(pady=5)
            tk.Button(self.root, text="Classroom Schedules", command=self.open_classroom_schedule).pack(pady=5)
        elif self.role == "teacher":
            tk.Button(self.root, text="Enter Grades", command=self.enter_grades).pack(pady=5)
            tk.Button(self.root, text="Messaging System", command=self.open_communication_system).pack(pady=5)
            tk.Button(self.root, text="Classroom Schedules", command=self.open_classroom_schedule).pack(pady=5)
        elif self.role == "registrar":
            tk.Button(self.root, text="Manage Enrollments", command=self.open_enrollment_management).pack(pady=5)
            tk.Button(self.root, text="Classroom Schedules", command=self.open_classroom_schedule).pack(pady=5)
        elif self.role == "student":
            tk.Button(self.root, text="Messaging System", command=self.open_communication_system).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.root.destroy).pack(pady=20)

        self.root.mainloop()


if __name__ == "__main__":
    dashboard = Dashboard(role="Admin")  # Example: Start as Admin
    dashboard.run()
