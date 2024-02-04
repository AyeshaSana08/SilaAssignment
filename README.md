
# Database Schema Documentation

## Overview

This document provides an overview of the database schema for the application. The schema includes tables for students, subjects, and a Many-to-Many relationship table for enrollments.

## Tables

### students

- **Columns:**
  - `id` (Primary Key)
  - `name` (String, Index)
  - `age` (Integer)

- **Description:**
  - Represents information about students.

### subjects

- **Columns:**
  - `id` (Primary Key)
  - `subject_id` (Integer, Index)

- **Description:**
  - Represents information about subjects.

### enrollments

- **Columns:**
  - `student_id` (Foreign Key to students)
  - `subject_id` (Foreign Key to subjects)

- **Description:**
  - Represents the Many-to-Many relationship between students and subjects. Each record in this table indicates that a student is enrolled in a specific subject.

## Relationships

- **students to enrollments (One-to-Many):**
  - Each student in the `students` table can have multiple records in the `enrollments` table, indicating enrollment in multiple subjects.

- **subjects to enrollments (One-to-Many):**
  - Each subject in the `subjects` table can have multiple records in the `enrollments` table, indicating multiple students enrolled in the subject.

- **students to subjects (Many-to-Many):**
  - Through the `enrollments` table, there is a Many-to-Many relationship between students and subjects. A student can be enrolled in multiple subjects, and a subject can have multiple students.

## Example SQL Queries

### Retrieve all students enrolled in a specific subject:

```sql
SELECT students.id, students.name, students.age
FROM students
JOIN enrollments ON students.id = enrollments.student_id
WHERE enrollments.subject_id = :subject_id;


