"""Course Management System public API."""

from .course import Course
from .enrollment import Enrollment
from .exceptions import (
    CourseFullError,
    CourseManagementError,
    DuplicateEnrollmentError,
    InvalidDataError,
)
from .users import Mentor, Student, User

__version__ = "1.0.0"

__all__ = [
    "Course", "CourseFullError", "CourseManagementError",
    "DuplicateEnrollmentError", "Enrollment", "InvalidDataError",
    "Mentor", "Student", "User",
]
