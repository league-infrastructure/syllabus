---
id: "001"
title: "Code Quality and Test Infrastructure"
status: active
branch: sprint/001-code-quality-and-test-infrastructure
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
---

# Sprint 001: Code Quality and Test Infrastructure

## Goals

Establish automated testing with golden master validation, improve code
quality (type hints, error messages, dead code removal), and update
project configuration and documentation to modern standards.

## Problem

The project has zero automated tests, incomplete type annotations,
hardcoded configuration values, generic error messages, dead code stubs,
overly permissive linting, complex version detection, and a nearly empty
README. These issues make the codebase fragile and hard to maintain.

## Solution

1. Add a pytest test suite with golden master files for syllabus YAML
   output and directory structure validation.
2. Create multiple test lesson source directories that get copied (not
   modified) during tests.
3. Clean up code: remove dead `path_map()`, simplify `__init__.py`,
   extract display modules to a constant, add type hints, improve
   error messages with file paths and context.
4. Update pylint config to a reasonable line length.
5. Rewrite README with install/usage docs.
6. Add pre-operation directory validation.

## Success Criteria

- `pytest` runs and passes with tests covering all major modules.
- Golden master YAML and directory listing files validate compilation
  output.
- All functions in `sync.py` and `util.py` have type annotations.
- Error messages include file paths and expected-vs-found context.
- README documents installation and CLI usage.
- No dead code stubs remain.

## Scope

### In Scope

- Automated pytest test suite with golden masters
- Multiple test lesson source fixtures
- Type hints for sync.py and util.py
- Error message improvements
- Display modules extracted to module-level constant
- Version detection simplification
- path_map() removal
- Pylint config update
- README rewrite
- Pre-operation directory validation

### Out of Scope

- CI/CD pipeline (stakeholder preference: pre-push, not post-push)
- New features or CLI commands
- Refactoring the core compilation algorithm

## Test Strategy

- **Unit tests**: Test individual functions in `util.py` (filename parsing,
  rank extraction, metadata read/write, display detection).
- **Integration tests**: Test `compile_syllabus()`, `renumber_lessons()`,
  `regroup_lessons()`, `metafy_lessons()` using copied lesson source
  directories.
- **Golden master tests**: Compare compiled syllabus YAML and post-process
  directory listings against committed reference files.
- **CLI tests**: Use Click's `CliRunner` to test command invocation.
- **Fixture strategy**: Multiple `test/*-source/` directories that get
  copied to temp dirs before each test. Source dirs are never modified.

## Architecture Notes

No architectural changes — this sprint improves code quality and adds
test infrastructure without changing the system's structure.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

- #001: Add pytest infrastructure and golden master test suite
- #002: Remove dead code and simplify version detection
- #003: Add type hints to sync.py and util.py
- #004: Improve error messages and add pre-operation validation
- #005: Extract display modules to constant and update pylint config
- #006: Rewrite README with install and usage documentation
