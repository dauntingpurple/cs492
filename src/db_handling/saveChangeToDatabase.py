from sqlalchemy import create_engine
import pandas as pd
# Any time changes to the data is made, one of these should be ran to update the database.

def refresh_df_from_db():
    """
    Open all DataFrames from an SQLite database.
    """
    engine = create_engine('sqlite:///school_management_system.db')
    #table_names = ['students', 'courses', 'enrollments', 'assignments', 'grades']
    
    # Load data from the database tables
    students_df = pd.read_sql_table('students', con=engine)
    courses_df = pd.read_sql_table('courses', con=engine)
    enrollments_df = pd.read_sql_table('enrollments', con=engine)
    grades_df = pd.read_sql_table('grades', con=engine)

    return students_df, courses_df, enrollments_df, grades_df

def read_from_df(table_name):
    """
    Read a single table from an SQLite database to a DataFrame.
    """
    engine = create_engine('sqlite:///school_management_system.db')
    dataframe = pd.read_sql_table(table_name, con=engine)
    return dataframe

def save_df_to_db(table_name, dataframe):
    """
    Save a single DataFrame to an SQLite database.
    """
    engine = create_engine('sqlite:///school_management_system.db')
    dataframe.to_sql(table_name, con=engine, if_exists='replace', index=False)


"""
# Example usage to save all dataframes to database: #
dataframes = {
    'students': students_df,
    'courses': courses_df,
    'enrollments': enrollments_df,
    'grades': grades_df
}
"""
def save_all_changes():
    """
    Save multiple DataFrames to an SQLite database.
    """
    engine = create_engine('sqlite:///school_management_system.db')
    students_df.to_sql('students', con=engine, if_exists='replace', index=False)
    for table_name, df in dataframes.items():
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)