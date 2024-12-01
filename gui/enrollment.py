from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df

class EnrollmentManagement:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enrollment Management")

    def enroll_student(self, student_id, course_id):
        enrollments_df = read_from_df('enrollments')
        new_index = (enrollments_df.index[-1]) + 1
        new_enroll = {student_id, course_id, new_index}
        enrollments_df = enrollments_df.append(new_enroll)
        save_df_to_db('enrollments', enrollments_df)

    def display_enrollments(self):
        enrollments_df = read_from_df('enrollments')
        print(enrollments_df)

    def run(self):
        tk.Label(self.root, text="Student ID").grid(row=0, column=0)
        student_id_entry = tk.Entry(self.root)
        student_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Course ID").grid(row=1, column=0)
        course_id_entry = tk.Entry(self.root)
        course_id_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Enroll", command=lambda: self.enroll_student(
            student_id_entry.get(),
            course_id_entry.get()
        )).grid(row=2, column=1)

        tk.Button(self.root, text="Display Enrollments", command=self.display_enrollments).grid(row=3, column=1)
        tk.Button(self.root, text="Exit", command=self.root.destroy).grid(row=4, column=1)
        self.root.mainloop()
