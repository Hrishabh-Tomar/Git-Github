import unittest

from course_management import (
    Course, CourseFullError, DuplicateEnrollmentError, Enrollment,
    InvalidDataError, Mentor, Student, User,
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
        with self.assertRaises(TypeError): User("Nobody", "nobody@example.com")
    def test_ids_are_unique_and_sequential(self): self.assertEqual((self.mentor.user_id, self.student.user_id), (1, 2))
    def test_user_id_is_read_only(self):
        with self.assertRaises(AttributeError): self.student.user_id = 50
    def test_invalid_email_rejected(self):
        with self.assertRaises(InvalidDataError): Student("Bad Email", "not-an-email")
    def test_email_is_normalised(self): self.assertEqual(Student("A", " A@B.COM ").email, "a@b.com")
    def test_empty_name_rejected(self):
        with self.assertRaises(InvalidDataError): Student("", "a@b.com")
    def test_is_valid_email_static(self): self.assertTrue(User.is_valid_email("a@b.com")); self.assertFalse(User.is_valid_email("oops"))
    def test_from_dict_builds_correct_subclass(self): self.assertIsInstance(Student.from_dict({"name": "A", "email": "a@b.com"}), Student)
    def test_mentor_requires_expertise(self):
        with self.assertRaises(InvalidDataError): Mentor("A", "a@b.com", "")
    def test_polymorphic_roles_and_dashboards(self): self.assertEqual((self.student.get_role(), self.mentor.get_role()), ("Student", "Mentor"))


class CourseTests(BaseTestCase):
    def test_code_is_upper_cased(self): self.assertEqual(self.course.code, "PY101")
    def test_fee_with_gst_static(self): self.assertEqual(Course.fee_with_gst(1000), 1180.0)
    def test_total_price_instance(self): self.assertEqual(self.course.total_price(), 1180.0)
    def test_from_dict_default_capacity(self): self.assertEqual(Course.from_dict({"code": "x", "title": "X", "fee": 1}).capacity, 30)
    def test_assign_mentor_links_both_sides(self): self.course.assign_mentor(self.mentor); self.assertIs(self.course.mentor, self.mentor); self.assertIn(self.course, self.mentor.courses)
    def test_invalid_course_data(self):
        with self.assertRaises(InvalidDataError): Course("", "X", 1)


class EnrollmentTests(BaseTestCase):
    def test_enroll_links_student_and_course(self):
        enrollment = Enrollment.enroll(self.student, self.course); self.assertIn(enrollment, self.student.enrollments); self.assertEqual(self.course.enrolled_count, 1)
    def test_duplicate_enrollment_rejected(self):
        Enrollment.enroll(self.student, self.course)
        with self.assertRaises(DuplicateEnrollmentError): Enrollment.enroll(self.student, self.course)
    def test_full_course_rejected_and_not_counted(self):
        Enrollment.enroll(self.student, self.course)
        with self.assertRaises(CourseFullError): Enrollment.enroll(Student("M", "m@b.com"), self.course)
    def test_non_student_rejected_without_partial_state(self):
        with self.assertRaises(InvalidDataError): Enrollment.enroll(self.mentor, self.course)
        self.assertEqual(self.course.enrolled_count, 0)
        self.assertEqual(Enrollment.total_enrollments(), 0)
    def test_complete_sets_grade_and_status(self):
        enrollment = Enrollment.enroll(self.student, self.course); enrollment.complete(88); self.assertEqual((enrollment.status, enrollment.letter_grade), ("Completed", "B"))
    def test_cannot_complete_twice(self):
        enrollment = Enrollment.enroll(self.student, self.course); enrollment.complete(88)
        with self.assertRaises(InvalidDataError): enrollment.complete(90)
    def test_invalid_grade_rejected(self):
        enrollment = Enrollment.enroll(self.student, self.course)
        with self.assertRaises(InvalidDataError): enrollment.complete(101)
    def test_grade_to_letter_boundaries(self): self.assertEqual([Enrollment.grade_to_letter(x) for x in (95, 80, 65, 45, 20)], ["A", "B", "C", "D", "F"])


if __name__ == "__main__": unittest.main()
