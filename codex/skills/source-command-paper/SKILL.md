---
name: source-command-paper
description: "Search arXiv literature for a research topic using the configured arXiv MCP."
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

- [paper-fetcher](references/agents/paper-fetcher.md)

# /paper — Search Research Papers

Search arXiv for papers relevant to current research.

## Usage
```
/paper <topic, method, or specific question>
```

## Examples
```
/paper "diffusion models for 3D molecular generation"
/paper "equivariant neural networks for protein structure"
/paper "fragment-based drug design with deep learning, last 2 years"
```

## Behavior

**Delegate to `paper-fetcher` agent:**

```
Delegation brief("Papers: <query>")
```

The paper-fetcher will:
1. Search arXiv via MCP
2. Filter and rank top 3-5 relevant papers
3. Return structured summaries with key ideas, methods, results

## When to Use

- During **discuss** phase — "what's the state of the art in X?"
- During **analyze** phase — "is there existing work on this approach?"
- When reviewer/colleague mentions a method you're unfamiliar with
- When exploring a new research direction

## Output

Structured paper summaries (under 800 tokens) with:
- Title, authors, arXiv ID
- Key idea and method summary
- Relevance to your question
- Suggested follow-up searches

## Notes

- Requires `arxiv` MCP server configured in `~/.codex/config.toml`
- Only searches arXiv — not Google Scholar, Semantic Scholar, etc.
- Does NOT download full papers — summaries only
- For deep reading, use the arXiv ID to find the full paper yourself
