---
id: "002"
title: "Remove dead code and simplify version detection"
status: todo
use-cases: []
depends-on: []
---

# Remove dead code and simplify version detection

## Description

Remove the unimplemented `path_map()` stub from `Course` in `models.py`.
Simplify version detection in `__init__.py` — since Python 3.12+ is
required and hatchling is the build backend, `importlib.metadata.version()`
should always work. Remove the pyproject.toml fallback complexity.

## Acceptance Criteria

- [ ] `path_map()` method removed from Course class
- [ ] `__init__.py` simplified to use only importlib.metadata.version()
- [ ] Package still imports and reports version correctly
- [ ] No dead code stubs remain

## Testing

- **Existing tests to run**: `python -c "from syllabus import __version__; print(__version__)"`
- **New tests to write**: None (covered by import tests in ticket 001)
- **Verification command**: `uv run pytest`
