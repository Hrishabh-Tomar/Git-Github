"""Course model with seat management and fee calculation."""

from .exceptions import CourseFullError, DuplicateEnrollmentError, InvalidDataError
from .users import Mentor

DEFAULT_GST_RATE = 0.18


class Course:
    def __init__(self, code, title, fee, capacity=30):
        if not isinstance(code, str) or not code.strip():
            raise InvalidDataError("Course code cannot be empty.")
        if not isinstance(title, str) or not title.strip():
            raise InvalidDataError("Course title cannot be empty.")
        if not isinstance(fee, (int, float)) or fee < 0:
            raise InvalidDataError("Course fee must be zero or more.")
        if not isinstance(capacity, int) or capacity <= 0:
            raise InvalidDataError("Course capacity must be a positive whole number.")
        self._code = code.strip().upper()
        self._title = title.strip()
        self._fee = fee
        self._capacity = capacity
        self._mentor = None
        self._students = []

    @property
    def code(self): return self._code
    @property
    def title(self): return self._title
    @property
    def fee(self): return self._fee
    @property
    def capacity(self): return self._capacity
    @property
    def mentor(self): return self._mentor
    @property
    def students(self): return tuple(self._students)
    @property
    def enrolled_count(self): return len(self._students)
    @property
    def available_seats(self): return self._capacity - len(self._students)
    @property
    def is_full(self): return self.available_seats <= 0

    def assign_mentor(self, mentor):
        if not isinstance(mentor, Mentor):
            raise InvalidDataError("Course mentor must be a Mentor instance.")
        if mentor is self._mentor:
            return
        if self._mentor is not None:
            self._mentor.remove_course(self)
        mentor.add_course(self)
        self._mentor = mentor

    def register_student(self, student):
        if student in self._students:
            raise DuplicateEnrollmentError(f"{student.name} is already enrolled in {self._code}.")
        if self.is_full:
            raise CourseFullError(f"{self._code} is full ({self._capacity} seats).")
        self._students.append(student)

    def total_price(self):
        return self.fee_with_gst(self._fee)

    @staticmethod
    def fee_with_gst(fee, gst_rate=DEFAULT_GST_RATE):
        return round(fee * (1 + gst_rate), 2)

    @classmethod
    def from_dict(cls, data):
        return cls(data["code"], data["title"], data["fee"], data.get("capacity", 30))

    def __str__(self):
        return (f"{self._code} - {self._title} (Rs.{self._fee:,.2f}, "
                f"{self.available_seats}/{self._capacity} seats left)")
