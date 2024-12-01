from src.db_handling.exampleCode import students_df, courses_df, enrollments_df, assignments_df, grades_df
from sqlalchemy import create_engine
import os

# Specify the database path
db_path = 'school_management_system.db'

# Print the database path for debugging
print(f"Saving changes to the database at: {os.path.abspath(db_path)}")

# Create an engine to connect to the SQLite database
engine = create_engine(f'sqlite:///{db_path}')

def save_all_changes():
    """
    Save all in-memory DataFrames to their respective tables in the database.
    """
    try:
        print("Saving Students DataFrame to the database...")
        students_df.to_sql('students', con=engine, if_exists='replace', index=False)
        print("Students table saved successfully.")

        courses_df.to_sql('courses', con=engine, if_exists='replace', index=False)
        print("Courses table saved successfully.")

        enrollments_df.to_sql('enrollments', con=engine, if_exists='replace', index=False)
        print("Enrollments table saved successfully.")

        assignments_df.to_sql('assignments', con=engine, if_exists='replace', index=False)
        print("Assignments table saved successfully.")

        grades_df.to_sql('grades', con=engine, if_exists='replace', index=False)
        print("Grades table saved successfully.")

        print("All changes have been saved to the database.")
    except Exception as e:
        print(f"Error saving changes: {e}")
        raise
