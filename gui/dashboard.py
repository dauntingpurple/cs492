import tkinter as tk
from tkinter import ttk
from gui.student import StudentManagement
from gui.course import CourseManagement
from gui.enrollment import EnrollmentManagement
from gui.communication import CommunicationSystem
from gui.teacher import TeacherManagement, GradeEntry
from gui.calendar import ClassroomSchedule


class Dashboard:
    def __init__(self, role):
        """
        Initialize the main dashboard GUI using ttk.Notebook for tab navigation.
        """
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {role}")
        self.root.geometry("900x600")
        self.role = role

        # Create the notebook widget
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add tabs
        self.add_student_management_tab()
        self.add_course_management_tab()
        self.add_enrollment_management_tab()
        self.add_classroom_schedule_tab()
        self.add_teacher_management_tab()

        # Add communication system tab
        if role in ["admin", "teacher", "student"]:
            self.add_communication_tab()

    def add_student_management_tab(self):
        """
        Add the Student Management tab.
        """
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="Student Management")
        StudentManagement(student_frame)

    def add_course_management_tab(self):
        """
        Add the Course Management tab.
        """
        course_frame = ttk.Frame(self.notebook)
        self.notebook.add(course_frame, text="Course Management")
        CourseManagement(course_frame)

    def add_enrollment_management_tab(self):
        """
        Add the Enrollment Management tab.
        """
        enrollment_frame = ttk.Frame(self.notebook)
        self.notebook.add(enrollment_frame, text="Enrollment Management")
        EnrollmentManagement(enrollment_frame)

    def add_classroom_schedule_tab(self):
        """
        Add the Classroom Schedule tab.
        """
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="Classroom Schedule")
        ClassroomSchedule(schedule_frame)

    def add_teacher_management_tab(self):
        """
        Add the Teacher Management tab.
        """
        teacher_frame = ttk.Frame(self.notebook)
        self.notebook.add(teacher_frame, text="Teacher Management")
        TeacherManagement(teacher_frame)

    def add_communication_tab(self):
        """
        Add the Messaging System tab.
        """
        communication_frame = ttk.Frame(self.notebook)
        self.notebook.add(communication_frame, text="Messaging System")
        CommunicationSystem(communication_frame, current_user=self.role)

    def run(self):
        """
        Start the Tkinter mainloop.
        """
        self.root.mainloop()


if __name__ == "__main__":
    Dashboard(role="admin").run()
