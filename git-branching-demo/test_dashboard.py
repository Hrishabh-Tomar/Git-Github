import unittest

from dashboard import render_dashboard


class DashboardTests(unittest.TestCase):
    def test_render_with_notifications(self):
        text = render_dashboard("ada", ["Welcome"])
        self.assertIn("Dashboard for ada", text)
        self.assertIn("Notifications: 1", text)
        self.assertIn("  - Welcome", text)

    def test_render_empty(self):
        self.assertIn("Notifications: 0", render_dashboard("ada", []))


if __name__ == "__main__":
    unittest.main()
