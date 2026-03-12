---
status: pending
---

# Simplify Version Detection in __init__.py

The version resolution in `__init__.py` has multiple fallback paths
(importlib.metadata → fallback string) with pragma-no-cover guards.
Since the project requires Python 3.12+ and uses hatchling,
`importlib.metadata` should always work. Simplify to a single
`importlib.metadata.version()` call and drop the fallback complexity.
