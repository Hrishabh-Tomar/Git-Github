import unittest

from greeting import farewell, greet


class GreetingTests(unittest.TestCase):
    def test_greet_mentions_name(self):
        self.assertIn("Ada", greet("Ada"))

    def test_farewell(self):
        self.assertEqual(farewell("Ada"), "Goodbye, Ada")


if __name__ == "__main__":
    unittest.main()
