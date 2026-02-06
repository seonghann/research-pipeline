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
## Project Status: <project name from CLAUDE.md>

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
