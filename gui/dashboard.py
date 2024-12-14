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
        Initialize the main dashboard GUI with vertical tabs on the left.
        """
        self.root = tk.Tk()
        self.root.title(f"Dashboard - {role}")
        self.root.geometry("1200x700")
        self.role = role

        # Define colors for each tab
        self.tab_colors = {
            "Student Management": "#ffebcd",
            "Course Management": "#add8e6",
            "Enrollment Management": "#ffe4e1",
            "Classroom Schedule": "#98fb98",
            "Teacher Management": "#f0e68c",
            "Messaging System": "#dda0dd",
        }

        # Create main frame for layout
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the tab frame
        self.tab_frame = tk.Frame(main_frame)
        self.tab_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create the content frame
        self.content_frame = tk.Frame(main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12, "bold"), padding=5)

        # Add tabs
        self.create_tabs()

        # Add Exit button
        self.add_exit_button()

    def create_tabs(self):
        """
        Add all feature tabs to the tab frame.
        """
        self.frames = {}

        # Create buttons for tabs
        for title in self.tab_colors.keys():
            button = tk.Button(self.tab_frame, text=title, command=lambda t=title: self.show_tab(t))
            button.pack(fill=tk.X, padx=5, pady=5)
            self.frames[title] = self.add_tab(title)

    def add_tab(self, title):
        """
        Create the content frame for the selected tab.
        """
        frame = tk.Frame(self.content_frame, bg=self.tab_colors[title])
        # Initialize the corresponding component (assuming it returns a frame)
        if title == "Student Management":
            StudentManagement(frame)
        elif title == "Course Management":
            CourseManagement(frame)
        elif title == "Enrollment Management":
            EnrollmentManagement(frame)
        elif title == "Classroom Schedule":
            ClassroomSchedule(frame)
        elif title == "Teacher Management":
            TeacherManagement(frame)
        elif title == "Messaging System" and self.role in ["admin", "teacher", "student"]:
            CommunicationSystem(frame, current_user=self.role)
        
        return frame

    def show_tab(self, title):
        """
        Show the selected tab and hide others.
        """
        for frame in self.frames.values():
            frame.pack_forget()  # Hide all frames
        self.frames[title].pack(fill=tk.BOTH, expand=True)  # Show selected frame

    def add_exit_button(self):
        """
        Add an Exit button at the bottom right of the dashboard.
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

    def exit_application(self):
        """
        Close the application when the Exit button is clicked.
        """
        self.root.destroy()

    def run(self):
        """
        Start the Tkinter mainloop.
        """
        self.show_tab(list(self.tab_colors.keys())[0])  # Show the first tab by default
        self.root.mainloop()


if __name__ == "__main__":
    Dashboard(role="admin").run()