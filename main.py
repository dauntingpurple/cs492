from gui.login import Login
from src.db_handling.saveChangeToDatabase import save_all_changes

if __name__ == "__main__":
    try:
        app = Login()
        app.run()
    finally:
        save_all_changes()
