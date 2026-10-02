"""Runnable, self-checking demonstration of the git stash workflow.

Run:  python stash_workflow_demo.py

It builds a throwaway repository in a temp folder and runs the real git commands:

 1. Begin a feature on feature/search-notes and leave it UNCOMMITTED.
 2. git stash push       -> save the unfinished work, working tree becomes clean.
 3. Switch to a hotfix branch, commit an urgent fix, merge it into main.
 4. Return to feature/search-notes (the original branch) and merge main.
 5. git stash list       -> shows the saved entry.
 6. git stash show [-p]  -> shows what the entry changes.
 7. git stash apply      -> restores the work but KEEPS the entry.
 8. git stash drop       -> deletes the entry by hand.
 9. git stash pop        -> restores the work AND deletes the entry (apply + drop).

apply vs pop: both restore the stashed changes. apply leaves the entry in
`git stash list`, so you can reuse it on another branch or keep it as a backup
until you've confirmed everything works, and then remove it with `git stash drop`.
pop drops the entry automatically when it applies cleanly. If there's a conflict,
pop keeps the entry so nothing is lost.
Each claim is checked with an assert below.
"""

import subprocess
import tempfile
from pathlib import Path

BASE_APP = '''_notes = []


def add_note(text):
    _notes.append({"text": text, "done": False})


def list_notes():
    return list(_notes)


def complete_note(index):
    _notes[index]["done"] = True


def reset():
    _notes.clear()
'''

SEARCH_FEATURE = '''

def search_notes(keyword):
    keyword = keyword.lower()
    return [note for note in _notes if keyword in note["text"].lower()]
'''

COUNT_FEATURE = '''

def count_notes():
    return len(_notes)
'''

BUGGY = '''def complete_note(index):
    _notes[index]["done"] = True
'''

FIXED = '''def complete_note(index):
    if not 0 <= index < len(_notes):
        raise ValueError(f"No note at index {index}.")
    _notes[index]["done"] = True
'''


class Repo:
    def __init__(self, path, verbose):
        self.path = Path(path)
        self.verbose = verbose
        self.app = self.path / "notes_app.py"

    def git(self, *args):
        result = subprocess.run(
            ["git", *args], cwd=self.path, capture_output=True, text=True, check=True
        )
        output = (result.stdout + result.stderr).strip()
        if self.verbose:
            print(f"$ git {' '.join(args)}")
            if output:
                print(output)
            print()
        return output

    def write(self, text):
        self.app.write_text(text, encoding="utf-8", newline="\n")

    def read(self):
        return self.app.read_text(encoding="utf-8")

    def stash_entries(self):
        return [line for line in self.git("stash", "list").splitlines() if line]


def step(verbose, title):
    if verbose:
        print(f"===== {title} =====")


def run(verbose=True):
    with tempfile.TemporaryDirectory() as tmp:
        repo = Repo(tmp, verbose)
        repo.git("init", "-q")
        repo.git("checkout", "-q", "-b", "main")
        repo.git("config", "user.name", "Stash Demo")
        repo.git("config", "user.email", "demo@example.com")
        repo.git("config", "core.autocrlf", "false")
        repo.write(BASE_APP)
        repo.git("add", "notes_app.py")
        repo.git("commit", "-q", "-m", "Base notes app")

        step(verbose, "1. Begin an uncommitted feature")
        repo.git("checkout", "-b", "feature/search-notes")
        repo.write(repo.read() + SEARCH_FEATURE)
        assert repo.git("status", "--short") == "M notes_app.py"

        step(verbose, "2. Stash the unfinished work")
        repo.git("stash", "push", "-m", "WIP: search_notes feature")
        assert repo.git("status", "--short") == "", "stash should leave a clean tree"
        assert "search_notes" not in repo.read()

        step(verbose, "3. Switch branches and make the urgent fix")
        repo.git("checkout", "main")
        repo.git("checkout", "-b", "hotfix/complete-note-index")
        repo.write(repo.read().replace(BUGGY, FIXED))
        repo.git("commit", "-q", "-am", "Fix complete_note crash on invalid index")
        repo.git("checkout", "main")
        repo.git("merge", "-q", "--no-ff", "hotfix/complete-note-index",
                 "-m", "Merge hotfix into main")
        assert FIXED in repo.read()

        step(verbose, "4. Return to the original branch")
        repo.git("checkout", "feature/search-notes")
        repo.git("merge", "-q", "main")
        assert FIXED in repo.read()

        step(verbose, "5. git stash list")
        entries = repo.stash_entries()
        assert len(entries) == 1 and "WIP: search_notes feature" in entries[0]

        step(verbose, "6. git stash show")
        assert "notes_app.py" in repo.git("stash", "show")
        assert "+def search_notes(keyword):" in repo.git("stash", "show", "-p")

        step(verbose, "7. git stash apply (entry is KEPT)")
        repo.git("stash", "apply")
        assert "def search_notes" in repo.read() and FIXED in repo.read()
        assert len(repo.stash_entries()) == 1, "apply must keep the stash entry"

        step(verbose, "8. git stash drop")
        repo.git("stash", "drop")
        assert repo.stash_entries() == []

        step(verbose, "9. git stash pop (entry is REMOVED)")
        repo.write(repo.read() + COUNT_FEATURE)
        repo.git("stash", "push", "-m", "WIP: count_notes")
        assert "count_notes" not in repo.read()
        assert len(repo.stash_entries()) == 1
        repo.git("stash", "pop")
        assert "def count_notes" in repo.read()
        assert repo.stash_entries() == [], "pop must remove the stash entry"

        repo.git("commit", "-q", "-am", "Add search_notes and count_notes")
        assert repo.git("status", "--short") == ""

    if verbose:
        print("All stash workflow checks passed.")


if __name__ == "__main__":
    run()
