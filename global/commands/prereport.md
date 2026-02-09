# /prereport — Generate Pre-report

Formalize a discussed problem into a structured pre-report.

## Usage
```
/prereport <task description>
```

## Prerequisite

This command should come AFTER the discuss phase — the user and Claude have
a shared understanding of the problem, approach, and success criteria.

If the conversation hasn't reached this point yet, say:
"아직 논의가 충분하지 않은 것 같습니다. [구체적으로 무엇이 불명확한지] 먼저 정리할까요?"

## Behavior

Delegate to `@prereport` agent. **The agent has no conversation context**,
so you MUST enrich the Task prompt with a summary of the discuss phase.

**Task prompt must include:**
- Task description (what to implement/investigate)
- Discussion summary: problem definition agreed upon, why it matters
- Relevant file paths discussed (src/, analyze/, obsidian notes)
- Hypotheses considered and their status (채택/기각/검증중)
- Success criteria discussed
- Any constraints or concerns raised during discussion

**Example:**
```
Task("Generate pre-report: attention layer의 NaN 문제 해결.
  논의 요약: training 3 epoch 후 loss NaN 발생. padding token의
  all-zero input → softmax uniform → downstream zero-division이 원인으로 의심.
  관련 파일: src/model/attention.py, analyze/260208_softmax_zero.py.
  접근 방향: attention mask를 -inf로 적용하는 방식.
  성공 기준: 10 epoch 학습 완료 without NaN, 기존 test 통과.
  주의: inference pipeline의 mask format 호환성 확인 필요.")
```

The agent will:
1. Read `docs/obsidian/` for research-level context
2. Read recent `docs/progress/*.md` (last 3-5)
3. Read relevant `analyze/*.py` scripts
4. Scan affected `src/` modules
5. Combine file-based context with the discussion summary from the prompt
6. Write pre-report to `docs/progress/YYMMDD_<slug>.md`

After the agent finishes, display the pre-report summary and ask for approval.

## After Approval

Once the researcher approves the pre-report, the natural next step is
**analyze phase** — write prototype scripts to validate the approach.

Suggest: "Pre-report 승인 완료. Analyze phase로 진행할까요? 먼저 검증할 항목: [list from plan]"

## Notes

- This is the standalone version of Phase 1 in `/go`.
- Use this when discuss has concluded and you want to formalize the plan.
- The pre-report is NOT the implementation. No code changes should happen.
- After prereport, the user may proceed with `/analyze` commands individually
  or use `/go` to run the remaining phases automatically.
