---
name: source-command-verify
description: "Verify research code against integrity gates and agreed success criteria."
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

## Role playbooks

Read only the role needed for the current phase.

- [verifier](references/agents/verifier.md)

# /verify — Verify Implementation

Run verification against the success criteria in the pre-report.

## Usage
```
/verify [progress log path]
```

If no path is given, use the most recent `docs/progress/*.md`.

## Behavior

Delegate to `verifier` agent with the progress log path.

Display the verification report including:
- Success criteria results (pass/fail per criterion)
- Test results
- Code quality checks
- Unplanned changes

## Post-conditions

- No code modifications.
- Suggest next steps based on results:
  - All pass → "Ready to commit. Run `/go` Phase 4 or commit manually."
  - Failures → "Issues found. Fix and re-verify, or abort."
