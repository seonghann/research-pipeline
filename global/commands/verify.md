# /verify — Verify Implementation

Run verification against the success criteria in the pre-report.

## Usage
```
/verify [progress log path]
```

If no path is given, use the most recent `docs/progress/*.md`.

## Behavior

Delegate to `@verifier` agent with the progress log path.

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
