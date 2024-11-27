from src.db_handling.openDatabase import courses_df

class CourseManagement:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Course Management")

	def add_course(self, course_name, credits):
		new_index = (courses_df.index[-1]) + 1
		new_course = {course_name, credits, new_index}
		courses_df = courses_df.append(new_course)

		""" I think it's easier if while the program is running we use the dataframe
		and then when it's closed it saves it to the database, that what it limits how many
		calls are being made to it.

		session = Session()
		session.execute(
			f"INSERT INTO courses (course_name, credits) VALUES ('{course_name}', {credits})"
		)
		session.commit()
		session.close()
		self.display_courses()
		"""
	def display_courses(self):
		print(courses_df)
		"""
		session = Session()
		df = pd.read_sql("SELECT * FROM courses", con=engine)
		print(df)  # Debugging: Replace with GUI table display
		session.close()
		"""

	def run(self):
		tk.Label(self.root, text="Course Name").grid(row=0, column=0)
		course_name_entry = tk.Entry(self.root)
		course_name_entry.grid(row=0, column=1)

		tk.Label(self.root, text="Credits").grid(row=1, column=0)
		credits_entry = tk.Entry(self.root)
		credits_entry.grid(row=1, column=1)

		tk.Button(self.root, text="Add Course", command=lambda: self.add_course(
			course_name_entry.get(),
			credits_entry.get()
		)).grid(row=2, column=1)

		tk.Button(self.root, text="Display Courses", command=self.display_courses).grid(row=3, column=1)
		tk.Button(self.root, text="Exit", command=self.root.destroy).grid(row=4, column=1)
		self.root.mainloop()
