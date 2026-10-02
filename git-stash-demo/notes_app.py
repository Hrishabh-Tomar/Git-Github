"""A tiny notes manager used to demonstrate the git stash workflow."""

_notes = []


def add_note(text):
    _notes.append({"text": text, "done": False})


def list_notes():
    return list(_notes)


def complete_note(index):
    if not 0 <= index < len(_notes):
        raise ValueError(f"No note at index {index}.")
    _notes[index]["done"] = True


def reset():
    """Clear all notes. Used between test runs."""
    _notes.clear()
