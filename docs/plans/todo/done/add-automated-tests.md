---
status: pending
---

# Add Automated Unit Tests

The project has no automated tests — only manual end-to-end testing via
the `test/justfile`. This means regressions can slip through undetected.

Add a pytest-based test suite covering at minimum:
- `models.py` — serialization, sorting, metadata extraction
- `util.py` — filename parsing, rank extraction, metadata read/write
- `sync.py` — compile, renumber, regroup, metafy logic
- `cli/main.py` — CLI invocation via Click's CliRunner

Use the existing `test/lessons-source/` as fixture data.
