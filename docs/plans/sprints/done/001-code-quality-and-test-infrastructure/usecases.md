---
status: approved
---

# Sprint 001 Use Cases

## SUC-001: Run Automated Tests After Code Changes
Parent: (none — new capability)

- **Actor**: Developer
- **Preconditions**: Project is checked out, dev dependencies installed
- **Main Flow**:
  1. Developer makes code changes to syllabus package.
  2. Developer runs `pytest` from the project root.
  3. Tests copy lesson source fixtures to temp directories.
  4. Tests exercise compile, renumber, regroup, metafy, and check functions.
  5. Golden master tests compare output YAML and directory listings against
     committed reference files.
  6. All tests pass or fail with clear diagnostics.
- **Postconditions**: Developer knows whether changes broke existing behavior.
- **Acceptance Criteria**:
  - [x] `pytest` discovers and runs all tests
  - [x] Tests use copied fixtures, never modifying source directories
  - [x] Golden master comparisons produce clear diffs on failure

## SUC-002: Get Clear Error Messages on Invalid Input
Parent: (none — improvement)

- **Actor**: Curriculum developer
- **Preconditions**: User has a lesson directory with structural issues
- **Main Flow**:
  1. User runs `syl compile` on a malformed lesson directory.
  2. System validates directory structure before processing.
  3. System reports the specific file/directory and what's wrong.
- **Postconditions**: User can fix the issue without guessing.
- **Acceptance Criteria**:
  - [x] Errors include file path and expected-vs-found description
  - [x] Destructive operations (renumber, regroup) validate before modifying

## SUC-003: Understand and Install the Tool from README
Parent: (none — documentation)

- **Actor**: New user or contributor
- **Preconditions**: User discovers the project on PyPI or GitHub
- **Main Flow**:
  1. User reads README.md.
  2. README explains what the tool does, how to install, and how to use it.
  3. User installs via `pip install jtl-syllabus` and runs `syl --help`.
- **Postconditions**: User can use the tool without reading source code.
- **Acceptance Criteria**:
  - [x] README has project description, install instructions, usage examples
