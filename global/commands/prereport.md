# /prereport — Generate Pre-report

Generate a structured pre-report for a task by synthesizing project context.

## Usage
```
/prereport <task description>
```

## Behavior

Delegate to `@prereport` agent with the task description.

The agent will:
1. Read `docs/obsidian/` for research-level context
2. Read recent `docs/progress/*.md` (last 3-5)
3. Read relevant `analyze/*.py` scripts
4. Scan affected `src/` modules
5. Write pre-report to `docs/progress/YYMMDD_<slug>.md`

After the agent finishes, display the pre-report summary and ask for approval.

## Notes

- This is the standalone version of Phase 1 in `/go`.
- Use this when you want to prepare a pre-report before a discuss session,
  or when discuss has concluded and you want to formalize the plan before
  starting implementation separately.
- The pre-report is NOT the implementation. No code changes should happen.
