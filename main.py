from gui.login import Login
from src.db_handling.saveChangeToDatabase import save_all_changes
import atexit

# Debug: Log when save_all_changes() is called
def on_exit():
    try:
        print("Attempting to save changes to the database...")
        save_all_changes()
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
