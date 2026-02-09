# /go — Full Research Task Cycle

Execute a complete task cycle with human checkpoints and failure recovery.

## Usage
```
/go <task description>
```

## Prerequisite

This command assumes the **discuss phase is already complete** — the user and
Claude have a shared understanding of the problem. If not, have the conversation
first. Do NOT run `/go` before discussing.

## Cycle

### Phase 1: Pre-report
Delegate to `@prereport` agent to generate the progress log pre-report.
**Agent has no conversation context** — include discuss phase summary,
agreed problem definition, success criteria, and relevant file paths in the Task prompt.

**Output**: `docs/progress/YYMMDD_<slug>.md` (sections 1-2 filled)

⏸ **CHECKPOINT**: Show the pre-report summary to the researcher.
Ask: "Pre-report ready. Review and approve? (y / n / edit)"
- **y** → proceed to Phase 2
- **n** → stop here
- **edit** → researcher provides corrections, update pre-report, re-ask

### Phase 2: Analyze (Iterative Prototyping)

Based on the approved pre-report, run iterative prototype analysis to validate
the approach BEFORE committing to implementation.

**Loop:**
1. Identify what to test/verify from the pre-report plan
2. Delegate to `@analyzer` agent (**include context**: why this question,
   related files, previous iteration conclusions):
   ```
   Task("Analyze: <question>. Context: <why, related files, previous findings>")
   ```
3. Review analyzer output: script path, conclusion, decision
4. Judge: does this answer the question?
   - **ADOPT** — approach validated, evidence supports the plan
   - **REJECT** — approach refuted, need to revise plan
   - **INVESTIGATE FURTHER** — run another analysis iteration

**If REJECT:**
- Discuss with researcher what to change
- Update pre-report plan if needed
- Re-enter analyze loop with revised hypothesis

**If INVESTIGATE FURTHER:**
- Run next analysis iteration with more specific question
- Max iterations: follow researcher guidance (suggest limit of 5)

**Exit condition:** Researcher agrees analysis is conclusive.

⏸ **CHECKPOINT**: Present analysis summary:
```
분석 결과 요약:
- Iteration 1: [question] → [conclusion] — [ADOPT/REJECT/INVESTIGATE]
- Iteration 2: ...
- 최종 결론: [approach is validated / needs revision]

분석 결과가 충분합니다. Implementation 진행할까요? (y / n / more analysis)
```
- **y** → update pre-report with analysis conclusions, proceed to Phase 3
- **n** → stop here (analysis scripts preserved as record)
- **more analysis** → continue Phase 2 loop

### Phase 3: Implementation
Delegate to `@implementer` agent with the approved pre-report.
**Agent has no conversation context** — include analysis conclusions,
design decisions from discussion, and relevant analyze script paths in the Task prompt.

```
Task("Implement: <progress log path>. 분석 결론: <key findings>. 합의 사항: <decisions>.")
```

The implementer will:
1. Execute plan step-by-step with integrity gates
2. Stop on any gate failure (NaN/Inf, shape, import, test)
3. Report per-step results with evidence

**On implementation failure:**
```
⏸ CHECKPOINT: "Implementation failed at step N. Options:"
  - retry  → fix and retry the failed step
  - debug  → invoke @debugger for systematic investigation
  - skip   → skip this step (researcher must approve)
  - abort  → stop cycle, preserve current state
```

**If debug chosen:**
```
→ Delegate to @debugger agent
→ Debugger creates repro, runs hypotheses, applies fix
→ After resolution: return to implementer, resume from failed step
```

⏸ **CHECKPOINT**: Show implementation summary (steps, gates, changes).
Ask: "Implementation complete. Review changes? (y / n / edit)"
- **y** → proceed to Phase 4
- **n** → rollback with `git checkout .`
- **edit** → researcher specifies what to change

### Phase 4: Verification
Delegate to `@verifier` agent with the progress log path.

The verifier will:
1. Run integrity gates (NaN/Inf, shape, import, gradient)
2. Run test suite
3. Check success criteria from pre-report
4. Check code quality
5. Compare plan vs reality

⏸ **CHECKPOINT**: Show verification results.
Ask: "Verification results above. Proceed to commit? (y / n / fix)"
- **y** → proceed to Phase 5
- **n** → stop, leave changes uncommitted
- **fix** → return to Phase 3 with specific issues to address

### Phase 5: Post-report & Commit
1. Update the progress log with post-report (sections 3-6):
   - Section 3.1: Iteration History (link to ALL analyze scripts from Phase 2)
   - Section 3.2: Actual actions taken
   - Section 3.3: Differences from plan
   - Section 3.4: Verification results summary
   - Section 4: Conclusion, hypothesis updates, lessons, next steps
   - Section 5: Failure section (if any steps failed and were resolved)
   - Section 6: Traceability (git, related docs, experiments)
2. Stage and commit:
   ```
   git add docs/progress/ analyze/ src/ test/
   git commit -m "[task] <slug>: <one-line summary>"
   ```

⏸ **CHECKPOINT**: Show commit summary.
"Task complete. Commit created (not pushed). Run `/compact` when ready for next task."

## Failure Recovery Flow

```
Phase 2 (analyze) finds approach is wrong
    │
    ├── revise plan → update prereport → re-analyze
    └── abandon → stop cycle, analyze scripts preserved

Phase 3 (impl) fails at step N
    │
    ├── retry → fix step, re-run integrity gates
    │     └── still fails → ask again
    │
    ├── debug → @debugger agent
    │     ├── resolved → resume impl from step N
    │     └── unresolved → CHECKPOINT: escalate to researcher
    │
    ├── skip → mark step skipped, continue (researcher approved)
    │
    └── abort → stop cycle
          └── partial progress preserved (uncommitted)
          └── analyze scripts preserved (permanent record)
```

## Rules

- NEVER skip a checkpoint. Every phase requires explicit approval.
- Phase 2 (Analyze) is NOT optional. Prototype validation before implementation.
- If any phase fails, explain what happened and offer concrete options.
- Do NOT `git push` — only commit locally.
- Keep the researcher informed of what's happening at each phase.
- Integrity gates are enforced in Phase 3 AND Phase 4 (defense in depth).
- All analyze/debug artifacts go in `analyze/` (permanent record).
