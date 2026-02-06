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

**Delegate to `@experiment-fetcher` agent:**

```
Task("Experiments: <query>")
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
