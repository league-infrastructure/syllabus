---
status: pending
---

# Validate Directory Structure Before Operations

The `compile`, `renumber`, `regroup`, and `metafy` commands assume the
input directory is well-formed. If it isn't, failures happen deep in
the processing logic with confusing errors.

Add upfront validation (leveraging the existing `check` command logic)
before running any destructive operation like `renumber` or `regroup`,
so users get a clear early error instead of a mid-operation crash.
