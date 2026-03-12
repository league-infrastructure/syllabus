---
id: "005"
title: "Extract display modules to constant and update pylint config"
status: todo
use-cases: []
depends-on: []
---

# Extract display modules to constant and update pylint config

## Description

Rename the `display_modules` list in `util.py` to `DISPLAY_MODULES` to
follow Python constant naming conventions and make it more visible.
Update `.pylintrc` to use a reasonable `max-line-length` (120) instead
of the current 1120 which effectively disables the check.

## Acceptance Criteria

- [ ] display_modules renamed to DISPLAY_MODULES (uppercase constant)
- [ ] All references updated (needs_display function)
- [ ] .pylintrc max-line-length set to 120
- [ ] No pylint violations introduced at the new line length

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (rename only)
- **Verification command**: `uv run pytest`
