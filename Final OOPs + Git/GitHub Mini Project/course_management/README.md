# Course Management System

A Python OOP project that models a small online learning platform with users, courses, and enrollments. It demonstrates inheritance, encapsulation, polymorphism, abstraction, instance methods, `@staticmethod`, and `@classmethod`.

## Requirements and Setup

- Python 3.8 or newer
- Git
- No third-party packages

Clone the repository and move into the project directory:

```bash
git clone https://github.com/Hrishabh-Tomar/Git-Github.git
cd "Git-Github/Final OOPs + Git/GitHub Mini Project/course_management"
python --version
```

## Class Relationships

```text
User (abstract)
├── Student  -> owns enrollments
└── Mentor   -> teaches courses

Course      -> has a mentor and enrolled students
Enrollment  -> links one Student to one Course
```

| Class | Responsibility |
|-------|----------------|
| `User` | Validates common identity data and defines the abstract role/dashboard interface |
| `Student(User)` | Enrolls in courses and displays enrollment progress |
| `Mentor(User)` | Provides expertise, teaches courses, and displays course statistics |
| `Course` | Tracks fee, GST, capacity, seats, mentor, and students |
| `Enrollment` | Links a student to a course and tracks status and grade |

## Features

- Abstract `User` base class with `Student` and `Mentor` roles
- Validated names and normalized email addresses
- Read-only unique user IDs and course/enrollment properties
- Course capacity, mentor assignment, seat tracking, and GST-inclusive pricing
- Duplicate and invalid enrollment protection
- Atomic enrollment validation: non-students are rejected before any state changes
- Enrollment completion, numeric grades, and letter grades
- Role-specific dashboards through polymorphism
- Custom exception hierarchy and 24 unit tests

## Run the Demo

```bash
python main.py
```

## Enrollment Example

```python
from course_management import Course, Enrollment, Mentor, Student

mentor = Mentor("Priya Verma", "priya@example.com", "Python & Data Analytics")
student = Student("Aarav Sharma", "aarav@example.com")
course = Course("PY101", "Python Fundamentals", fee=4999, capacity=30)
course.assign_mentor(mentor)

enrollment = Enrollment.enroll(student, course)
enrollment.complete(88)
print(enrollment)
```

Expected output:

```text
Enrollment #1: Aarav Sharma -> PY101 [Completed]
```

Only `Student` instances can enroll. Duplicate enrollments and full courses raise a specific exception without leaving partial state.

## Running the Tests

```bash
python -m unittest -v
```

## Project Structure

```text
course_management/
├── course_management/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── users.py
│   ├── course.py
│   └── enrollment.py
├── tests/
│   ├── __init__.py
│   └── test_course_management.py
├── main.py
└── README.md
```

## Git Workflow

Feature work is developed on branches, pushed to GitHub, reviewed through a Pull Request, and merged into `main`.

## Author

Hrishabh Singh Tomar