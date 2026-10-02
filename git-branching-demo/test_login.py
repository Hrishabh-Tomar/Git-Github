import unittest

from login import login


class LoginTests(unittest.TestCase):
    def test_valid_login(self):
        self.assertTrue(login("ada", "lovelace123"))

    def test_wrong_password(self):
        self.assertFalse(login("ada", "nope"))

    def test_unknown_user(self):
        self.assertFalse(login("bob", "x"))


if __name__ == "__main__":
    unittest.main()
