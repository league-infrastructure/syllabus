---
status: approved
---

# Architecture

## Architecture Overview

The system is a CLI tool with four layers:

```
CLI (Click) → Sync Logic → Models (Pydantic) → Utilities
```

- **CLI** (`cli/main.py`): Click commands, argument parsing, logging setup.
- **Sync** (`sync.py`): Core operations — compile, renumber, regroup, metafy, check.
- **Models** (`models.py`): Pydantic data models — Course, Module, LessonSet, Lesson.
- **Utilities** (`util.py`): File parsing, metadata extraction, rank/filename helpers.
- **Where** (`where.py`): Environment detection and syllabus pruning.

## Technology Stack

- Python 3.12+, Click 8.1+, Pydantic v2, python-frontmatter, PyYAML
- Build: Hatchling / uv
- **New this sprint**: pytest for testing

## Component Design

### Component: Test Suite (NEW)

**Purpose**: Validate syllabus operations against known-good outputs.

**Boundary**: Lives in `test/`. Reads from `test/*-source/` fixture
directories. Writes to temp directories only. Never modifies source.

**Use Cases**: SUC-001

Golden master files (`test/golden/`) contain expected YAML output and
directory listings. Tests copy a source directory, run an operation,
and compare results against the golden master.

### Component: Utilities (`util.py`)

**Purpose**: Parse filenames, extract/insert metadata, detect display needs.

**Sprint Changes**: Add type annotations. Extract `display_modules` list
to a module-level constant `DISPLAY_MODULES`.

### Component: Sync (`sync.py`)

**Purpose**: Orchestrate lesson directory operations.

**Sprint Changes**: Add type annotations. Add pre-operation validation
calls. Improve error messages with file paths.

### Component: Models (`models.py`)

**Purpose**: Define the data model for courses, modules, and lessons.

**Sprint Changes**: Remove dead `path_map()` stub.

### Component: `__init__.py`

**Purpose**: Package initialization and version resolution.

**Sprint Changes**: Simplify to single `importlib.metadata.version()` call.

## Data Model

No changes to the data model in this sprint.

## Security Considerations

Not applicable — CLI tool operating on local files only.

## Design Rationale

**Golden master testing over assertion-based testing**: The primary output
of this tool is structured YAML. Comparing full output against committed
reference files catches regressions that individual assertions might miss,
and makes it easy to review what changed when output format evolves.

**Multiple source fixtures**: Different directory structures exercise
different code paths (flat lessons, grouped lessons, lesson sets, nested
modules). Separate source directories keep test concerns isolated.

## Sprint Changes

### Changed Components

- **test/**: New pytest test suite with golden master validation
- **util.py**: Type annotations, `DISPLAY_MODULES` constant
- **sync.py**: Type annotations, pre-operation validation, better errors
- **models.py**: Remove `path_map()` stub
- **`__init__.py`**: Simplify version detection
- **`.pylintrc`**: Reasonable line length
- **`README.md`**: Full documentation
- **`pyproject.toml`**: Add pytest dev dependency

### Migration Concerns

None — no API changes, no data format changes.
