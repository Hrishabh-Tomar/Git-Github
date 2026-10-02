"""JSON file persistence for tasks."""

import json
from pathlib import Path

from models import Task

DEFAULT_PATH = Path("tasks.json")


def load_tasks(path=DEFAULT_PATH):
    """Return the list of saved tasks (empty list if no file exists yet)."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return [Task.from_dict(item) for item in json.load(f)]


def save_tasks(tasks, path=DEFAULT_PATH):
    """Write the given tasks to disk as JSON."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)