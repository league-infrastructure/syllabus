---
status: pending
---

# Replace the Makefile with a Justfile

The project currently uses a Makefile for build/publish/setup tasks.
Replace it with a justfile for consistency with the test directory
(which already uses just) and for better cross-platform support and
cleaner syntax.
