from src.db_handling.saveChangeToDatabase import save_df_to_db, read_from_df

class CourseManagement:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Course Management")

	def add_course(self, course_name, credits):
		courses_df = read_from_df('courses')
		new_index = (courses_df.index[-1]) + 1
		new_course = {course_name, credits, new_index}
		courses_df = courses_df.append(new_course)
		save_df_to_db('courses', courses_df)
	
	def display_courses(self):
		courses_df = read_from_df('courses')
		print(courses_df)

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
