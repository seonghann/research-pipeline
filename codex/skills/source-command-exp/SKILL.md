---
name: source-command-exp
description: "Read and compare experiment metrics using the configured W&B MCP."
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

- [experiment-fetcher](references/agents/experiment-fetcher.md)

# /exp — Query Experiment Metrics

Query W&B for experiment results, comparisons, and diagnostics.

## Usage
```
/exp <question about experiments>
```

## Examples
```
/exp "best val_loss across FRAG3D-260201 runs"
/exp "compare learning rates in recent training runs"
/exp "show failed runs from this week"
/exp "what config did the best performing run use?"
```

## Behavior

**Delegate to `experiment-fetcher` agent:**

```
Delegation brief("Experiments: <query>")
```

The experiment-fetcher will:
1. Query W&B via MCP for matching runs
2. Fetch relevant metrics and configs
3. Return structured comparison with best run, trends, anomalies

## When to Use

- During **analyze** phase — "are my experiments actually improving?"
- During **discuss** phase — "what hyperparams worked best so far?"
- After training — "did anything NaN out or crash?"
- Before planning next experiment — "what hasn't been tried yet?"

## Output

Structured experiment summary (under 600 tokens) with:
- Best run with config
- Top 5 comparison table
- Patterns and anomalies
- Failed runs (if any)
- Suggested next experiments

## Notes

- Requires `wandb` MCP server configured
- Set `WANDB_API_KEY` in environment
- Project-level `.mcp.json` should have `WANDB_ENTITY` and `WANDB_PROJECT`
- Read-only — never starts or modifies experiments
