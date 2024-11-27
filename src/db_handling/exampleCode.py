from src.db_handling.openDatabase import students_df, courses_df,enrollments_df, assignments_df, grades_df 

## Example Filtering Students by Date of Birth
filtered_students = students_df[students_df['date_of_birth'] < '2003-01-01']
print("\nFiltered Students (born before 2003):")
print(filtered_students)

## Example Calculating Average Grades
average_grades = grades_df.groupby('student_id')['grade'].mean().reset_index()
average_grades.columns = ['student_id', 'average_grade']
print("\nAverage Grades:")
print(average_grades)

## Example Find the Top N Students by Average Grade
# Use Example Above Calculating Average Grades
# Merge with students to get names
top_students = average_grades.merge(students_df, on='student_id')
top_students = top_students[['first_name', 'last_name', 'average_grade']]
# Sort and get top 5
top_students = top_students.sort_values(by='average_grade', ascending=False).head(5)
print("\nTop 5 Students by Average Grade:")
print(top_students)

## Example All Students Enrolled in a Specific Course
# Get the course_id for 'Mathematics'
course_id = courses_df[courses_df['course_name'] == 'Mathematics']['course_id'].values[0]
# Find students enrolled in this course
enrolled_students = enrollments_df[enrollments_df['course_id'] == course_id]
student_ids = enrolled_students['student_id'].unique()
# Retrieve student details
students_in_course = students_df[students_df['student_id'].isin(student_ids)]
print("Students enrolled in Mathematics:")
print(students_in_course)