---
status: approved
---

# Project Overview

## Project Name

JTL Syllabus (`jtl-syllabus`)

## Problem Statement

The LEAGUE of Amazing Programmers (jointheleague.org) maintains a coding
curriculum as directories of lesson files (Python, Jupyter notebooks,
Markdown). These directories need to be compiled into structured YAML
syllabus files that downstream systems (LMS, grading, course delivery)
can consume. Without tooling, managing lesson ordering, metadata (UIDs,
display requirements), and directory structure is manual and error-prone.

## Target Users

- **Curriculum developers** at The LEAGUE who create and maintain lesson
  content as files in a directory tree.
- **Infrastructure/DevOps** who integrate the compiled syllabus YAML into
  course delivery systems.
- **Instructors** who need stable, well-ordered syllabi for their classes.

## Key Constraints

- Python 3.12+ required (uses `Path.walk()`, `tomllib`).
- Must handle three lesson file formats: Markdown (`.md`), Python (`.py`),
  Jupyter notebooks (`.ipynb`).
- Metadata must be stable — UIDs, once assigned, must persist across
  recompilations.
- The tool is a CLI (`syl`) distributed via PyPI as `jtl-syllabus`.
- Single maintainer; process should be lightweight.

## High-Level Requirements

1. **Compile**: Read a lesson directory tree and produce a structured YAML
   syllabus with courses, modules, lesson sets, and lessons.
2. **Renumber**: Renumber lessons with configurable increments to allow
   inserting new content without renaming everything.
3. **Regroup**: Automatically group files with the same base name (e.g.,
   `20_Crazy_Tina.py` and `20_Crazy_Tina.md`) into a single lesson
   directory.
4. **Metafy**: Generate and insert metadata (UIDs, names) into lesson
   files and README frontmatter.
5. **Check**: Validate that a lesson directory conforms to the expected
   structure (ranked directories, no loose files at top level).
6. **Environment pruning**: Filter syllabus content based on runtime
   environment (local, CodeSpaces, League Codeserver).
7. **Detect display requirements**: Automatically flag lessons that import
   GUI modules (turtle, guizero, pygame, tkinter).

## Technology Stack

- **Language**: Python 3.12+
- **CLI framework**: Click 8.1+
- **Data models**: Pydantic v2
- **Metadata handling**: python-frontmatter, PyYAML
- **Build system**: Hatchling (PEP 517)
- **Package manager**: uv
- **Distribution**: PyPI (`jtl-syllabus` → `syl` CLI entry point)

## Sprint Roadmap

- **Sprint 001**: Code quality and test infrastructure — add automated
  tests with golden master validation, improve type hints, error messages,
  configuration, and documentation. Clean up dead code and simplify
  version detection.

## Out of Scope

- GUI or web interface for curriculum editing.
- Runtime lesson delivery or student-facing features.
- Integration with specific LMS APIs (the tool produces YAML; consumers
  handle integration).
- CI/CD pipeline (stakeholder prefers pre-push validation over post-push).
