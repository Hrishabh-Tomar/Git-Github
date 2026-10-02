"""Unit tests for the Course Management System. Run with: python -m unittest -v"""

import unittest

from course_management import (
    Course,
    CourseFullError,
    DuplicateEnrollmentError,
    Enrollment,
    InvalidDataError,
    Mentor,
    Student,
    User,
)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        User.reset_id_counter()
        Enrollment.reset_counter()
        self.mentor = Mentor("Priya Verma", "priya@example.com", "Python")
        self.student = Student("Aarav Sharma", "aarav@example.com")
        self.course = Course("PY101", "Python Fundamentals", 1000, capacity=1)


class UserTests(BaseTestCase):
    def test_user_is_abstract(self):
        with self.assertRaises(TypeError):
            User("Nobody", "nobody@example.com")

    def test_ids_are_unique_and_sequential(self):
        self.assertEqual((self.mentor.user_id, self.student.user_id), (1, 2))

    def test_user_id_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.student.user_id = 50

    def test_invalid_email_rejected(self):
        with self.assertRaises(InvalidDataError):
            Student("Bad Email", "not-an-email")

    def test_email_is_normalised(self):
        self.assertEqual(Student("X", "  X@Example.COM ").email, "x@example.com")

    def test_empty_name_rejected(self):
        with self.assertRaises(InvalidDataError):
            Student("   ", "a@b.com")

    def test_is_valid_email_static(self):
        self.assertTrue(User.is_valid_email("a@b.com"))
        self.assertFalse(User.is_valid_email("a@b"))
        self.assertFalse(User.is_valid_email(None))

    def test_from_dict_builds_correct_subclass(self):
        student = Student.from_dict({"name": "Sneha", "email": "sneha@example.com"})
        self.assertIsInstance(student, Student)

    def test_polymorphic_roles_and_dashboards(self):
        self.assertEqual(self.mentor.get_role(), "Mentor")
        self.assertEqual(self.student.get_role(), "Student")
        self.assertIn("Mentor Dashboard", self.mentor.dashboard())
        self.assertIn("Student Dashboard", self.student.dashboard())

    def test_mentor_requires_expertise(self):
        with self.assertRaises(InvalidDataError):
            Mentor("No Skill", "m@example.com", "")


class CourseTests(BaseTestCase):
    def test_code_is_upper_cased(self):
        self.assertEqual(Course("py999", "T", 0).code, "PY999")

    def test_invalid_course_data(self):
        for args in (("", "T", 10), ("C1", "", 10), ("C1", "T", -1), ("C1", "T", 10, 0)):
            with self.assertRaises(InvalidDataError):
                Course(*args)

    def test_fee_with_gst_static(self):
        self.assertEqual(Course.fee_with_gst(1000), 1180.0)
        self.assertEqual(Course.fee_with_gst(1000, 0.05), 1050.0)

    def test_total_price_instance(self):
        self.assertEqual(self.course.total_price(), 1180.0)

    def test_from_dict_default_capacity(self):
        course = Course.from_dict({"code": "a1", "title": "T", "fee": 5})
        self.assertEqual(course.capacity, 30)

    def test_assign_mentor_links_both_sides(self):
        self.course.assign_mentor(self.mentor)
        self.assertIs(self.course.mentor, self.mentor)
        self.assertIn(self.course, self.mentor.courses)


class EnrollmentTests(BaseTestCase):
    def test_enroll_links_student_and_course(self):
        enrollment = Enrollment.enroll(self.student, self.course)
        self.assertIn(enrollment, self.student.enrollments)
        self.assertEqual(self.course.enrolled_count, 1)
        self.assertEqual(self.course.available_seats, 0)
        self.assertTrue(self.course.is_full)

    def test_duplicate_enrollment_rejected(self):
        course = Course("PY102", "More Python", 1000, capacity=5)
        Enrollment.enroll(self.student, course)
        with self.assertRaises(DuplicateEnrollmentError):
            Enrollment.enroll(self.student, course)

    def test_full_course_rejected_and_not_counted(self):
        Enrollment.enroll(self.student, self.course)
        other = Student("Rohan", "rohan@example.com")
        with self.assertRaises(CourseFullError):
            Enrollment.enroll(other, self.course)
        self.assertEqual(Enrollment.total_enrollments(), 1)

    def test_mentor_cannot_enroll_and_state_is_unchanged(self):
        with self.assertRaises(InvalidDataError):
            Enrollment.enroll(self.mentor, self.course)
        self.assertEqual(self.course.available_seats, 1)
        self.assertEqual(self.course.students, ())
        self.assertEqual(Enrollment.total_enrollments(), 0)

    def test_invalid_course_leaves_student_and_counter_unchanged(self):
        with self.assertRaises(InvalidDataError):
            Enrollment.enroll(self.student, "PY101")
        self.assertEqual(self.student.enrollments, ())
        self.assertEqual(Enrollment.total_enrollments(), 0)

    def test_complete_sets_grade_and_status(self):
        enrollment = Enrollment.enroll(self.student, self.course)
        enrollment.complete(92)
        self.assertEqual(enrollment.status, Enrollment.STATUS_COMPLETED)
        self.assertEqual(enrollment.letter_grade, "A")

    def test_cannot_complete_twice(self):
        enrollment = Enrollment.enroll(self.student, self.course)
        enrollment.complete(70)
        with self.assertRaises(InvalidDataError):
            enrollment.complete(80)

    def test_invalid_grade_rejected(self):
        for bad in (-1, 101, "A"):
            with self.assertRaises(InvalidDataError):
                Enrollment.validate_grade(bad)

    def test_grade_to_letter_boundaries(self):
        expected = {95: "A", 90: "A", 75: "B", 60: "C", 40: "D", 39: "F"}
        for grade, letter in expected.items():
            self.assertEqual(Enrollment.grade_to_letter(grade), letter)


if __name__ == "__main__":
    unittest.main()