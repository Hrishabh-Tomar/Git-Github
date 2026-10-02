import unittest

import app


class AppTests(unittest.TestCase):
    def test_app_name(self):
        self.assertEqual(app.APP_NAME, "Branching Demo App")


if __name__ == "__main__":
    unittest.main()
