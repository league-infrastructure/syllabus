---
id: "003"
title: "Add type hints to sync.py and util.py"
status: todo
use-cases: []
depends-on: []
---

# Add type hints to sync.py and util.py

## Description

Add complete type annotations to all functions in `sync.py` and `util.py`.
These modules have many functions with missing or incomplete type hints.

## Acceptance Criteria

- [ ] All functions in util.py have parameter and return type annotations
- [ ] All functions in sync.py have parameter and return type annotations
- [ ] Code still runs correctly after annotations are added

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (type hints don't change behavior)
- **Verification command**: `uv run pytest`
