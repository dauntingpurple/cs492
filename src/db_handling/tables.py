import pandas as pd
from sqlalchemy import create_engine

## This is for if we want to use 'real data' and not the seedData

# Define the Students table
students_data = {
    'first_name': ['John', 'Jane', 'Jim'],
    'last_name': ['Doe', 'Smith', 'Brown'],
    'date_of_birth': pd.to_datetime(['2000-01-01', '2001-02-02', '2002-03-03']),
    'address' : ['123 Main St, Springfield, OH', '95 Donahue Blvd, Appleton, WI', '802 Salebarn Rd, Fort Pierre, SD'],
    'email' : ['john.doe@example.com', 'jane.smith@testmail.org', 'brownj@dummydata.net']
}
students_df = pd.DataFrame(students_data)
students_df["student_id"] = students_df.index

# Create Teachers DataFrame
teachers_df = {
    'first_name': ['Alice', 'Bob', 'Carol'],
    'last_name': ['Smith', 'Johnson', 'Williams'],
    'qualifications': ['M.Ed', 'Ph.D.', 'B.Ed.'],
    'course_name': ['Mathematics', 'Science', 'English']
}
teachers_df = pd.DataFrame(teachers_df)
teachers_df["teacher_id"] = teachers_df.index

# Define the Courses table
courses_data = {
    'course_id': [101, 102, 103],
    'course_name': ['Mathematics', 'Science', 'History'],
    'credits': [3, 4, 3]
}
courses_df = pd.DataFrame(courses_data)

# Define the Enrollments table
enrollments_data = {
    'student_id': [1, 2, 3],
    'course_id': [101, 102, 103],
    'semester': ['Fall', 'Fall', 'Fall'],
    'year': [2023, 2023, 2023]
}
enrollments_df = pd.DataFrame(enrollments_data)
enrollments_df["enrollment_id"] = enrollments_df.index

# Create Grades DataFrame
grades_data = {
    'student_id': [1, 2, 3],
    'assignment_id': [1, 2, 3],
    'grade': [99, 94, 93],
}
grades_df = pd.DataFrame(grades_data)
grades_df["grade_id"] = grades_df.index

audit_log_columns = ['change_id', 'table_name', 'record_id', 'change_type', 'change_timestamp', 'changed_by', 'old_value', 'new_value']
audit_log_df = pd.DataFrame(columns=audit_log_columns)
messages_df_columns = ['sender', 'receiver', 'message_text', 'timestamp', 'is_read']
messages_df = pd.DataFrame(columns=messages_df_columns)

# Display the DataFrames
print("Students DataFrame:")
print(students_df.head())
print("\nCourses DataFrame:")
print(courses_df.head())
print("\nEnrollments DataFrame:")
print(enrollments_df.head())
print("\nGrades DataFrame:")
print(grades_df.head())

# Create a SQLite database
engine = create_engine('sqlite:///school_management_system.db')

# Save DataFrames to the database
students_df.to_sql('students', con=engine, if_exists='replace', index=False)
teachers_df.to_sql('teachers', con=engine, if_exists='replace', index=False)
courses_df.to_sql('courses', con=engine, if_exists='replace', index=False)
enrollments_df.to_sql('enrollments', con=engine, if_exists='replace', index=False)
grades_df.to_sql('grades', con=engine, if_exists='replace', index=False)
audit_log_df.to_sql('audit_log', con=engine, if_exists='replace', index=False)
messages_df.to_sql('messages', con=engine, if_exists='replace', index=False)