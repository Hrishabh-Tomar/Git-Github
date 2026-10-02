"""Unit tests for the task tracker. Run with: python -m unittest"""

import tempfile
import unittest
from pathlib import Path

from models import Task
from storage import load_tasks, save_tasks
from utils import add_task, complete_task


class TaskTests(unittest.TestCase):
    def test_invalid_priority_raises(self):
        with self.assertRaises(ValueError):
            Task(id=1, title="x", priority="urgent")

    def test_add_and_complete(self):
        tasks = []
        task = add_task(tasks, "Write tests", "high")
        self.assertEqual(task.id, 1)
        complete_task(tasks, 1)
        self.assertTrue(tasks[0].done)

    def test_complete_missing_task_raises(self):
        with self.assertRaises(KeyError):
            complete_task([], 99)

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            save_tasks([Task(id=1, title="a", priority="low")], path)
            loaded = load_tasks(path)
        self.assertEqual(loaded, [Task(id=1, title="a", priority="low")])


if __name__ == "__main__":
    unittest.main()