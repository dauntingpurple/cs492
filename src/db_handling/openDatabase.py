import pandas as pd
from sqlalchemy import create_engine

# Create an engine to connect to the SQLite database
engine = create_engine('sqlite:///student_management_system.db')

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