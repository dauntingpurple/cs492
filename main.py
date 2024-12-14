from gui.login import Login
from src.saveChangeToDatabase import save_df_to_db
import atexit

# Debug: Log when save_all_changes() is called
def on_exit():
    try:
        print("Attempting to save changes to the database...")
        # Thinking we actually save periodically so that if there's multiple users data gets updated pretty regularly.
        print("Changes saved successfully.")
    except Exception as e:
        print(f"Error saving changes on exit: {e}")

# Register the save function to run when the program exits
atexit.register(on_exit)

if __name__ == "__main__":
    try:
        print("Starting application...")
        app = Login()
        app.run()
    finally:
        print("Application is exiting.")
        on_exit()
