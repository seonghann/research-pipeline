---
name: source-command-repo
description: "Inspect an external repository for a specific research implementation question."
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

- [repo-explorer](references/agents/repo-explorer.md)

# /repo — Explore External Repository

Clone and analyze an external repository to extract specific implementation details.

## Usage
```
/repo <github URL> "<what to find>"
```

## Examples
```
/repo https://github.com/user/diffusion-model "how is the denoising score matching loss implemented?"
/repo https://github.com/user/equivariant-gnn "encoder architecture and attention mechanism"
/repo https://github.com/user/fragment-vae "training loop and sampling procedure"
```

## Behavior

**Delegate to `repo-explorer` agent:**

```
Delegation brief("Explore repo: <url> — <what to find>")
```

The repo-explorer will:
1. Shallow-clone the repo to `/tmp/`
2. Scan structure, find relevant code
3. Extract and summarize the specific information requested
4. Clean up (remove clone)

## When to Use

- Found a paper's reference implementation and want to understand specifics
- Colleague shared a repo and you need to understand their approach
- Want to compare your implementation with an existing one
- Need to understand a library's internal behavior

## Output

Structured analysis (under 1000 tokens) with:
- Repo structure overview
- Answer to the specific question with `<file:line>` references
- Relevant code snippets (max 30 lines)
- How it relates to your project
- Caveats (license, deps, assumptions)

## Rules

- Cloned to `/tmp/` only — never into your project
- Read-only — no code is copied into your project
- If you want to adopt a pattern, implement it yourself based on the understanding
- Check the license before using any ideas
