## Metadata

Each lesson / exercise can (optionally) carry explicit metadata. If you omit it,
the system derives sensible defaults from filenames and code contents. You only
need to add or edit metadata when you want to (a) control the human readable
title, or (b) provide / pin a stable unique identifier (`uid`) that other
systems (LMS, grading, linking) can depend on.

### Automatically derived fields

Without any manual metadata the compiler infers:

* `name`  – Cleaned from the filename (numeric rank and underscores removed).
  For a directory lesson, the directory name. For a Markdown lesson with a `#
  Heading` the heading overrides the filename unless you set `name` explicitly
  in frontmatter.
* `display` – `true` if a Python exercise imports any of: `turtle`, `guizero`,
  `pygame`, `tkinter`; else `false`.
* `lesson` – Path to the first Markdown (`.md`) file in a lesson (or the README
  inside a lesson directory).
* `exercise` – Path to the primary code file (`.py`, `.ipynb`) when present.
* `uid` – Added only when you run the metadata generation command (`meta` /
  `--metafy`). If you never run it and never set one manually, an object may
  have `uid: false` (unset) in the internal model.

### Where metadata can live

You may supply / override metadata in any (or all) of these places:

1. Markdown frontmatter (YAML at the top of a `.md` file or a `README.md`).
2. Notebook–level metadata under the JSON key `metadata.syllabus` inside a `.ipynb` file.
3. Special comment lines near the top of a Python file: lines beginning with `#` followed by `key: value`.

Only keys that match fields on the `Lesson` model are applied: `name`,
`description`, `uid`, `display`, `terminal`, `lesson`, `exercise`, `exer_test`,
`assessment`.

Later sources encountered while building a lesson can override earlier implicit
values (e.g. a `name` set in frontmatter overrides the cleaned filename).

### The two critical fields

| Field | Purpose | Notes |
|-------|---------|-------|
| `uid` | Stable opaque identifier | Generate once and keep. Do NOT encode meaning; treat as a primary key. |
| `name` | Human‑readable title | Shown in syllabus outputs. Provide concise, student‑facing wording. |

If you do nothing, `name` is auto derived; `uid` is only created when you run
the metafy step (see below). For long‑term references you should explicitly set
(or lock in) a `uid` early; otherwise a regenerated random one might appear if
you delete / recreate files.

### Generating / inserting missing uids

Use the CLI to populate uids everywhere they are missing:

```
syl meta path/to/lessons
```

Or as part of a compile:

```
syl compile -m path/to/lessons
```

This will:
* Ensure every directory that represents a course / module / lesson set has a
  `README.md` with frontmatter containing a `uid`.
* Add a `uid` into each notebook’s `metadata.syllabus` block if absent.
* Leave existing `uid` values untouched (so they remain stable).

Top‑level course `uid` is generated with a UUID4; others use an 8‑character
base‑62 string (letters + digits).

---

## Examples

### 1. Markdown file (`README.md` or standalone lesson `.md`)

Frontmatter (YAML) at the very top delimited by `---` lines:

```markdown
---
uid: aB93kLm2
name: Efficient Turtle Drawing
description: Introduce performance techniques for turtle graphics.
display: true   # Optional override (normally only relevant for code files)
---

# Efficient Turtle Drawing

Content starts here...
```

Notes:
* `name` here overrides both the first level‑1 heading and the filename.
* If you omit `name` but keep the heading, the heading becomes the title.
* If you omit both, the filename (sans rank / underscores) becomes the title.

### 2. Python exercise file (`050_Turtle_Tricks.py`)

Add “YAML‑ish” comment lines near the top. Pattern: `# key: value` (no quotes
required; everything after the colon is taken literally, trimmed):

```python
# uid: G7htP4Qa
# name: Turtle Tricks
# description: Small demonstrations of custom turtle functions.

import turtle as t

# rest of your code ...
```

Tips:
* Keep these at the beginning for clarity (the extractor scans the file line by line until EOF, but grouping helps reviewers).
* `display` will normally auto‑compute from imports; you can force it with `# display: false` if needed.

### 3. Jupyter notebook (`080_Variables_and_Functions.ipynb`)

Notebook metadata lives at the top level; the relevant block is:

```json
{
	"metadata": {
		"syllabus": {
			"uid": "Xy72Za9Q",
			"name": "Variables and Functions (Part 1)",
			"description": "Introduce variable assignment and simple functions."
		}
	}
	// ... remainder of notebook ...
}
```

Editing methods:
* In JupyterLab: Settings → Turn on “Show Advanced Tools” if needed, then use
  the property inspector / JSON editor to add `metadata.syllabus`.
* In VS Code: Open the notebook, click the “…” in the toolbar → “Edit Notebook
  Metadata” and insert the JSON snippet (merging with any existing metadata).
  Ensure the `syllabus` object sits inside the existing `metadata` object.

If you run `syl meta` and the notebook lacks a `uid`, one is inserted
automatically (other fields are not auto‑guessed for notebooks besides `display`
through code analysis in a paired `.py` file, so set `name` yourself for
clarity).

---
## Precedence & merging rules

1. Implicit defaults from filenames/imports are set first.
2. File‑specific metadata (Markdown frontmatter, Python comments, Notebook `metadata.syllabus`) is read and applied; only keys present override defaults.
3. For a lesson directory containing multiple files, metadata from each relevant file is merged (order: lesson markdown, then exercise code). Later values override earlier ones when keys collide.

## Common tasks

| Task | Recommended Action |
|------|--------------------|
| Add uids everywhere | `syllabus meta lessons/` |
| Force regeneration of missing uids only | Delete no files; re‑run `syllabus meta` (existing retained) |
| Change a title | Edit `name` in the relevant source (frontmatter / comments / notebook metadata) |
| Ensure stable linking | Manually set `uid` once; commit it |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Lesson shows odd title (e.g. `050 Turtle Tricks`) | No `name` provided; auto derived from filename | Add `name` in metadata or heading |
| Two lessons share same conceptual title but need distinct references | Different files but missing `uid`s | Run `syllabus meta` or add manual `uid`s |
| Notebook not picking up metadata | JSON placed at wrong level | Ensure under `metadata.syllabus` |
| `display` unexpectedly true | Auto‑detected import (e.g. accidental `import turtle`) | Remove import or set `display: false` |

---
## Minimal quick reference

Markdown frontmatter:
```markdown
---
uid: 8Xa9LmQ2
name: Lists Story
---
```

Python header comments:
```python
# uid: 9kLm23Qp
# name: List Story Exercise
```

Notebook metadata (partial top‑level JSON):
```json
"metadata": { "syllabus": { "uid": "Qp23Lm9k", "name": "List Story" } }
```

Choose and set `uid` once; tweak `name` anytime.