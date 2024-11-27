# Database Schema Documentation

## Overview
This database schema supports the School Management System and includes tables for managing students, courses, and enrollments.

## Tables

### Students
- **Table Name:** students
- **Purpose:** Stores student information.
- **Columns:**
  - `student_id` (INTEGER, PRIMARY KEY)
  - `first_name` (VARCHAR)
  - `last_name` (VARCHAR)
  - `date_of_birth` (DATE)

### Courses
- **Table Name:** courses
- **Purpose:** Stores course information.
- **Columns:**
  - `course_id` (INTEGER, PRIMARY KEY)
  - `course_name` (VARCHAR)
  - `credits` (INTEGER)

### Enrollments
- **Table Name:** enrollments
- **Purpose:** Tracks student enrollments in courses.
- **Columns:**
  - `enrollment_id` (INTEGER, PRIMARY KEY)
  - `student_id` (INTEGER, FOREIGN KEY to students)
  - `course_id` (INTEGER, FOREIGN KEY to courses)
  - `enrollment_date` (DATE)

### Grades
- **Table Name:** grades
- **Purpose:** Stores student grades per assignment.
- **Columns:**
- `grade_id` (INTEGER, PRIMARY KEY)
- `student_id` (INTEGER, FOREIGN KEY to students)
- `assignment_id` (INTEGER, FOREIGN KEY to assignments)
- `grade` (FLOAT)

## Relationships
- One student can enroll in multiple courses (one-to-many).
- A course can have multiple students enrolled (one-to-many).

## Sample Queries
```sql
-- Retrieve all students
SELECT * FROM students;

-- Enroll a student in a course
INSERT INTO enrollments (student_id, course_id, enrollment_date)
VALUES (1, 101, '2023-08-01');