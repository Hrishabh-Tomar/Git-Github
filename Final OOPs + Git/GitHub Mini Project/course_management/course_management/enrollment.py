"""Enrollment links a Student to a Course and tracks progress."""

from datetime import date

from .course import Course
from .exceptions import InvalidDataError
from .users import Student


class Enrollment:
    """A single student's enrollment in a course.

    Always create enrollments with Enrollment.enroll(), which checks seats and
    duplicates before linking the student and the course.
    """

    STATUS_ACTIVE = "Active"
    STATUS_COMPLETED = "Completed"
    _total = 0

    def __init__(self, student, course):
        Enrollment._total += 1
        self._enrollment_id = Enrollment._total
        self._student = student
        self._course = course
        self._enrolled_on = date.today()
        self._status = self.STATUS_ACTIVE
        self._grade = None

    # ---- read-only properties ----------------------------------------
    @property
    def enrollment_id(self):
        return self._enrollment_id

    @property
    def student(self):
        return self._student

    @property
    def course(self):
        return self._course

    @property
    def enrolled_on(self):
        return self._enrolled_on

    @property
    def status(self):
        return self._status

    @property
    def grade(self):
        return self._grade

    @property
    def is_active(self):
        return self._status == self.STATUS_ACTIVE

    @property
    def letter_grade(self):
        return None if self._grade is None else self.grade_to_letter(self._grade)

    # ---- instance method ---------------------------------------------
    def complete(self, grade):
        """Mark the enrollment as completed with a grade between 0 and 100."""
        if not self.is_active:
            raise InvalidDataError("This enrollment is already completed.")
        self._grade = self.validate_grade(grade)
        self._status = self.STATUS_COMPLETED

    # ---- class methods -----------------------------------------------
    @classmethod
    def enroll(cls, student, course):
        """Factory: validate, reserve a seat, create the enrollment and link it.

        Every check happens before any state changes, so a rejected enrollment
        leaves the course seats, the student's enrollments and the counter untouched.
        """
        if not isinstance(student, Student):
            raise InvalidDataError(
                f"Only a Student can enroll in a course, got {type(student).__name__}.")
        if not isinstance(course, Course):
            raise InvalidDataError(
                f"Enrollment requires a Course, got {type(course).__name__}.")

        course.register_student(student)  # raises if full or duplicate, before any change
        enrollment = cls(student, course)
        student.add_enrollment(enrollment)
        return enrollment

    @classmethod
    def total_enrollments(cls):
        """How many enrollments have been created so far."""
        return Enrollment._total

    @classmethod
    def reset_counter(cls):
        """Reset the shared counter (useful in tests and demos)."""
        Enrollment._total = 0

    # ---- static methods ----------------------------------------------
    @staticmethod
    def validate_grade(grade):
        """Return the grade if it is a number from 0 to 100, otherwise raise."""
        if not isinstance(grade, (int, float)) or not 0 <= grade <= 100:
            raise InvalidDataError("Grade must be a number between 0 and 100.")
        return grade

    @staticmethod
    def grade_to_letter(grade):
        """Convert a numeric grade to a letter grade."""
        if grade >= 90:
            return "A"
        if grade >= 75:
            return "B"
        if grade >= 60:
            return "C"
        if grade >= 40:
            return "D"
        return "F"

    def __str__(self):
        return (f"Enrollment #{self._enrollment_id}: {self._student.name} -> "
                f"{self._course.code} [{self._status}]")