import tkinter as tk
from tkinter import ttk
from gui.student import StudentManagement
from gui.course import CourseManagement
from gui.enrollment import EnrollmentManagement
from gui.communication import CommunicationSystem
from gui.teacher import TeacherManagement
from gui.calendar import ClassroomSchedule


class Dashboard:
    def __init__(self, role):
        """
        Initialize the main dashboard GUI using ttk.Notebook for tab navigation.
        """
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {role}")
        self.root.geometry("1200x700")  # Ensure enough space for content
        self.role = role

        # Define colors for each tab
        self.tab_colors = {
            "Student Management": "#ffebcd",  # Blanched Almond
            "Course Management": "#add8e6",  # Light Blue
            "Enrollment Management": "#ffe4e1",  # Misty Rose
            "Classroom Schedule": "#98fb98",  # Pale Green
            "Teacher Management": "#f0e68c",  # Khaki
            "Messaging System": "#dda0dd",  # Plum
        }

        # Create Notebook widget and style it
        self.style = ttk.Style(self.root)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"), padding=[10, 5])
        self.style.configure("TNotebook", tabmargins=[5, 5, 5, 0])
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create all tabs
        self.create_tabs()

    def create_tabs(self):
        """
        Add all feature tabs to the Notebook.
        """
        self.add_tab("Student Management", StudentManagement, self.tab_colors["Student Management"])
        self.add_tab("Course Management", CourseManagement, self.tab_colors["Course Management"])
        self.add_tab("Enrollment Management", EnrollmentManagement, self.tab_colors["Enrollment Management"])
        self.add_tab("Classroom Schedule", ClassroomSchedule, self.tab_colors["Classroom Schedule"])
        self.add_tab("Teacher Management", TeacherManagement, self.tab_colors["Teacher Management"])
        if self.role in ["admin", "teacher", "student"]:
            self.add_tab("Messaging System", lambda parent: CommunicationSystem(parent, current_user=self.role),
                         self.tab_colors["Messaging System"])

    def add_tab(self, title, component_class, color):
        """
        Add a tab with a specific title and attach the corresponding component.
        """
        # Create the frame for the tab content
        frame = tk.Frame(self.notebook, bg=color)  # Use tk.Frame for easy color assignment
        self.notebook.add(frame, text=title)  # Add the frame to the Notebook
        component_class(frame)  # Initialize the content for the frame

    def run(self):
        """
        Start the Tkinter mainloop.
        """
        self.root.mainloop()


if __name__ == "__main__":
    Dashboard(role="admin").run()
