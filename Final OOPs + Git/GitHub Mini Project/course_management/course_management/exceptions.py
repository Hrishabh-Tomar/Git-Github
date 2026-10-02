"""Custom exceptions for the Course Management System."""


class CourseManagementError(Exception):
    """Base class for all errors raised by this package."""


class InvalidDataError(CourseManagementError):
    """Raised when a name, email, fee, grade or similar value is invalid."""


class CourseFullError(CourseManagementError):
    """Raised when a course has no seats left."""


class DuplicateEnrollmentError(CourseManagementError):
    """Raised when a student is already enrolled in a course."""
