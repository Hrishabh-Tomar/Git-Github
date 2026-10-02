"""Runnable, self-checking demonstration of a Git merge conflict.

Run:  python conflict_demo.py

It builds a throwaway repository in a temp folder and:
 1. commits a base file,
 2. creates two branches from that same base,
 3. changes the SAME line differently on each branch,
 4. merges the first branch into main (clean),
 5. merges the second branch (CONFLICT), printing the conflict markers,
 6. resolves the file by hand, commits the merge, and checks the final result.
"""

import subprocess
import tempfile
from pathlib import Path

BASE = 'def greet(name):\n    return f"Hello, {name}"\n'
BRANCH_A = 'def greet(name):\n    return f"Welcome, {name}!"\n'
BRANCH_B = 'def greet(name):\n    return f"Hey {name}, nice to see you."\n'
RESOLVED = 'def greet(name):\n    return f"Welcome, {name}! Nice to see you."\n'


def run(verbose=True):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        target = path / "greeting.py"

        def git(*args, check=True):
            result = subprocess.run(["git", *args], cwd=path, capture_output=True, text=True)
            output = (result.stdout + result.stderr).strip()
            if verbose:
                print(f"$ git {' '.join(args)}")
                if output:
                    print(output)
                print()
            if check and result.returncode != 0:
                raise RuntimeError(output)
            return result.returncode, output

        def write(text):
            target.write_text(text, encoding="utf-8", newline="\n")

        git("init", "-q")
        git("checkout", "-q", "-b", "main")
        git("config", "user.name", "Conflict Demo")
        git("config", "user.email", "demo@example.com")
        git("config", "core.autocrlf", "false")
        write(BASE)
        git("add", "greeting.py")
        git("commit", "-q", "-m", "Base greeting")

        git("branch", "feature/welcome")
        git("branch", "feature/friendly")

        git("checkout", "-q", "feature/welcome")
        write(BRANCH_A)
        git("commit", "-q", "-am", "Formal welcome")
        git("checkout", "-q", "feature/friendly")
        write(BRANCH_B)
        git("commit", "-q", "-am", "Casual greeting")

        git("checkout", "-q", "main")
        code, _ = git("merge", "--no-ff", "-m", "Merge welcome", "feature/welcome")
        assert code == 0, "first merge must be clean"

        code, output = git("merge", "--no-ff", "feature/friendly", check=False)
        assert code != 0 and "CONFLICT" in output, "second merge must conflict"

        conflicted = target.read_text(encoding="utf-8")
        if verbose:
            print("----- greeting.py with conflict markers -----")
            print(conflicted)
        assert "<<<<<<< HEAD" in conflicted
        assert "=======" in conflicted
        assert ">>>>>>> feature/friendly" in conflicted
        assert 'f"Welcome, {name}!"' in conflicted and "nice to see you" in conflicted

        write(RESOLVED)
        git("add", "greeting.py")
        git("commit", "-q", "-m", "Merge friendly, resolving conflict")

        final = target.read_text(encoding="utf-8")
        assert "<<<<<<<" not in final and ">>>>>>>" not in final
        assert final == RESOLVED
        _, parents = git("log", "-1", "--format=%p")
        assert len(parents.split()) == 2, "final commit must be a two-parent merge"
        _, status = git("status", "--short")
        assert status == ""

    if verbose:
        print("All merge conflict checks passed.")


if __name__ == "__main__":
    run()
