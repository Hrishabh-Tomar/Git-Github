"""Demo: runs the Course Management System end to end."""

from course_management import (
    Course, CourseFullError, DuplicateEnrollmentError, Enrollment,
    InvalidDataError, Mentor, Student, User,
)


def section(title):
    print(f"\n=== {title} ===")


def main():
    User.reset_id_counter()
    Enrollment.reset_counter()
    section("1. Abstraction: User cannot be created directly")
    try:
        User("Nobody", "nobody@example.com")
    except TypeError as error:
        print(f"TypeError: {error}")
    section("2. Inheritance and @classmethod: creating users")
    mentor = Mentor("Priya Verma", "priya@example.com", "Python & Data Analytics")
    aarav = Student("Aarav Sharma", "aarav@example.com")
    sneha = Student.from_dict({"name": "Sneha Iyer", "email": "sneha@example.com"})
    rohan = Student("Rohan Mehta", "rohan@example.com")
    for user in (mentor, aarav, sneha, rohan): print(user)
    section("3. Encapsulation: validation and read-only data")
    try: aarav.email = "not-an-email"
    except InvalidDataError as error: print(f"InvalidDataError: {error}")
    try: aarav.user_id = 99
    except AttributeError as error: print(f"AttributeError: {error}")
    print(f"Email check (@staticmethod): {User.is_valid_email('a@b.com')}, {User.is_valid_email('oops')}")
    section("4. Creating courses (@classmethod and @staticmethod)")
    python_course = Course("py101", "Python Fundamentals", 4999, capacity=2)
    sql_course = Course.from_dict({"code": "SQL201", "title": "SQL for Analytics", "fee": 3499})
    for course in (python_course, sql_course):
        course.assign_mentor(mentor)
        print(f"{course} | with GST: Rs.{course.total_price():,.2f}")
    print(f"Course.fee_with_gst(1000) = {Course.fee_with_gst(1000)}")
    section("5. Enrollment and business rules")
    first = Enrollment.enroll(aarav, python_course)
    Enrollment.enroll(sneha, python_course)
    Enrollment.enroll(aarav, sql_course)
    print(first)
    for student, course in ((aarav, python_course), (rohan, python_course)):
        try: Enrollment.enroll(student, course)
        except (DuplicateEnrollmentError, CourseFullError) as error:
            print(f"{type(error).__name__}: {error}")
    print(f"Total enrollments: {Enrollment.total_enrollments()}")
    section("6. Completing a course")
    first.complete(88)
    print(f"{first} -> grade {first.grade} ({first.letter_grade})")
    section("7. Polymorphism: same call, different dashboards")
    for user in (mentor, aarav, sneha, rohan):
        print(user.dashboard())
        print()


if __name__ == "__main__":
    main()
