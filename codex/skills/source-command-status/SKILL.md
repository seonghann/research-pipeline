---
name: source-command-status
description: "Summarize the research project state from progress logs and evidence; not Codex usage status."
---

## Codex execution conventions

Use the available native subagent tools for delegation. Role names below identify
custom agents installed in `~/.codex/agents/` (or `$CODEX_HOME/agents/`). Pass the
role's instructions, research context, file paths, previous results and constraints.
`Delegation brief(...)` examples are explanatory prompt text, not a tool or command.
If this client cannot select a custom role, load the matching playbook from
`references/agents/` in this skill and pass it to an available subagent. If delegation
is unavailable, perform the role inline and disclose that fallback. Keep role scope
and checkpoints. Do not claim a subagent ran when it did not. Independent subtasks
may run concurrently; dependent phases remain sequential. Inherit the user's model.
Read/Write/Edit/Bash/Grep/Glob are capability descriptions: use the actual available
file, shell and search tools. Never invoke a nonexistent Codex tool.

Use `$source-command-NAME` for these skills. Legacy `/NAME` labels below describe
the research workflow, not registered CLI slash commands. `/status` in Codex is a
built-in usage command; use `$source-command-status` for research status.
Honor existing user authorization; do not request the same approval again.
Do not undo work or delete files on a rejected checkpoint. Preserve and report state.
Stage only explicit task-owned paths. Push only when the user explicitly requests it.

# /status — Project Status Overview

Show the current state of the project: recent progress, active hypotheses,
and pending tasks.

## Usage
```
/status
```

## Behavior

1. **Recent Progress** — Read last 3 `docs/progress/*.md` files (sorted by date).
   For each, show: date, title, status (pre-report only / completed / failed).

2. **Active Hypotheses** — Scan recent progress logs for hypothesis status markers
   (`[채택]`, `[기각]`, `[검증중]`). List currently active ones.

3. **Recent Analyses** — List last 5 `analyze/*.py` files with their one-line
   conclusion from the docstring.

4. **Git Status** — Show `git status --short` and last 3 commits.

5. **Pending Work** — Check if any progress log has pre-report but no post-report
   (incomplete task).

## Output Format

```
## Project Status: <project name from AGENTS.md>

### Recent Progress
| Date | Task | Status |
|------|------|--------|
| ... | ... | ... |

### Active Hypotheses
- [검증중] ...
- [채택] ...

### Recent Analyses
- analyze/YYMMDD_slug.py → (conclusion)

### Pending
- docs/progress/YYMMDD_slug.md — pre-report only, not implemented

### Git
- Branch: ...
- Last commit: ...
- Uncommitted changes: Y/N
```

## Notes

- This command is read-only. It modifies nothing.
- Useful at the start of a session to recover context.
- Useful when managing multiple projects to quickly see where each one stands.
