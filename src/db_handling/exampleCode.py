from src.db_handling.openDatabase import students_df, courses_df, enrollments_df, grades_df
import pandas as pd

from src.db_handling.openDatabase import assignments_df

print("Assignments DataFrame (Debug):")
print(assignments_df.head())


# Ensure the DataFrame contains data
if courses_df.empty:
    print("ERROR: 'courses_df' is empty. Verify that the database and seeding scripts are working correctly.")
    exit()

# Example Filtering Students by Date of Birth
filtered_students = students_df[students_df['date_of_birth'] < '2003-01-01']
print("\nFiltered Students (born before 2003):")
print(filtered_students)

# Example Calculating Average Grades
average_grades = grades_df.groupby('student_id')['grade'].mean().reset_index()
average_grades.columns = ['student_id', 'average_grade']
print("\nAverage Grades:")
print(average_grades)

# Example Find the Top N Students by Average Grade
top_students = average_grades.merge(students_df, on='student_id')
top_students = top_students[['first_name', 'last_name', 'average_grade']]
top_students = top_students.sort_values(by='average_grade', ascending=False).head(5)
print("\nTop 5 Students by Average Grade:")
print(top_students)

# Check for "Mathematics" Course
course_query = courses_df[courses_df['course_name'] == 'Mathematics']

if course_query.empty:
    print("\nCourse 'Mathematics' not found in the database. Adding 'Mathematics' for demonstration.")
    # Add 'Mathematics' course dynamically
    new_course = pd.DataFrame([{
        'course_id': courses_df['course_id'].max() + 1 if not courses_df.empty else 101,
        'course_name': 'Mathematics',
        'credits': 3
    }])
    courses_df = pd.concat([courses_df, new_course], ignore_index=True)
    print("\nUpdated Courses DataFrame:")
    print(courses_df)
    course_id = new_course['course_id'].values[0]
else:
    course_id = course_query['course_id'].values[0]

# Fetch students enrolled in the "Mathematics" course
enrolled_students = enrollments_df[enrollments_df['course_id'] == course_id]

if enrolled_students.empty:
    print("\nNo students are enrolled in 'Mathematics'.")
else:
    student_ids = enrolled_students['student_id'].unique()
    students_in_course = students_df[students_df['student_id'].isin(student_ids)]
    print("\nStudents enrolled in Mathematics:")
    print(students_in_course)
