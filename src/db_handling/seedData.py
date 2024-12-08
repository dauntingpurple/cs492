import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# This is solely to generate fake data for the database

# Initialize Faker for generating random data
fake = Faker()

# Set a random seed for reproducibility
np.random.seed(42)

# Generate seed data for Students
num_students = 10
students_data = {
    'first_name': [fake.first_name() for _ in range(num_students)],
    'last_name': [fake.last_name() for _ in range(num_students)],
    'date_of_birth': [fake.date_of_birth(minimum_age=18, maximum_age=25) for _ in range(num_students)],
    'address': [fake.address().replace("\n", ", ") for _ in range(num_students)],
    'email': [fake.email() for _ in range(num_students)]
}
students_df = pd.DataFrame(students_data)
students_df["student_id"] = students_df.index

# Create Teachers DataFrame
num_teachers = 3
teachers_df = {
    'first_name': [fake.first_name() for _ in range(num_teachers)],
    'last_name': [fake.last_name() for _ in range(num_teachers)],
    'qualifications': [fake.random_element(elements=('M.Ed', 'Ph.D.', 'B.Ed.', 'M.A.', 'M.Sc.')) for _ in range(num_teachers)],
    'course_name': [fake.word().capitalize() + " 101" for _ in range(num_teachers)]
}
teachers_df = pd.DataFrame(teachers_df)
teachers_df["teacher_id"] = teachers_df.index

# Generate seed data for Courses
num_courses = 5
courses_data = {
    'course_id': np.arange(101, 101 + num_courses),
    'course_name': [fake.word().capitalize() + " 101" for _ in range(num_courses)],
    'credits': np.random.choice([3, 4], size=num_courses)
}
courses_df = pd.DataFrame(courses_data)

# Generate seed data for Enrollments
num_enrollments = 15
enrollments_data = {
    'student_id': np.random.choice(students_df['student_id'], size=num_enrollments),
    'course_id': np.random.choice(courses_df['course_id'], size=num_enrollments)
}
enrollments_df = pd.DataFrame(enrollments_data)
enrollments_df["enrollment_id"] = enrollments_df.index

# Create Grades DataFrame
grades_data = {
    'student_id': np.random.choice(students_df['student_id'], size=200),
    'enrollments_id': np.random.choice(enrollments_df['enrollment_id'], size=200),
    'grade': np.random.uniform(0, 100, size=200)  # Random grades between 0 and 100
}
grades_df = pd.DataFrame(grades_data)
grades_df["grade_id"] = grades_df.index

# Create Calendar Scheduling Data
num_events = 10
base_date = datetime.now()

calendar_data = {
    'classroom_name': [f"Room {np.random.randint(100, 200)}" for _ in range(num_events)],
    'start_time': [(base_date + timedelta(days=i, hours=9)).strftime("%Y-%m-%d %H:%M:%S") for i in range(num_events)],
    'end_time': [(base_date + timedelta(days=i, hours=10)).strftime("%Y-%m-%d %H:%M:%S") for i in range(num_events)],
    'reserved_by': [fake.name() for _ in range(num_events)],
    'purpose': [fake.word().capitalize() + " Meeting" for _ in range(num_events)]
}
calendar_df = pd.DataFrame(calendar_data)

# Initialize Audit Logs and Messages
audit_log_df = {
    'change_id': [0],
    'table_name': ["test"],
    'record_id': ["0"],
    'change_type': ["INSERT"],
    'change_timestamp': [datetime.now()],
    'changed_by': ["admin"]
}

messages_df = {
    'sender': ["test"],
    'receiver': ["test1"],
    'message_text': ["test1"],
    'timestamp': [datetime.now()],
    'is_read': [False]
}

# Display the generated data
print("Students DataFrame:")
print(students_df)
print("\nCourses DataFrame:")
print(courses_df)
print("\nEnrollments DataFrame:")
print(enrollments_df)
print("\nGrade DataFrame:")
print(grades_df)
print("\nCalendar Scheduling DataFrame:")
print(calendar_df)

# Create a SQLite database
engine = create_engine('sqlite:///school_management_system.db')

# Save the generated DataFrames to the database
pd.DataFrame(audit_log_df).to_sql('audit_log', con=engine, if_exists='replace', index=False)
pd.DataFrame(messages_df).to_sql('messages', con=engine, if_exists='replace', index=False)
students_df.to_sql('students', con=engine, if_exists='replace', index=False)
courses_df.to_sql('courses', con=engine, if_exists='replace', index=False)
enrollments_df.to_sql('enrollments', con=engine, if_exists='replace', index=False)
grades_df.to_sql('grades', con=engine, if_exists='replace', index=False)
calendar_df.to_sql('classroom_schedules', con=engine, if_exists='replace', index=False)
