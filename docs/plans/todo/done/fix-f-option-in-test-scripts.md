---
status: pending
---

# Fix -f option in test scripts

The test justfile has `syl -v -f syllabus.yaml regroup lessons` but there
is no `-f` option on the `regroup` or top-level CLI group. The `-f` / `--file`
option only exists on the `compile` command. Either add a `-f` option to the
CLI group or fix the test scripts to remove the invalid flag.
