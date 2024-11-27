import pandas as pd
import numpy as np
from sqlalchemy import create_engine

## This is for if we want to use 'real data' and not the seedData

# Define the Students table
students_data = {
    'student_id': [1, 2, 3],
    'first_name': ['John', 'Jane', 'Jim'],
    'last_name': ['Doe', 'Smith', 'Brown'],
    'date_of_birth': pd.to_datetime(['2000-01-01', '2001-02-02', '2002-03-03'])
}
students_df = pd.DataFrame(students_data)

# Define the Courses table
courses_data = {
    'course_id': [101, 102, 103],
    'course_name': ['Mathematics', 'Science', 'History'],
    'credits': [3, 4, 3]
}
courses_df = pd.DataFrame(courses_data)

# Define the Enrollments table
enrollments_data = {
    'enrollment_id': [1, 2, 3],
    'student_id': [1, 2, 3],
    'course_id': [101, 102, 103],
    'enrollment_date': pd.to_datetime(['2023-08-01', '2023-08-01', '2023-08-02'])
}
enrollments_df = pd.DataFrame(enrollments_data)

# Create Assignments DataFrame
assignments_data = {
    'assignment_id': [1, 2, 3],
    'course_id': [101, 102, 103],
    'title': ['Assignment_1', 'Assignment_2', 'Assignment_3'],
}
assignments_df = pd.DataFrame(assignments_data)

# Create Grades DataFrame
grades_data = {
    'grade_id': [1, 2, 3],
    'student_id': [1, 2, 3],
    'assignment_id': [1, 2, 3],
    'grade': [99, 94, 93],
}
grades_df = pd.DataFrame(grades_data)

# Display the DataFrames
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

# Create a SQLite database
engine = create_engine('sqlite:///school_management_system.db')

# Save DataFrames to the database
students_df.to_sql('students', con=engine, if_exists='replace', index=False)
courses_df.to_sql('courses', con=engine, if_exists='replace', index=False)
enrollments_df.to_sql('enrollments', con=engine, if_exists='replace', index=False)
assignments_df.to_sql('assignments', con=engine, if_exists='replace', index=False)
grades_df.to_sql('grades', con=engine, if_exists='replace', index=False)