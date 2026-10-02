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

    def test_complete_note_invalid_index_raises(self):
        for bad in (0, -1, 5):
            with self.assertRaises(ValueError):
                notes_app.complete_note(bad)

    def test_search_notes_is_case_insensitive(self):
        notes_app.add_note("Buy MILK")
        notes_app.add_note("Call mom")
        self.assertEqual(
            notes_app.search_notes("milk"),
            [{"text": "Buy MILK", "done": False}],
        )

    def test_search_notes_no_match(self):
        notes_app.add_note("Call mom")
        self.assertEqual(notes_app.search_notes("milk"), [])


if __name__ == "__main__":
    unittest.main()
