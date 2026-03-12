---
id: "007"
title: "Fix -f option in test scripts"
status: todo
use-cases: []
depends-on: []
---

# Fix -f option in test scripts

## Description

The test justfile has `syl -v -f syllabus.yaml regroup lessons` but there
is no `-f` option on the top-level CLI group or the `regroup` command.
The `-f` / `--file` option only exists on `compile`. Remove the invalid
`-f` flag from the test scripts.

## Acceptance Criteria

- [ ] test/justfile updated to remove invalid -f flags
- [ ] All justfile targets use valid CLI options

## Testing

- **Existing tests to run**: Run the updated justfile targets manually
- **New tests to write**: None
- **Verification command**: `cd test && just test1`
