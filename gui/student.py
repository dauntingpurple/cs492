from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df

class StudentManagement:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Management")

    def add_student(self, first_name, last_name, dob, address, email):
        """
        Adds a new student to the database.
        """
        # Validate input fields
        if not first_name or not last_name or not dob:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            students_df = read_from_df('students')
            new_index = (students_df.index[-1]) + 1
            new_student = {first_name, last_name, dob, address, email, new_index}
            students_df = students_df.append(new_student)
            save_df_to_db('students', students_df)

            # Show success message
            messagebox.showinfo("Success", "Student added successfully!")
            
        except Exception as e:
            # Show error message if something goes wrong
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def display_students(self):
        """
        Displays all student records in a scrollable GUI window.
        """
        # Create a new window for displaying student information
        display_window = tk.Toplevel(self.root)
        display_window.title("Student List")
        display_window.geometry("500x400")

        # Fetch student data from the database
        students_df = read_from_df('students')

        # Debugging: Print the dataframe to verify the data
        print(students_df)

        # Add a title label
        tk.Label(display_window, text="Student List", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Create a frame to hold the student data and make it scrollable
        frame = tk.Frame(display_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas for scrolling
        canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbar to interact with the canvas
        scrollbar.config(command=canvas.yview)

        # Add a frame inside the canvas to hold the labels
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Display student data dynamically using labels
        #for index, row in df.iterrows():
        #    tk.Label(inner_frame, text=f"ID: {row['student_id']}, "
        #                               f"Name: {row['first_name']} {row['last_name']}, "
        #                               f"DOB: {row['date_of_birth']}").pack(anchor="w", padx=10, pady=2)
        tk.Label(inner_frame, text = students_df).pack(anchor="w", padx=10, pady=2)

        # Configure the canvas size dynamically based on inner_frame
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def run(self):
        """
        Starts the GUI application.
        """
        # Add input fields for student data
        tk.Label(self.root, text="First Name").grid(row=0, column=0)
        first_name_entry = tk.Entry(self.root)
        first_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Last Name").grid(row=1, column=0)
        last_name_entry = tk.Entry(self.root)
        last_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Date of Birth").grid(row=2, column=0)
        dob_entry = tk.Entry(self.root)
        dob_entry.grid(row=2, column=1)

        # Add buttons for actions
        tk.Button(self.root, text="Add Student", command=lambda: self.add_student(
            first_name_entry.get(),
            last_name_entry.get(),
            dob_entry.get()
        )).grid(row=3, column=1, pady=10)

        tk.Button(self.root, text="Display Students", command=self.display_students).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Exit", command=self.root.destroy).grid(row=5, column=1, pady=10)

        # Start the main loop
        self.root.mainloop()


# Entry point for the application
if __name__ == "__main__":
    app = StudentManagement()
    app.run()

