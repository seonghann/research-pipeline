# /impl — Implement from Pre-report

Execute the implementation plan with integrity gates and step-by-step verification.

## Usage
```
/impl [progress log path]
```

If no path is given, use the most recent `docs/progress/*.md` that has
a pre-report (sections 1-2) but no post-report (sections 3-4).

## Behavior

Delegate to `@implementer` agent. **The agent has no conversation context**,
so you MUST enrich the Task prompt with analysis conclusions and discussion insights.

**Task prompt must include:**
- Progress log path (primary reference)
- Key analysis conclusions from the analyze phase (ADOPT decisions and evidence)
- Specific design decisions made during discussion
- Known constraints or edge cases raised in conversation
- Relevant analyze script paths that validated the approach

**Example:**
```
Task("Implement: docs/progress/260208_attention_fix.md
  분석 결론: padding token의 all-zero input이 softmax에서 uniform dist를 만들고,
  이게 downstream에서 zero-division 유발 (analyze/260208_softmax_zero.py에서 확인).
  합의된 접근: attention_mask를 -inf로 채우는 방식 적용.
  주의사항: 기존 inference pipeline에서 mask format이 bool이므로 변환 필요.")
```

The implementer agent will:
1. Read pre-report for planned approach and success criteria
2. Build step queue from section 2.1
3. Execute each step with integrity gates:
   - NaN/Inf check after numerical operations
   - Shape verification after tensor operations
   - Import check after every code change
   - Test check after every code change
4. On gate failure: STOP, offer Retry/Skip/Abort/Debug
5. After all steps: assess results against success criteria
6. Report summary of changes, integrity results, and next steps

## Pre-conditions

- A pre-report MUST exist. If not, refuse and suggest `/prereport` first.
- The researcher should have approved the pre-report.

## Post-conditions

- Code changes are made but NOT committed.
- Implementation summary with:
  - Steps completed / failed / skipped
  - Files changed
  - Integrity gate results
  - Success criteria preliminary check
- Suggest running `/verify` next.

## On Failure

If implementation fails at any step:
- Implementer stops and creates diagnostic analyze script
- Options presented: Retry / Skip / Abort / Debug
- If **Debug** chosen → invoke `/debug` with failure context
- If **Abort** → preserve current state, report what was completed

## Rules

- Follow the plan. If significant deviation is needed, STOP and explain why.
- If something in the plan turns out to be wrong, create an analyze script
  to document the finding rather than silently changing approach.
- Integrity gates are non-negotiable — never skip them.
- Every step must produce observable evidence of completion.
