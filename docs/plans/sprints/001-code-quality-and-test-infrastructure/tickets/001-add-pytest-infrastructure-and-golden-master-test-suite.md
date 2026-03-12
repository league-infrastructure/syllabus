---
id: "001"
title: "Add pytest infrastructure and golden master test suite"
status: todo
use-cases:
  - SUC-001
depends-on: []
---

# Add pytest infrastructure and golden master test suite

## Description

Add pytest as a dev dependency and create a comprehensive test suite.
Create multiple lesson source fixture directories under `test/` that get
copied to temp dirs during tests (never modified in place). Create golden
master files for syllabus YAML output and directory listings.

## Acceptance Criteria

- [ ] pytest added to dev dependencies in pyproject.toml
- [ ] conftest.py with fixtures that copy source dirs to tmp_path
- [ ] At least two lesson source directories for different test scenarios
- [ ] Golden master YAML files for compile output validation
- [ ] Golden master directory listing files for post-operation validation
- [ ] Unit tests for util.py functions (rank parsing, metadata, display detection)
- [ ] Integration tests for compile_syllabus, renumber, regroup, metafy
- [ ] CLI tests using Click CliRunner
- [ ] All tests pass with `uv run pytest`

## Testing

- **Existing tests to run**: `test/justfile` targets (manual validation)
- **New tests to write**: Full pytest suite as described above
- **Verification command**: `uv run pytest`
