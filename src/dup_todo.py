#!/usr/bin/env python3
"""dup‑todo‑cli – a tiny todo list with duplicate detection.

Features
--------
* Simple text storage (`~/.dup_todo.txt`).
* Automatic duplicate checking when adding items.
* Small, typed, and fully unit‑tested.
* Configurable logging (JSON or human‑readable) via ``--log-format``.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import List

# ---------------------------------------------------------------------------
# Logging configuration – flexible but sane defaults
# ---------------------------------------------------------------------------

def configure_logging(level: str = "INFO", json_format: bool = False) -> None:
    """Configure the root logger.

    Parameters
    ----------
    level: str
        Logging level name (e.g. ``"DEBUG"``).
    json_format: bool
        If ``True`` emit JSON lines, otherwise the classic ``%(level)s: %(msg)s``.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    handler = logging.StreamHandler()
    if json_format:
        formatter = logging.Formatter(
            json.dumps({
                "time": "%(asctime)s",
                "level": "%(levelname)s",
                "msg": "%(message)s",
                "module": "%(module)s",
                "func": "%(funcName)s",
            })
        )
    else:
        formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logging.basicConfig(level=log_level, handlers=[handler])

# ---------------------------------------------------------------------------
# Core todo handling
# ---------------------------------------------------------------------------

def _todo_path() -> Path:
    """Return the Path object for the todo file.

    The file lives in the user's home directory and is hidden to avoid accidental
    commits.
    """
    return Path(os.getenv("HOME", ".")).joinpath(".dup_todo.txt")


def load_tasks() -> List[str]:
    """Load all tasks from the storage file, stripping newlines.
    Returns an empty list if the file does not exist.
    """
    p = _todo_path()
    if not p.exists():
        return []
    return [line.rstrip("\n") for line in p.read_text(encoding="utf-8").splitlines()]


def save_tasks(tasks: List[str]) -> None:
    """Write the list of *tasks* back to disk.
    The function is atomic – it writes to a temporary file and then renames.
    """
    p = _todo_path()
    tmp = p.with_suffix(".tmp")
    tmp.write_text("\n".join(tasks) + "\n", encoding="utf-8")
    tmp.replace(p)


def add_task(task: str) -> None:
    """Add *task* to the todo list.

    Raises
    ------
    ValueError
        If the exact text is already present (case‑sensitive).
    """
    tasks = load_tasks()
    if task in tasks:
        raise ValueError(f"Duplicate task detected: '{task}'")
    tasks.append(task)
    save_tasks(tasks)
    logging.info("Added task: %s", task)


def list_tasks() -> None:
    """Print all tasks with line numbers.
    """
    tasks = load_tasks()
    if not tasks:
        print("✅ No tasks – you are free!")
        return
    for idx, txt in enumerate(tasks, start=1):
        print(f"{idx}. {txt}")


def remove_task(index: int) -> None:
    """Remove the task at *index* (1‑based).

    Raises
    ------
    IndexError
        If *index* is out of range.
    """
    tasks = load_tasks()
    if not 1 <= index <= len(tasks):
        raise IndexError(f"Task number {index} does not exist (1‑{len(tasks)})")
    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    logging.info("Removed task #%d: %s", index, removed)

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dup‑todo", description="Simple todo list with duplicate detection")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, …)")
    parser.add_argument("--log-json", action="store_true", help="Emit logs as JSON lines")

    sub = parser.add_subparsers(dest="cmd", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new task (fails on duplicate)")
    p_add.add_argument("task", help="Task description (exact match used for duplicate detection)")

    # list
    sub.add_parser("list", help="Show all tasks")

    # rm
    p_rm = sub.add_parser("rm", help="Remove a task by its number")
    p_rm.add_argument("num", type=int, help="Task number as shown by `list`")

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.log_level, args.log_json)

    try:
        if args.cmd == "add":
            add_task(args.task)
        elif args.cmd == "list":
            list_tasks()
        elif args.cmd == "rm":
            remove_task(args.num)
        else:
            parser.error("unknown command")
    except Exception as exc:  # pragma: no cover – exercised via tests
        logging.error(str(exc))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
