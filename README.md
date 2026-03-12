# JTL Syllabus

The `syl` CLI compiles structured YAML syllabus files from a directory tree
of lesson files (Python, Jupyter notebooks, Markdown), in support of
[The LEAGUE of Amazing Programmers](https://jointheleague.org) coding
curriculum.

## Installation

```bash
pip install jtl-syllabus
```

This installs the `syl` command.

## Usage

All commands operate on a lesson directory (defaults to `./lessons`).
Use `-l` to specify a different path.

### Compile a syllabus

```bash
syl compile
syl compile -l path/to/lessons
syl compile -f output.yaml          # custom output path
syl compile -ngm -i100              # regroup, renumber (increment 100), metafy, then compile
```

### Check directory structure

```bash
syl check
```

Validates that the lesson directory follows the expected structure:
ranked module directories at the top level, no loose files.

### Renumber lessons

```bash
syl renumber                        # renumber with increment 1
syl renumber -i 100                 # renumber with increment 100
syl renumber -d                     # dry run (show changes without renaming)
```

### Regroup lessons

```bash
syl regroup                         # group files with same basename into directories
syl regroup -d                      # dry run
```

Groups files that share the same rank and base name (e.g., `20_Loops.py`
and `20_Loops.md`) into a single lesson directory.

### Add metadata

```bash
syl meta                            # add UIDs and names to all lesson files
syl meta -d                         # dry run
```

Ensures every module, lesson set, and lesson has a `uid` and `name` in
its metadata (README frontmatter, Python comments, or notebook metadata).

### Global options

```
-v, -vv          Increase verbosity (info / debug)
-e               Raise exceptions on errors
-d PATH          Set working directory
-l PATH          Set lesson directory (default: ./lessons)
```

## Lesson directory structure

```
lessons/
  README.md                    # Course-level metadata
  10_Module_Name/              # Module (ranked directory)
    README.md                  # Module metadata
    10_Lesson.py               # Lesson file
    20_Lesson.ipynb             # Lesson file
    30_Grouped_Lesson/          # Lesson directory (multiple files)
      Grouped_Lesson.py
      README.md
    01_Lesson_Set/              # Lesson set (nested group)
      10_Sub_Lesson.py
      20_Sub_Lesson.ipynb
  20_Another_Module/
    ...
```

See [docs/course_structure.md](docs/course_structure.md) for the full
hierarchy and [docs/metadata.md](docs/metadata.md) for metadata formats.
