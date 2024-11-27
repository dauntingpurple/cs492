class EnrollmentManagement:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enrollment Management")

    def enroll_student(self, student_id, course_id):
        session = Session()
        session.execute(
            f"INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES ({student_id}, {course_id}, CURRENT_DATE)"
        )
        session.commit()
        session.close()
        self.display_enrollments()

    def display_enrollments(self):
        session = Session()
        df = pd.read_sql("SELECT * FROM enrollments", con=engine)
        print(df)  # Debugging: Replace with GUI table display
        session.close()

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
