# /analyze — Create and Run Analysis Script

Investigate a specific question by creating a self-contained analysis script.

## Usage
```
/analyze <question or hypothesis to test>
```

## Context

This command is used in two situations:

1. **During discuss phase** — to empirically verify a question before committing
   to a direction. "Is this actually true? Let's check."
2. **During analyze phase** — as part of the iterative prototyping loop after
   prereport. Each `/analyze` call is one iteration of the loop.

## Behavior

Delegate to `@analyzer` agent. **The agent has no conversation context**,
so you MUST enrich the Task prompt with relevant information from the discussion.

**Task prompt must include:**
- The question/hypothesis to test
- WHY this question matters (context from discussion)
- Related file paths mentioned in conversation (src/, analyze/, progress logs)
- Previous analysis conclusions relevant to this question
- Specific edge cases or constraints discussed

**Example:**
```
Task("Analyze: softmax output이 0이 되는 케이스 있는지.
  Context: attention layer에서 NaN 발생 의심 중.
  관련 파일: src/model/attention.py (scaled_dot_product 함수).
  이전 분석: analyze/260205_nan_check.py — gradient는 정상.
  주의: padding token이 all-zero인 경우 확인 필요.")
```

The agent will:
1. Understand what needs to be verified
2. Read relevant source code
3. Write `analyze/YYMMDD_<slug>.py` following ANALYSIS_TEMPLATE
4. Run the script
5. Fill in the Conclusion based on results

After the agent finishes, display:
- Script path
- Key findings (1-3 sentences)
- Decision: **ADOPT** / **REJECT** / **INVESTIGATE FURTHER**

## After Each Analysis

Based on the decision, suggest next action:

- **ADOPT**: "접근법이 검증되었습니다. Implementation으로 넘어갈까요, 추가 분석이 필요할까요?"
- **REJECT**: "가설이 기각되었습니다. [구체적 이유]. 대안: [suggest alternatives based on findings]"
- **INVESTIGATE FURTHER**: "추가 확인이 필요합니다: [what's still unknown]. 다음 분석을 실행할까요?"

## Notes

- The script modifies nothing — it only reads and reports.
- Each `/analyze` produces a permanent record in `analyze/`.
- Multiple `/analyze` calls form the iterative analysis loop.
- When the loop concludes, update the pre-report with analysis conclusions
  before moving to implementation.
