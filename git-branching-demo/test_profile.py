import unittest

from profile import build_profile


class ProfileTests(unittest.TestCase):
    def test_build_profile(self):
        self.assertEqual(
            build_profile("ada", "ada@example.com"),
            {"username": "ada", "email": "ada@example.com"},
        )

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            build_profile("ada", "not-an-email")


if __name__ == "__main__":
    unittest.main()
