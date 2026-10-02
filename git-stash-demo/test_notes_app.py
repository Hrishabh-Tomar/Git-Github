import unittest

import notes_app


class NotesAppTests(unittest.TestCase):
    def setUp(self):
        notes_app.reset()

    def test_add_and_list(self):
        notes_app.add_note("Buy milk")
        self.assertEqual(notes_app.list_notes(), [{"text": "Buy milk", "done": False}])

    def test_complete_note(self):
        notes_app.add_note("Buy milk")
        notes_app.complete_note(0)
        self.assertTrue(notes_app.list_notes()[0]["done"])


if __name__ == "__main__":
    unittest.main()
