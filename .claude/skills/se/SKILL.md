---
description: CLASI Software Engineering process dispatcher
---

# /se

Dispatch to the CLASI SE process. Parse the argument after `/se` and
call the matching MCP tool from the table below.

If `/se` is called with **no arguments**, display this help listing
to the user and stop — do not execute any skill.

## Available commands

| Command | Description | MCP call |
|---------|-------------|----------|
| `/se status` | Show project status — sprints, tickets, next actions | `get_skill_definition("project-status")` |
| `/se next` | Determine and execute the next process step | `get_skill_definition("next")` |
| `/se todo <text>` | Create a TODO file from the description | `get_skill_definition("todo")` |
| `/se init` | Start a new project with a guided interview | `get_skill_definition("project-initiation")` |
| `/se report` | Report a bug with the CLASI tools | `get_skill_definition("report")` |
| `/se ghtodo <text>` | Create a GitHub issue from the description | `get_skill_definition("ghtodo")` |

Pass any remaining text after the subcommand as the argument to the
skill (e.g., `/se todo fix the login bug` passes "fix the login bug"
to the todo skill).

For general SE process guidance, call `get_se_overview()`.
