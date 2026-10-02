"""Employee Management System: a simple OOP example in Python."""


class Employee:
    """Represents an employee with basic details and salary operations."""

    total_employees = 0  # class variable shared by all objects

    def __init__(self, emp_id, name, department, salary, designation):
        if salary <= 0:
            raise ValueError("Salary must be greater than zero.")
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary  # monthly salary
        self.designation = designation
        Employee.total_employees += 1

    def display_info(self):
        print(f"ID: {self.emp_id} | Name: {self.name} | Department: {self.department} "
              f"| Designation: {self.designation} | Monthly Salary: Rs.{self.salary:,.2f}")

    def update_salary(self, new_salary):
        if new_salary <= 0:
            raise ValueError("New salary must be greater than zero.")
        old_salary = self.salary
        self.salary = new_salary
        print(f"{self.name}'s salary updated: Rs.{old_salary:,.2f} -> Rs.{new_salary:,.2f}")

    def calculate_annual_salary(self):
        return self.salary * 12


if __name__ == "__main__":
    employees = [
        Employee(101, "Aarav Sharma", "Engineering", 85000, "Software Engineer"),
        Employee(102, "Priya Verma", "Data Analytics", 78000, "Data Analyst"),
        Employee(103, "Rohan Mehta", "Human Resources", 60000, "HR Manager"),
        Employee(104, "Sneha Iyer", "Finance", 72000, "Accountant"),
        Employee(105, "Hrishabh Singh Tomar", "Data Analytics", 95000, "Senior Data Analyst"),
    ]

    print("=== All Employees ===")
    for emp in employees:
        emp.display_info()

    print("\n=== Annual Salaries ===")
    for emp in employees:
        print(f"{emp.name}: Rs.{emp.calculate_annual_salary():,.2f}")

    print("\n=== Updating Salary ===")
    employees[1].update_salary(84000)
    print(f"New annual salary of {employees[1].name}: Rs.{employees[1].calculate_annual_salary():,.2f}")

    print("\n=== Updated Employee Details ===")
    employees[1].display_info()

    print(f"\nTotal employees created: {Employee.total_employees}")
    
    """=== All Employees ===
ID: 101 | Name: Aarav Sharma | Department: Engineering | Designation: Software Engineer | Monthly Salary: Rs.85,000.00
ID: 102 | Name: Priya Verma | Department: Data Analytics | Designation: Data Analyst | Monthly Salary: Rs.78,000.00
ID: 103 | Name: Rohan Mehta | Department: Human Resources | Designation: HR Manager | Monthly Salary: Rs.60,000.00
ID: 104 | Name: Sneha Iyer | Department: Finance | Designation: Accountant | Monthly Salary: Rs.72,000.00
ID: 105 | Name: Hrishabh Singh Tomar | Department: Data Analytics | Designation: Senior Data Analyst | Monthly Salary: Rs.95,000.00

=== Annual Salaries ===
Aarav Sharma: Rs.1,020,000.00
Priya Verma: Rs.936,000.00
Rohan Mehta: Rs.720,000.00
Sneha Iyer: Rs.864,000.00
Hrishabh Singh Tomar: Rs.1,140,000.00

=== Updating Salary ===
Priya Verma's salary updated: Rs.78,000.00 -> Rs.84,000.00
New annual salary of Priya Verma: Rs.1,008,000.00

=== Updated Employee Details ===
ID: 102 | Name: Priya Verma | Department: Data Analytics | Designation: Data Analyst | Monthly Salary: Rs.84,000.00

Total employees created: 5"""