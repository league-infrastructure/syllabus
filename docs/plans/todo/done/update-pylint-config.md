---
status: pending
---

# Update Pylint Configuration

The `.pylintrc` sets `max-line-length` to 1120, which effectively
disables line length checking entirely. This is likely a workaround
rather than an intentional style choice and means overly long lines
won't be flagged.

Consider setting a reasonable limit (e.g., 120) or switching to
ruff for faster, more modern linting with sensible defaults.
