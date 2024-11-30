import os
from sqlalchemy import create_engine
import pandas as pd

print(f"Using database at: {DB_PATH}")

# Determine if the app is running in a PyInstaller bundle
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS  # PyInstaller extracts files to this directory
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Normal script directory

DB_PATH = os.path.join(BASE_DIR, 'school_management_system.db')

# Check if the database file exists
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database file not found at {DB_PATH}")

# Create an engine to connect to the SQLite database
engine = create_engine(f'sqlite:///{DB_PATH}')

# Load data from the database tables
students_df = pd.read_sql('SELECT * FROM students', con=engine)
courses_df = pd.read_sql('SELECT * FROM courses', con=engine)
enrollments_df = pd.read_sql('SELECT * FROM enrollments', con=engine)
assignments_df = pd.read_sql('SELECT * FROM assignments', con=engine)
grades_df = pd.read_sql('SELECT * FROM grades', con=engine)



# Display the loaded DataFrames
# The following can be removed once we are further and don't need to troubleshoot
print("Students DataFrame:")
print(students_df.head())

print("\nCourses DataFrame:")
print(courses_df.head())

print("\nEnrollments DataFrame:")
print(enrollments_df.head())

print("\nAssignments DataFrame:")
print(assignments_df.head())

print("\nGrades DataFrame:")
print(grades_df.head())

# DataFrames are now in memory and will be used during runtime
# Changes to these DataFrames should be explicitly saved using saveChangeToDatabase.py