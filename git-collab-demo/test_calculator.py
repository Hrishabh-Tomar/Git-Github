import unittest

from calculator import calculate


class CalculatorTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculate(2, "+", 3), 5)

    def test_subtract(self):
        self.assertEqual(calculate(5, "-", 3), 2)

    def test_multiply(self):
        self.assertEqual(calculate(4, "*", 3), 12)

    def test_divide(self):
        self.assertEqual(calculate(9, "/", 3), 3)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ValueError):
            calculate(1, "/", 0)

    def test_unsupported_operator_raises(self):
        with self.assertRaises(ValueError):
            calculate(1, "^", 2)


if __name__ == "__main__":
    unittest.main()
