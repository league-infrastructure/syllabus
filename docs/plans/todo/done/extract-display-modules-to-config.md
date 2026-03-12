---
status: pending
---

# Extract Hardcoded Display Module List to Configuration

The list of Python modules that indicate a lesson needs a display
(`turtle`, `guizero`, `pygame`, `tkinter`) is hardcoded in `util.py`.
This makes it invisible and hard to update.

Move this to a configurable location — either `pyproject.toml` metadata,
a constant at the top of the module, or a config file — so it's easy
to find and extend.
