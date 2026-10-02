"""Command-line entry point for the task tracker.

Usage:
    python main.py add "Write report" --priority high
    python main.py list
    python main.py done 1
"""

import argparse

from storage import load_tasks, save_tasks
from utils import add_task, complete_task, format_task, pending_tasks


def build_parser():
    parser = argparse.ArgumentParser(description="Simple task tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add a new task")
    add.add_argument("title")
    add.add_argument("--priority", default="medium", choices=["low", "medium", "high"])

    list_cmd = sub.add_parser("list", help="List tasks")
    list_cmd.add_argument("--pending", action="store_true", help="Hide completed tasks")

    done = sub.add_parser("done", help="Mark a task as done")
    done.add_argument("task_id", type=int)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    tasks = load_tasks()

    if args.command == "add":
        task = add_task(tasks, args.title, args.priority)
        save_tasks(tasks)
        print(f"Added: {format_task(task)}")
    elif args.command == "list":
        shown = pending_tasks(tasks) if args.pending else tasks
        if not shown:
            print("No tasks to show.")
        for task in shown:
            print(format_task(task))
    elif args.command == "done":
        task = complete_task(tasks, args.task_id)
        save_tasks(tasks)
        print(f"Completed: {format_task(task)}")


if __name__ == "__main__":
    main()