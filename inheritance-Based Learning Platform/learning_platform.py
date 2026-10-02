"""Learning platform: inheritance and method overriding in Python."""


class User:
    """Parent class holding properties and behaviour common to every user."""

    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def login(self):
        print(f"{self.name} logged in.")

    def get_role(self):
        return "User"

    def show_dashboard(self):
        """Overridden by child classes to show role-specific content."""
        print(f"[{self.get_role()}] Welcome, {self.name}. This is the generic dashboard.")

    def __str__(self):
        return f"{self.get_role()} #{self.user_id}: {self.name} <{self.email}>"


class Student(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.enrolled_courses = []

    def get_role(self):
        return "Student"

    def enroll(self, course):
        self.enrolled_courses.append(course)
        print(f"{self.name} enrolled in {course}.")

    def show_dashboard(self):  # method overriding
        courses = ", ".join(self.enrolled_courses) or "no courses yet"
        print(f"[Student] {self.name}'s dashboard -> Courses: {courses}")


class Mentor(User):
    def __init__(self, user_id, name, email, expertise):
        super().__init__(user_id, name, email)
        self.expertise = expertise
        self.mentees = []

    def get_role(self):
        return "Mentor"

    def assign_mentee(self, student):
        self.mentees.append(student.name)
        print(f"{self.name} is now mentoring {student.name}.")

    def show_dashboard(self):  # method overriding
        mentees = ", ".join(self.mentees) or "no mentees yet"
        print(f"[Mentor] {self.name}'s dashboard -> Expertise: {self.expertise} | Mentees: {mentees}")


class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.managed_users = []

    def get_role(self):
        return "Admin"

    def add_user(self, user):
        self.managed_users.append(user)
        print(f"{self.name} added {user.get_role()} {user.name} to the platform.")

    def show_dashboard(self):  # method overriding
        print(f"[Admin] {self.name}'s dashboard -> Total users managed: {len(self.managed_users)}")


if __name__ == "__main__":
    student = Student(1, "Aarav Sharma", "aarav@example.com")
    mentor = Mentor(2, "Priya Verma", "priya@example.com", "Python & Data Analytics")
    admin = Admin(3, "Hrishabh Singh Tomar", "admin@example.com")

    print("--- Common behaviour inherited from User ---")
    for user in (student, mentor, admin):
        print(user)
        user.login()

    print("\n--- Role-specific functionality ---")
    student.enroll("Python Basics")
    student.enroll("SQL for Analytics")
    mentor.assign_mentee(student)
    for user in (student, mentor):
        admin.add_user(user)

    print("\n--- Method overriding: same call, different output ---")
    for user in (User(0, "Guest", "guest@example.com"), student, mentor, admin):
        user.show_dashboard()

    print("\n--- Class relationships ---")
    for cls in (Student, Mentor, Admin):
        print(f"{cls.__name__} is a subclass of User: {issubclass(cls, User)}")
        
        
        """--- Common behaviour inherited from User ---
Student #1: Aarav Sharma <aarav@example.com>
Aarav Sharma logged in.
Mentor #2: Priya Verma <priya@example.com>
Priya Verma logged in.
Admin #3: Hrishabh Singh Tomar <admin@example.com>
Hrishabh Singh Tomar logged in.

--- Role-specific functionality ---
Aarav Sharma enrolled in Python Basics.
Aarav Sharma enrolled in SQL for Analytics.
Priya Verma is now mentoring Aarav Sharma.
Hrishabh Singh Tomar added Student Aarav Sharma to the platform.
Hrishabh Singh Tomar added Mentor Priya Verma to the platform.

--- Method overriding: same call, different output ---
[User] Welcome, Guest. This is the generic dashboard.
[Student] Aarav Sharma's dashboard -> Courses: Python Basics, SQL for Analytics
[Mentor] Priya Verma's dashboard -> Expertise: Python & Data Analytics | Mentees: Aarav Sharma
[Admin] Hrishabh Singh Tomar's dashboard -> Total users managed: 2

--- Class relationships ---
Student is a subclass of User: True
Mentor is a subclass of User: True
Admin is a subclass of User: True"""