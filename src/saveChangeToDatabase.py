from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
import os
import sys

# Initialize the audit log DataFrame globally
audit_log_df = pd.DataFrame(columns=[
    "change_id", "table_name", "record_id", "change_type", "change_timestamp", "changed_by", "old_value", "new_value"
])

def get_database_path():
    """
    Get the path to the SQLite database file, adjusting for PyInstaller's temp directory.
    """
    if hasattr(sys, '_MEIPASS'):  # PyInstaller's temp folder
        return os.path.join(sys._MEIPASS, "school_management_system.db")
    return "school_management_system.db"

def get_engine():
    """
    Create and return a SQLAlchemy engine for the database.
    """
    db_path = get_database_path()
    return create_engine(f"sqlite:///{db_path}")

def read_from_df(table_name):
    """
    Read a single table from an SQLite database to a DataFrame.
    """
    engine = get_engine()
    dataframe = pd.read_sql_table(table_name, con=engine)
    return dataframe

def save_df_to_db(table_name, dataframe, index=None):
    """
    Save a single DataFrame to an SQLite database.
    """
    engine = get_engine()
    dataframe.to_sql(table_name, con=engine, if_exists='replace', index=False)
    log_change(table_name, index)

def log_change(table_name, index=None):
    """
    Log changes to the audit log.
    """
    global audit_log_df  # Ensure we're modifying the global DataFrame
    # Create a new entry in the audit log
    new_entry = {
        'change_id': len(audit_log_df) + 1,  # Incremental ID
        'table_name': table_name,
        'record_id': index,
        'change_timestamp': datetime.now(),
        'change_type': 'Update',  # Default type for now
        'changed_by': 'System',  # Placeholder for user information
        'old_value': None,  # Placeholder for old value
        'new_value': None,  # Placeholder for new value
    }

    # Append the new entry to the audit log DataFrame
    audit_log_df = pd.concat([audit_log_df, pd.DataFrame([new_entry])], ignore_index=True)

    # Push the updated audit log to the database
    engine = get_engine()
    audit_log_df.to_sql("audit_log", con=engine, if_exists='replace', index=False)
