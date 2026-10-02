"""Task operations (add, complete, format) used by the CLI."""

from models import Task


def next_id(tasks):
    return max((t.id for t in tasks), default=0) + 1


def add_task(tasks, title, priority="medium"):
    task = Task(id=next_id(tasks), title=title, priority=priority)
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    for task in tasks:
        if task.id == task_id:
            task.done = True
            return task
    raise KeyError(f"No task with id {task_id}")


def format_task(task):
    mark = "x" if task.done else " "
    return f"[{mark}] #{task.id} {task.title} ({task.priority})"