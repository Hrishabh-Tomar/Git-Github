# Employee Management System

A simple Python program that models employees using a single `Employee` class and Object-Oriented Programming.

## Employee Class

| Attribute | Description |
|-----------|-------------|
| `emp_id` | Unique employee ID |
| `name` | Employee name |
| `department` | Department the employee works in |
| `salary` | Monthly salary |
| `designation` | Job title |

| Method | Description |
|--------|-------------|
| `display_info()` | Prints the employee's details |
| `update_salary(new_salary)` | Changes the salary (rejects zero or negative values) |
| `calculate_annual_salary()` | Returns monthly salary x 12 |

## OOP Concepts Used

- **Class and objects:** `Employee` is the blueprint, and five objects are created from it.
- **Constructor (`__init__`):** sets up each object's attributes when it is created.
- **Encapsulation:** data and the methods that work on it live together in one class, with salary validation.
- **Class variable:** `total_employees` is shared by all objects and counts how many exist.

## Run

```bash
python employee_management.py
```

## Sample Output

```
ID: 102 | Name: Priya Verma | Department: Data Analytics | Designation: Data Analyst | Monthly Salary: Rs.78,000.00
Priya Verma's salary updated: Rs.78,000.00 -> Rs.84,000.00
New annual salary of Priya Verma: Rs.1,008,000.00
Total employees created: 5
```

## Author

Hrishabh Singh Tomar
