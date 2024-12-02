import unittest
from src.teacher import Teacher, TeacherAssignment

class TestTeacher(unittest.TestCase):
    
    def test_teacher_creation(self):
        teacher = Teacher(teacher_id=1, name="John Doe", qualifications=["MSc in Math"], subjects=["Math"])
        self.assertEqual(teacher.name, "John Doe")
        self.assertIn("Math", teacher.subjects)
    
    def test_teacher_update_details(self):
        teacher = Teacher(teacher_id=1, name="John Doe", qualifications=["MSc in Math"], subjects=["Math"])
        teacher.update_details(name="Jane Smith", subjects=["Math", "Computer Science"])
        self.assertEqual(teacher.name, "Jane Smith")
        self.assertIn("Computer Science", teacher.subjects)
    
    def test_teacher_assignment(self):
        teacher = Teacher(teacher_id=1, name="John Doe", qualifications=["MSc in Math"], subjects=["Math"])
        assignment = TeacherAssignment(teacher, "Room 101", "Math")
        self.assertEqual(assignment.teacher.name, "John Doe")
        self.assertEqual(assignment.subject, "Math")

if __name__ == "__main__":
    unittest.main()
