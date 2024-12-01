import os
import sys
from sqlalchemy import create_engine
import pandas as pd

# Detect if running in a PyInstaller bundle
if hasattr(sys, "_MEIPASS"):
    ROOT_DIR = sys._MEIPASS  # PyInstaller extracts files to this directory
else:
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))  # Script or .exe location

# Define the database path
DB_PATH = os.path.join(ROOT_DIR, 'school_management_system.db')

# Print the database path for debugging purposes
print(f"Using database at: {DB_PATH}")

# Check if the database file exists
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database file not found at {DB_PATH}")

# Create an engine to connect to the SQLite database
engine = create_engine(f'sqlite:///{DB_PATH}')

# Load data from the database tables
try:
    # Load the tables into pandas DataFrames
    students_df = pd.read_sql('SELECT * FROM students', con=engine)
    courses_df = pd.read_sql('SELECT * FROM courses', con=engine)
    enrollments_df = pd.read_sql('SELECT * FROM enrollments', con=engine)
    assignments_df = pd.read_sql('SELECT * FROM assignments', con=engine)
    grades_df = pd.read_sql('SELECT * FROM grades', con=engine)

    # Debugging: Display the first few rows of each DataFrame
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
except Exception as e:
    # Print an error message if there is an issue loading the database
    print(f"Error loading data from the database: {e}")
    raise

# The DataFrames are now available for use during runtime
# Any changes to these DataFrames should be saved explicitly using saveChangeToDatabase.py
