# dup‑todo‑cli

A **single‑file**, zero‑dependency Python CLI for managing a personal todo list.

* Detects and rejects duplicate tasks automatically.
* Stores items in a plain‑text file (`~/.dup_todo.txt`).
* Fully typed, unit‑tested, and lint‑checked.
* Includes a tiny GitHub Actions workflow that runs:
  * `ruff` linting
  * `pytest` unit tests with coverage
  * `bandit` security scan
  * caching of `pip` packages
  * SHA‑pinned actions and read‑only `GITHUB_TOKEN` defaults.

## Install
```bash
pip install --user git+https://github.com/your‑handle/dup‑todo‑cli.git
```

## Usage
```bash
# add a task (fails if the text already exists)
dup-todo add "Buy milk"

# list all tasks
dup-todo list

# remove a task by its line number
dup-todo rm 2
```

## Development
```bash
# clone, create a virtualenv and install dev deps
git clone https://github.com/your‑handle/dup‑todo‑cli.git
cd dup-todo-cli
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
Run the test suite:
```bash
pytest -q
```

## CI status
[![CI](https://github.com/your-handle/dup-todo-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/your-handle/dup-todo-cli/actions)
