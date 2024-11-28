import pandas as pd
from sqlalchemy import create_engine

# I don't know if you want to run this as it is or pull the data separately

# Create an engine to connect to the SQLite database
engine = create_engine('sqlite:///school_management_system.db')

# Load data into DataFrames
students_df = pd.read_sql('SELECT * FROM students', con=engine)
courses_df = pd.read_sql('SELECT * FROM courses', con=engine)
enrollments_df = pd.read_sql('SELECT * FROM enrollments', con=engine)
assignments_df = pd.read_sql('SELECT * FROM assignments', con=engine)
grades_df = pd.read_sql('SELECT * FROM grades', con=engine)

## Overall Performance Report
# Calculate average grades for each student by semester and year
student_average_grades = (grades_df.groupby(['student_id', 'semester', 'year'])['grade'].mean().reset_index())
student_average_grades.columns = ['student_id', 'semester', 'year', 'average_grade']
# Count total grades recorded for each student by semester and year
grades_count = (grades_df.groupby(['student_id', 'semester', 'year'])['grade'].count().reset_index())
grades_count.columns = ['student_id', 'semester', 'year', 'total_grades']
# Merge the two DataFrames
overall_performance = student_average_grades.merge(grades_count, on=['student_id', 'semester', 'year'])
# Merge with students to include names
overall_performance = overall_performance.merge(students_df[['student_id', 'first_name', 'last_name']], on='student_id')
# Display the overall performance report
print("\nOverall Performance Report:")
print(overall_performance[['first_name', 'last_name', 'semester', 'year', 'average_grade', 'total_grades']])

## Course-Specific Performance Report
# Merge grades with enrollments to get course information
grades_with_enrollments = (grades_df.merge(enrollments_df[['student_id', 'course_id', 'semester', 'year']], on=['student_id', 'semester', 'year']))
# Group by course_id, semester, and year to calculate average grade
average_grades_by_course = (grades_with_enrollments.groupby(['course_id', 'semester', 'year'])['grade'].mean().reset_index())
average_grades_by_course = average_grades_by_course.merge(courses_df[['course_id', 'course_name']], on='course_id')
# Display the course performance report
print("\nCourse-Specific Performance Report:")
print(average_grades_by_course[['course_name', 'semester', 'year', 'grade']])

## Top 5 Students by Average Grade
# Specify the semester and year for analysis
specified_semester = 'Fall'
specified_year = 2023
# Calculate average grades for each student for the specified semester and year
top_students = (grades_df[(grades_df['semester'] == specified_semester) & (grades_df['year'] == specified_year)].groupby('student_id')['grade'].mean().reset_index(name='average_grade'))
# Merge with students to get names
top_students = top_students.merge(students_df, on='student_id')
# Sort and get top 5
top_students = top_students.sort_values(by='average_grade', ascending=False).head(5)
print("\nTop 5 Students by Average Grade:")
print(top_students[['first_name', 'last_name', 'average_grade']])

## Export Reports

# Save reports as CSV files
overall_performance.to_csv('overall_performance_report.csv', index=False)
average_grades_by_course.to_csv('course_performance_report.csv', index=False)
top_students.to_csv('top_students_report.csv', index=False)

# Save reports to Excel files
overall_performance.to_excel('overall_performance_report.xlsx', index=False)
average_grades_by_course.to_excel('course_performance_report.xlsx', index=False)
top_students.to_excel('top_students_report.xlsx', index=False)

# Function to save DataFrame to PDF
from fpdf import FPDF
def save_df_to_pdf(df, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Set font
    pdf.set_font("Arial", size=12)
    # Add title
    pdf.cell(200, 10, txt=filename.replace('.pdf', ''), ln=True, align='C')
    # Add column headers
    pdf.set_font("Arial", 'B', size=12)
    for column in df.columns:
        pdf.cell(40, 10, column, border=1)
    pdf.ln()
    # Add data
    pdf.set_font("Arial", size=12)
    for index, row in df.iterrows():
        for item in row:
            pdf.cell(40, 10, str(item), border=1)
        pdf.ln()
    pdf.output(filename)
    
# Save reports as PDF files
save_df_to_pdf(overall_performance, 'overall_performance_report.pdf')
save_df_to_pdf(average_grades_by_course, 'course_performance_report.pdf')
save_df_to_pdf(top_students, 'top_students_report.pdf')
