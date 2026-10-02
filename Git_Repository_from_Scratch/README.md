# Task Tracker

A small command-line task manager written in Python, with no third-party dependencies. It was built as a hands-on project to practise a complete Git workflow, from a local repository to a published GitHub repository.

## Features

- Add tasks with a priority (`low`, `medium`, `high`)
- List all tasks, or only pending ones with `--pending`
- Mark tasks as done
- Tasks are saved to a local `tasks.json` file, which is ignored by Git
- Input validation and unit tests

## Requirements

- Python 3.8 or newer
- Git

## Getting Started

```bash
git clone https://github.com/<your-username>/task-tracker.git
cd task-tracker
```

## Usage

```bash
# Add tasks
python main.py add "Write report" --priority high
python main.py add "Buy groceries"

# List tasks
python main.py list
python main.py list --pending

# Mark task 1 as done
python main.py done 1
```

Example output:

```
Added: [ ] #1 Write report (high)
Added: [ ] #2 Buy groceries (medium)
Completed: [x] #1 Write report (high)
```

## Running the Tests

```bash
python -m unittest
```

## Project Structure

| File            | Purpose                                   |
|-----------------|-------------------------------------------|
| `main.py`       | Command-line interface                    |
| `models.py`     | `Task` data model with priority validation |
| `storage.py`    | Load and save tasks as JSON               |
| `utils.py`      | Task operations and formatting helpers    |
| `test_tasks.py` | Unit tests                                |
| `.gitignore`    | Keeps `tasks.json`, `__pycache__/` and similar files out of Git |

## Git Commands Demonstrated

| Command | Why it is used |
|---------|----------------|
| `git init` | Creates a new repository in the project folder |
| `git status` | Shows which files are untracked, modified or staged |
| `git add` | Stages selected changes for the next commit |
| `git commit -m` | Saves a snapshot of the staged changes with a message |
| `git log --oneline` | Shows the commit history in a compact form |
| `git diff` | Shows line-by-line changes that are not yet staged |
| `.gitignore` | Stops generated and local files from being tracked |
| `git remote add origin` | Links the local repository to GitHub |
| `git push -u origin main` | Uploads the commit history to GitHub |

## Commit History Overview

1. Add README and `.gitignore`
2. Add `Task` data model with priority validation
3. Add JSON storage layer
4. Add task operations and CLI entry point
5. Add `pending_tasks` helper and unit tests
6. Add `--pending` flag to the `list` command
7. Document features, usage and project structure in the README

## Author

Hrishabh Singh Tomar
