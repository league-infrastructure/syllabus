---
status: pending
---

# Complete Type Hints Across sync.py and util.py

The Pydantic models in `models.py` are well-typed, but `sync.py` and
`util.py` have many functions with missing or incomplete type
annotations. Adding full type hints would improve IDE support, catch
bugs statically, and make the code easier to reason about.

Consider adding a mypy or pyright check to the dev workflow once hints
are in place.
