---
id: "004"
title: "Improve error messages and add pre-operation validation"
status: todo
use-cases:
  - SUC-002
depends-on: []
---

# Improve error messages and add pre-operation validation

## Description

Improve error messages throughout the codebase to include file paths and
expected-vs-found context. Add pre-operation directory validation to
`compile_syllabus()` so users get clear early errors instead of crashes
mid-operation. `renumber_lessons()` and `regroup_lessons()` already call
`check_structure()` — ensure `compile_syllabus()` does too.

## Acceptance Criteria

- [ ] compile_syllabus() calls check_structure() before processing
- [ ] ValueError messages include the file path and what was expected
- [ ] check_structure() error messages are clear and actionable

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: Tests that pass invalid directory structures and verify error messages
- **Verification command**: `uv run pytest`
