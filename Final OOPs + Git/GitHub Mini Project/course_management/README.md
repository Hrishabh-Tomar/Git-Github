# Course Management System

A Python OOP project that models a small online learning platform: users (students and mentors), courses, and enrollments. It demonstrates inheritance, encapsulation, polymorphism, abstraction, instance methods, `@staticmethod` and `@classmethod`, and it is developed with a feature-branch Git workflow.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [OOP Concepts Demonstrated](#oop-concepts-demonstrated)
- [Usage Example](#usage-example)
- [Running the Tests](#running-the-tests)
- [Project Structure](#project-structure)
- [Git Workflow](#git-workflow)
- [Author](#author)

## Features

- Abstract `User` base class with `Student` and `Mentor` roles
- Validated, encapsulated user data (name, normalized email, read-only unique ID)
- Courses with capacity, mentor assignment, seat tracking and GST-inclusive pricing
- Enrollments with duplicate and capacity checks, completion, grading and letter grades
- Safe enrollment: all inputs are validated before any change, so a rejected enrollment never uses a seat or changes any counter
- Role-specific dashboards through polymorphism
- Custom exception hierarchy for clear error handling
- 24 unit tests, with no third-party dependencies

## Requirements

- **Python 3.8 or newer** (developed and tested on Python 3.12)
- Git
- No third-party packages

## Getting Started

This project lives inside a larger repository, so navigate to it from the repository root before running anything.

```bash
# 1. Clone the repository and enter its root folder
git clone https://github.com/Hrishabh-Tomar/Git-Github.git
cd Git-Github

# 2. Move into the project folder
cd "Final OOPs + Git/GitHub Mini Project/course_management"

# 3. Check your Python version (3.8 or newer)
python --version

# 4. Run the demo and the tests
python main.py
python -m unittest -v
```

Run every command from the project folder in step 2. The tests and demo import the `course_management` package from the current directory.

## Architecture

### Class relationships

```text
                 User (abstract)
                /               \
          Student               Mentor
             |                     |
             | has many            | teaches many
             v                     v
        Enrollment  ------->    Course
     (student, course,       (code, title, fee,
      status, grade)          capacity, mentor)
```

- `Student` and `Mentor` **inherit** from the abstract `User` class (is-a).
- A `Mentor` teaches many `Course` objects, and each `Course` has one assigned `Mentor`.
- A `Student` has many `Enrollment` objects.
- Each `Enrollment` links exactly one `Student` to exactly one `Course`, and holds the status and grade for that pair.
- A `Course` keeps the list of enrolled students and controls seat availability.

### Class responsibilities

| Class | Responsibility |
|-------|----------------|
| `User` (abstract) | Common data (ID, name, email), validation, and the abstract `get_role()` and `dashboard()` methods |
| `Student(User)` | Keeps the student's enrollments and shows a learner dashboard |
| `Mentor(User)` | Keeps expertise and the courses taught, and shows an instructor dashboard |
| `Course` | Manages capacity, seats, the assigned mentor and fee with GST |
| `Enrollment` | Links one student to one course, validates the request, and tracks status and grade |
| `CourseManagementError` | Base exception, with `InvalidDataError`, `CourseFullError` and `DuplicateEnrollmentError` as subclasses |

## OOP Concepts Demonstrated

| Concept | Where it is used |
|---------|------------------|
| **Inheritance** | `Student` and `Mentor` extend `User` and reuse its constructor, validation and `__str__` through `super()` |
| **Encapsulation** | Private `__user_id` with a read-only property; validated `name` and `email` setters; read-only properties on `Course` and `Enrollment` |
| **Polymorphism** | `dashboard()` and `get_role()` are called on any `User` and each subclass responds differently |
| **Abstraction** | `User` uses `ABC` and `@abstractmethod`, so it cannot be instantiated directly |
| **Instance methods** | `Course.assign_mentor()`, `Course.register_student()`, `Enrollment.complete()`, `Student.add_enrollment()` |
| **`@staticmethod`** | `User.is_valid_email()`, `Course.fee_with_gst()`, `Enrollment.validate_grade()`, `Enrollment.grade_to_letter()` |
| **`@classmethod`** | `User.from_dict()`, `Course.from_dict()`, `Enrollment.enroll()` (factory), `Enrollment.total_enrollments()` |

## Usage Example

```python
from course_management import Course, Enrollment, Mentor, Student

mentor = Mentor("Priya Verma", "priya@example.com", "Python & Data Analytics")
student = Student("Aarav Sharma", "aarav@example.com")

course = Course("PY101", "Python Fundamentals", fee=4999, capacity=30)
course.assign_mentor(mentor)

enrollment = Enrollment.enroll(student, course)   # checks participants, seats and duplicates
enrollment.complete(88)                           # grade 88 -> letter B

print(student.dashboard())
print(mentor.dashboard())
print(Course.fee_with_gst(4999))                  # 5898.82

try:
    Enrollment.enroll(mentor, course)             # a Mentor is not allowed to enroll
except Exception as error:
    print(f"{type(error).__name__}: {error}")
print(f"Seats left: {course.available_seats}/{course.capacity}")
```

Expected output:

```text
Student Dashboard - Aarav Sharma
  - PY101 Python Fundamentals: Completed (grade 88, B)
Mentor Dashboard - Priya Verma (Expertise: Python & Data Analytics)
  - PY101 Python Fundamentals: 1 student(s)
  Total students: 1
5898.82
InvalidDataError: Only Student users can enroll in a course.
Seats left: 29/30
```

Run the full demonstration with `python main.py`. It prints seven sections covering the concepts above.

## Running the Tests

```bash
python -m unittest -v
```

All 24 tests should pass. They cover validation, abstraction, polymorphism, seat limits, duplicate enrollments, grading, and a regression check that a rejected enrollment leaves seats, student enrollments and the enrollment counter unchanged.

## Project Structure

```text
course_management/                  <- project folder (run commands from here)
├── course_management/              <- Python package
│   ├── __init__.py                 # public API
│   ├── exceptions.py               # custom exceptions
│   ├── users.py                    # User, Student, Mentor
│   ├── course.py                   # Course
│   └── enrollment.py               # Enrollment
├── tests/
│   ├── __init__.py
│   └── test_course_management.py
├── main.py                         # runnable demo
├── .gitignore
└── README.md
```

## Git Workflow

Development followed a feature-branch workflow. The enrollment validation and documentation update were developed on `feature/atomic-enrollment-docs`, reviewed in Pull Request [#1](https://github.com/Hrishabh-Tomar/Git-Github/pull/1), and merged into `main`.

## Author

Hrishabh Singh Tomar