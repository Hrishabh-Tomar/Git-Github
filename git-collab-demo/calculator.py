"""A tiny command-line calculator: add, subtract, multiply, divide."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a, operator, b):
    if operator not in OPERATIONS:
        raise ValueError(f"Unsupported operator: {operator!r}")
    return OPERATIONS[operator](a, b)


def main():
    print("Simple Calculator (type 'quit' to exit)")
    while True:
        expression = input("Enter expression (e.g. 3 + 4): ").strip()
        if expression.lower() == "quit":
            break
        try:
            a_str, operator, b_str = expression.split()
            result = calculate(float(a_str), operator, float(b_str))
            print(f"Result: {result}")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
