# Database Schema Documentation

## Overview
This database schema supports the School Management System and includes tables for managing students, courses, and enrollments.

## Tables

### Students
- **Table Name:** students
- **Purpose:** Stores student information.
- **Columns:**
  - `first_name` (VARCHAR)
  - `last_name` (VARCHAR)
  - `date_of_birth` (DATE)
  - `address` (VARCHAR)
  - `email` (VARCHAR)
  - `student_id` (INTEGER, PRIMARY KEY)

### Courses
- **Table Name:** courses
- **Purpose:** Stores course information.
- **Columns:**
  - `course_name` (VARCHAR)
  - `credits` (INTEGER)
  - `course_id` (INTEGER, PRIMARY KEY)

### Enrollments
- **Table Name:** enrollments
- **Purpose:** Tracks student enrollments in courses.
- **Columns:**
  - `student_id` (INTEGER, FOREIGN KEY to students)
  - `course_id` (INTEGER, FOREIGN KEY to courses)
  - `semester` (VARCHAR)
  - `year` (INTEGER)
    - `enrollment_id` (INTEGER, PRIMARY KEY)

### Grades
- **Table Name:** grades
- **Purpose:** Stores student grades per assignment.
- **Columns:**
- `student_id` (INTEGER, FOREIGN KEY to students)
- `grade` (FLOAT)
- `grade_id` (INTEGER, PRIMARY KEY)

## Relationships
- One student can enroll in multiple courses (one-to-many).
- A course can have multiple students enrolled (one-to-many).

## Sample Queries
```sql
-- Retrieve all students
SELECT * FROM students;

-- Enroll a student in a course
INSERT INTO enrollments (student_id, course_id,)
VALUES (1, 101);