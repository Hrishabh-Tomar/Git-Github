# Learning Platform

A small Python learning platform that demonstrates **inheritance** and **method overriding**.

## Class Relationships

```
        User  (parent)
       /  |  \
Student Mentor Admin  (children)
```

| Class | Inherited from `User` | Role-specific functionality |
|-------|----------------------|-----------------------------|
| `Student` | `user_id`, `name`, `email`, `login()` | `enroll()`, list of enrolled courses |
| `Mentor` | `user_id`, `name`, `email`, `login()` | `assign_mentee()`, expertise, mentee list |
| `Admin` | `user_id`, `name`, `email`, `login()` | `add_user()`, list of managed users |

## Concepts Demonstrated

- **Inheritance:** common properties (`user_id`, `name`, `email`) and methods (`login()`, `__str__()`) are written once in `User` and reused by every child class through `super().__init__()`.
- **Method overriding:** `show_dashboard()` and `get_role()` are defined in `User` and redefined in each child, so the same call gives a different result for each role.

## Run

```bash
python learning_platform.py
```

## Sample Output

```
[User] Welcome, Guest. This is the generic dashboard.
[Student] Aarav Sharma's dashboard -> Courses: Python Basics, SQL for Analytics
[Mentor] Priya Verma's dashboard -> Expertise: Python & Data Analytics | Mentees: Aarav Sharma
[Admin] Hrishabh Singh Tomar's dashboard -> Total users managed: 2
```

## Author

Hrishabh Singh Tomar
