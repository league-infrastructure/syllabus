---
id: "008"
title: "Replace Makefile with justfile"
status: todo
use-cases: []
depends-on: []
---

# Replace Makefile with justfile

## Description

Replace the top-level Makefile with a justfile for consistency with the
test directory (which already uses just) and for cleaner syntax. Port
all existing targets: ver, compile, push, publish, build, setup.

## Acceptance Criteria

- [ ] justfile created at project root with all Makefile targets ported
- [ ] Makefile removed
- [ ] All targets work correctly (`just build`, `just setup`, etc.)

## Testing

- **Existing tests to run**: Run each target manually
- **New tests to write**: None
- **Verification command**: `just build`
