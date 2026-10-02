"""User hierarchy: an abstract User with Student and Mentor subclasses."""

import re
from abc import ABC, abstractmethod

from .exceptions import InvalidDataError


class User(ABC):
    _id_counter = 0
    _EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, name, email):
        self.name = name
        self.email = email
        User._id_counter += 1
        self.__user_id = User._id_counter

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not self.is_valid_email(value):
            raise InvalidDataError(f"Invalid email address: {value!r}")
        self._email = value.strip().lower()

    @staticmethod
    def is_valid_email(email):
        return isinstance(email, str) and bool(User._EMAIL_PATTERN.match(email.strip()))

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def reset_id_counter(cls):
        User._id_counter = 0

    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def dashboard(self):
        pass

    def __str__(self):
        return f"{self.get_role()} #{self.user_id}: {self.name} <{self.email}>"

    def __repr__(self):
        return f"{type(self).__name__}(id={self.user_id}, name={self.name!r})"


class Student(User):
    def __init__(self, name, email):
        super().__init__(name, email)
        self._enrollments = []

    @property
    def enrollments(self):
        return tuple(self._enrollments)

    def add_enrollment(self, enrollment):
        self._enrollments.append(enrollment)

    def get_role(self):
        return "Student"

    def dashboard(self):
        lines = [f"Student Dashboard - {self.name}"]
        if not self._enrollments:
            lines.append("  No enrollments yet.")
        for enrollment in self._enrollments:
            line = f"  - {enrollment.course.code} {enrollment.course.title}: {enrollment.status}"
            if enrollment.grade is not None:
                line += f" (grade {enrollment.grade}, {enrollment.letter_grade})"
            lines.append(line)
        return "\n".join(lines)


class Mentor(User):
    def __init__(self, name, email, expertise):
        super().__init__(name, email)
        if not isinstance(expertise, str) or not expertise.strip():
            raise InvalidDataError("Expertise cannot be empty.")
        self._expertise = expertise.strip()
        self._courses = []

    @property
    def expertise(self):
        return self._expertise

    @property
    def courses(self):
        return tuple(self._courses)

    def add_course(self, course):
        if course not in self._courses:
            self._courses.append(course)

    def get_role(self):
        return "Mentor"

    def dashboard(self):
        total_students = sum(course.enrolled_count for course in self._courses)
        lines = [f"Mentor Dashboard - {self.name} (Expertise: {self.expertise})"]
        if not self._courses:
            lines.append("  No courses assigned yet.")
        for course in self._courses:
            lines.append(f"  - {course.code} {course.title}: {course.enrolled_count} student(s)")
        lines.append(f"  Total students: {total_students}")
        return "\n".join(lines)
