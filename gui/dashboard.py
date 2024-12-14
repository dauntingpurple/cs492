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
        self.style.configure(
            "TNotebook.Tab",
            font=("Helvetica", 12, "bold"),  # Adjust font and boldness
            padding=[10, 5],  # Add spacing around tabs
        )
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add tabs
        self.create_tabs()

        # Add Exit button
        self.add_exit_button()

        # Fix tab colors
        self.fix_tab_colors()

    def create_tabs(self):
        """
        Add all feature tabs to the Notebook.
        """
        self.frames = {}  # Store frames to access them later for styling

        # Add Student Management Tab
        self.frames["Student Management"] = self.add_tab("Student Management", StudentManagement)

        # Add Course Management Tab
        self.frames["Course Management"] = self.add_tab("Course Management", CourseManagement)

        # Add Enrollment Management Tab
        self.frames["Enrollment Management"] = self.add_tab("Enrollment Management", EnrollmentManagement)

        # Add Classroom Schedule Tab
        self.frames["Classroom Schedule"] = self.add_tab("Classroom Schedule", ClassroomSchedule)

        # Add Teacher Management Tab
        self.frames["Teacher Management"] = self.add_tab("Teacher Management", TeacherManagement)

        # Add Messaging System Tab (only for admin, teacher, or student roles)
        if self.role in ["admin", "teacher", "student"]:
            self.frames["Messaging System"] = self.add_tab(
                "Messaging System", lambda parent: CommunicationSystem(parent, current_user=self.role)
            )

    def add_tab(self, title, component_class):
        """
        Add a tab with a specific title and attach the corresponding component.
        """
        # Create the frame for the tab content
        frame = tk.Frame(self.notebook, bg=self.tab_colors[title])
        self.notebook.add(frame, text=title)  # Add the frame to the Notebook
        component_class(frame)  # Initialize the content for the frame
        return frame

    def add_exit_button(self):
        """
        Add an always-visible Exit button at the bottom right of the dashboard.
        """
        exit_button_frame = tk.Frame(self.root)
        exit_button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        exit_button = tk.Button(
            exit_button_frame,
            text="Exit",
            font=("Helvetica", 12, "bold"),
            bg="#ff4d4d",
            fg="white",
            command=self.exit_application,
        )
        exit_button.pack(side=tk.RIGHT, padx=10)

    def fix_tab_colors(self):
        """
        Update tab styles to match their corresponding background colors.
        """
        for idx, tab_name in enumerate(self.frames):
            self.notebook.tab(idx, background=self.tab_colors[tab_name])  # Update the tab background

    def exit_application(self):
        """
        Close the application when the Exit button is clicked.
        """
        self.root.destroy()

    def run(self):
        """
        Start the Tkinter mainloop.
        """
        self.root.mainloop()


if __name__ == "__main__":
    Dashboard(role="admin").run()
