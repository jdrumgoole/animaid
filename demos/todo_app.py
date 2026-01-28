#!/usr/bin/env python3
"""Demo: Todo App

Demonstrates: Complete mini app with CRUD operations, styling for state.

Shows a simulated todo list that:
- Adds tasks one by one
- Marks some as complete (strikethrough + muted styling)
- Removes completed tasks
"""

import time

from animaid import Animate, HTMLList, HTMLString


def main() -> None:
    print("Starting Todo App Demo...")
    print("Watch tasks being added, completed, and removed!")
    print()

    with Animate(title="Demo: Todo List") as anim:
        # Title
        title = HTMLString("My Todo List").bold().xxl()
        anim.add(title)

        # Status display
        status = HTMLString("Adding tasks...").muted()
        status_id = anim.add(status)

        # Initialize empty todo list with menu styling
        todos = HTMLList([]).menu().gap("8px")
        anim.add(todos)

        time.sleep(1)

        # Tasks to add
        tasks = [
            "Buy groceries",
            "Walk the dog",
            "Finish report",
            "Call mom",
            "Clean kitchen",
        ]

        # Add tasks one by one
        print("Adding tasks:")
        for task in tasks:
            task_item = HTMLString(task)
            todos.append(task_item)
            print(f"  + {task}")
            time.sleep(0.4)

        print()
        time.sleep(0.5)

        # Mark some tasks as complete
        status = HTMLString("Completing tasks...").muted()
        anim.update(status_id, status)

        print("Completing tasks:")
        completed_indices = [0, 2, 4]  # Complete every other task

        for idx in completed_indices:
            task_text = str(todos[idx])
            # Replace with completed version (strikethrough + muted)
            completed_task = HTMLString(task_text).strikethrough().gray()
            todos[idx] = completed_task
            print(f"  [x] {task_text}")
            time.sleep(0.4)

        print()
        time.sleep(0.5)

        # Remove completed tasks (work backwards to maintain indices)
        status = HTMLString("Removing completed tasks...").muted()
        anim.update(status_id, status)

        print("Removing completed tasks:")
        for idx in sorted(completed_indices, reverse=True):
            task_text = str(todos[idx])
            print(f"  - {task_text}")
            todos.pop(idx)
            time.sleep(0.4)

        print()

        # Final status
        remaining = len(todos)
        status = HTMLString(f"{remaining} tasks remaining").info()
        anim.update(status_id, status)

        print(f"Done! {remaining} tasks remaining.")

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
