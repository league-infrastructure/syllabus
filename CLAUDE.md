<!-- CLASI:START -->
## CLASI Software Engineering Process

**MANDATORY: Before doing ANY work that involves code or planning on
code, you MUST call `get_se_overview()` to load the software engineering
process. Do this at the start of every conversation. No exceptions.**

This project uses the **CLASI** (Claude Agent Skills Instructions)
software engineering process, managed via an MCP server.

**The SE process is the default.** Any activity that results in changes
to the codebase — or plans to change the codebase — falls under this
process. Follow it unless the stakeholder explicitly says "out of
process" or "direct change".

Activities that trigger the SE process include:

- Building a new feature or adding functionality
- Fixing a bug or resolving an issue
- Refactoring, restructuring, or reorganizing code
- Writing, updating, or removing tests
- Updating documentation that describes code behavior
- Planning, scoping, or designing an implementation
- Reviewing code or architecture
- Creating, modifying, or closing sprints and tickets
- Merging, branching, or tagging releases

**If it touches code, tests, docs about code, or plans for code — STOP.
Call `get_se_overview()` if you haven't already. Then either follow the
process it describes, or confirm the stakeholder has explicitly said
"out of process" or "direct change" before proceeding without a sprint.**

### MANDATORY: Pre-Flight Check

**Before writing ANY code, you MUST confirm one of:**

1. You have an active sprint and ticket — check with `list_sprints()`
   and `list_tickets()`. If you do, execute that ticket.
2. The stakeholder has explicitly said "out of process", "direct change",
   or invoked `/oop`. If so, proceed without a sprint.

**If neither is true, do NOT write code.** Instead, enter the SE process:
use `get_skill_definition("plan-sprint")` to create a sprint, or
`get_skill_definition("next")` to determine the correct next step.

### MANDATORY: CLASI Skills First

**Before using any generic tool for a process activity, check
`list_skills()` for a CLASI-specific skill.** CLASI skills always take
priority over generic tools for process activities.

Examples of what this means:
- Creating a TODO → use the CLASI `todo` skill, not the `TodoWrite` tool
- Finishing a sprint → use `close-sprint` skill, not generic branch tools
- Creating tickets → use `create-tickets` skill, not ad-hoc file creation

### MANDATORY: Stop and Report on Failure

**When a required MCP tool or process step is unavailable or fails, STOP
and report the failure to the stakeholder.** Do not:

- Create substitute artifacts that bypass the process
- Improvise workarounds outside the established workflow
- Silently continue without the required tool

The correct response is: "Tool X is unavailable. I cannot proceed without
it. Let's fix the MCP connection first."

### Process

Work happens at two levels: **project initiation** and **sprints**.

**Project initiation** (once per project):

1. Interview the stakeholder to understand the project goals and scope.
   → `get_skill_definition("project-initiation")`
2. Generate project initiation documents (overview, spec, use cases).
   → `get_skill_definition("elicit-requirements")`
3. Break the project into sprints — either all at once if the spec is
   complete, or incrementally (one or two sprints at a time) so the
   stakeholder can adjust later sprints as the project evolves.
   → `get_skill_definition("plan-sprint")`

**Sprint lifecycle** (repeated per sprint):

1. **Mine TODOs** — Scan `docs/plans/todo/` with `list_todos()` for
   ideas relevant to the sprint. Discuss with the stakeholder.
2. **Create sprint** — `create_sprint(title)` sets up the directory and
   registers the sprint. Create the branch: `git checkout -b sprint/NNN-slug`.
3. **Write planning docs** — Fill in `sprint.md`, `usecases.md`, and
   update `architecture.md` in the sprint directory with real content.
   The architecture doc is copied from the previous sprint — update it
   to reflect the target end-of-sprint state and fill in Sprint Changes.
4. **Architecture review** — `advance_sprint_phase(sprint_id)` to move
   to architecture-review. Delegate to the architecture-reviewer agent.
   Record the result: `record_gate_result(sprint_id, "architecture_review", "passed")`.
5. **Stakeholder review** — Present the plan to the stakeholder.
   `record_gate_result(sprint_id, "stakeholder_approval", "passed")`.
6. **Create tickets** — `advance_sprint_phase(sprint_id)` to ticketing.
   Use `create_ticket(sprint_id, title)` for each ticket. Fill in details.
7. **Execute tickets** — `advance_sprint_phase(sprint_id)` to executing.
   `acquire_execution_lock(sprint_id)`. Execute each ticket via
   `get_skill_definition("execute-ticket")`.
8. **Close sprint** — After all tickets are done, use
   `get_skill_definition("close-sprint")` to merge, archive, and tag.

Use `/se` or call `get_se_overview()` for full process details and MCP
tool reference.

### MANDATORY: Ticket and Sprint Completion

**Agents MUST complete these steps. No exceptions. No skipping.**

Agents have repeatedly failed to move tickets to done and close sprint
branches. This creates inconsistent state. These rules are non-negotiable.

**After finishing a ticket's code changes, you MUST:**

1. Run the full test suite and confirm all tests pass.
2. Set ticket `status` to `done` in YAML frontmatter.
3. Check off all acceptance criteria (`- [x]`).
4. Move the ticket file to `tickets/done/` — use `move_ticket_to_done`.
5. Move the ticket plan file to `tickets/done/` if it exists.
6. Commit the moves: `chore: move ticket #NNN to done`.

**Finishing the code is NOT finishing the ticket.** The ticket is not done
until the file is in `tickets/done/` and committed.

**After finishing all tickets in a sprint, you MUST close the sprint:**

1. Merge the sprint branch into main.
2. Call `close_sprint` MCP tool (archives directory, releases lock).
3. Commit the archive.
4. Push tags (`git push --tags`).
5. Delete the sprint branch (`git branch -d sprint/NNN-slug`).

**Never merge a sprint branch without archiving the sprint directory.**
**Never leave a sprint branch dangling after the sprint is closed.**

### Stakeholder Corrections

When the stakeholder corrects your behavior or expresses frustration
("that's wrong", "why did you do X?", "I told you to..."):

1. Acknowledge the correction immediately.
2. Run `get_skill_definition("self-reflect")` to produce a structured
   reflection in `docs/plans/reflections/`.
3. Continue with the corrected approach.

Do NOT trigger on simple clarifications, new instructions, or questions
about your reasoning.
<!-- CLASI:END -->
