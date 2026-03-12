---
status: pending
---

# Improve Error Messages and Validation

Several functions raise generic `ValueError` with minimal context,
making it hard to diagnose issues. For example, metadata extraction
failures and invalid directory structures produce vague errors.

Improve by:
- Including the file path and what was expected vs. found
- Adding pre-flight validation in `compile_syllabus()` before processing
- Using custom exception classes where appropriate
