from src.db_handling.exampleCode import students_df, courses_df,enrollments_df, assignments_df, grades_df 
from sqlalchemy import create_engine

# Create an engine to connect to the SQLite database
engine = create_engine('sqlite:///school_management_system.db')


# Save the changed DataFrames to the database
def save_all_changes():
    """
    Save all in-memory DataFrames to their respective tables in the database.
    """
    try:
        students_df.to_sql('students', con=engine, if_exists='replace', index=False)
        courses_df.to_sql('courses', con=engine, if_exists='replace', index=False)
        enrollments_df.to_sql('enrollments', con=engine, if_exists='replace', index=False)
        assignments_df.to_sql('assignments', con=engine, if_exists='replace', index=False)
        grades_df.to_sql('grades', con=engine, if_exists='replace', index=False)
        print("All changes have been saved to the database.")
    except Exception as e:
        print(f"Error saving changes: {e}")