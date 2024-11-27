Setup Process Document: School Database Management System

1. Overview

This project is a school management system with a tkinter GUI for managing students, courses, and enrollments, and it integrates with an SQLite database. It uses Python for backend and tkinter for the frontend.


2. Prerequisites

2.1 Software Requirements
Python 3.8 or later
Visual Studio Code (VS Code) or any Python IDE
SQLite (installed with Python by default)
Required Python libraries:
sqlalchemy
pandas


3. Project Structure

Below is the expected directory structure for the project:

school_management_system/
├── main.py                # Main entry point of the application
├── gui/
│   ├── __init__.py        # Makes gui a package
│   ├── login.py           # Login screen
│   ├── dashboard.py       # Dashboard for different roles
│   ├── students.py        # Student management GUI
│   ├── courses.py         # Course management GUI (if needed)
│   ├── enrollments.py     # Enrollment management GUI (if needed)
├── schoolDatabase.py      # Handles database connections
├── schema.md              # Database schema documentation
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── school_management_system.db # SQLite database file


4. Installation Steps

4.1 Clone the Repository

Create a directory where you want to store the project.
If the project is stored in a Git repository, run:

bash
git clone <repository_url>
Navigate to the project directory:

bash
cd school_management_system

4.2 Set Up a Virtual Environment

Create a virtual environment:
bash
python -m venv .venv
Activate the virtual environment:


bash
.\.venv\Scripts\Activate


bash
pip install -r requirements.txt
Verify installation:
bash
pip list
Ensure sqlalchemy, pandas, and other required libraries are installed.

4.3 Create or Verify the Database

Ensure the SQLite database file (school_management_system.db) exists in the project root.

If the database is missing, create it by running schoolDatabase.py:

bash
python schoolDatabase.py
Verify that the students table and other necessary tables exist. Use an SQLite client or a Python script:

sql
SELECT * FROM students;


5. Running the Application

5.1 Launch the Application
Run the main.py file:
bash
python main.py
The application will launch a login screen.

6. Testing the Features

6.1 Logging In
Use predefined usernames and passwords based on roles:
Admin: username = admin, password = admin123
Teacher: username = teacher, password = teacher123
Registrar: username = registrar, password = registrar123
Student: username = student, password = student123

6.2 Managing Students
Navigate to Student Management via the dashboard.
Use the Add Student button to insert student data (First Name, Last Name, Date of Birth).
Use the Display Students button to view all students in a scrollable GUI.

6.3 Managing Courses
(If implemented) Navigate to Course Management to add or view courses.

6.4 Managing Enrollments
(If implemented) Navigate to Enrollment Management to enroll students in courses.


7. Additional Notes

7.1 Debugging
If the application doesn’t launch, check for missing libraries or syntax errors in the terminal.
Use print statements in code to debug database queries or GUI logic.


7.2 Editing the Database
Use a tool like DB Browser for SQLite to inspect and modify the database manually.

7.3 Adding More Features
To extend the system, add new GUIs for course and enrollment management.
Update the database schema as required.