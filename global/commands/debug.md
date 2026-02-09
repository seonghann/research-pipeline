# /debug — Hypothesis-Driven Debugging

Systematically investigate and resolve a bug or failure.

## Usage
```
/debug <problem description>
```

## Behavior

Delegate to `@debugger` agent. **The agent has no conversation context**,
so you MUST enrich the Task prompt with everything needed to reproduce and investigate.

**Task prompt must include:**
- Problem description (what's wrong, when it happens)
- Error messages or stack traces from conversation
- What was being done when the problem occurred (impl step, test run, etc.)
- Related file paths and line numbers discussed
- What has already been tried or ruled out in conversation

**Example:**
```
Task("Debug: training 3 epoch 후 loss가 NaN으로 발산.
  Error: RuntimeError at src/model/loss.py:42 — log(0) 발생.
  상황: /impl 중 Phase 3 step 2에서 발견.
  관련 파일: src/model/loss.py (contrastive_loss 함수),
            src/data/sampler.py (negative sampling).
  이미 확인: learning rate는 정상 (1e-4), gradient clipping 적용됨.
  의심: negative sample이 positive와 동일할 때 distance=0 케이스.")
```

The debugger agent will:
1. Collect evidence (error messages, suspected location, recent changes)
2. Create minimal repro script in `analyze/` (REQUIRED before any fix)
3. Run hypothesis loop (max 5 iterations):
   - Write hypothesis check script in `analyze/`
   - Execute and record outcome: confirmed / refuted / inconclusive
4. If root cause confirmed:
   - Apply minimal fix
   - Add regression test in `test/`
   - Verify: repro passes, regression test passes, existing tests pass
5. Document everything in analyze scripts (permanent record)

## When to Use

- After `/impl` fails at an integrity gate
- After `/verify` returns FAIL verdict
- When unexpected behavior is observed during discuss/analyze phase
- When existing tests start failing

## Output

All artifacts in `analyze/`:
- `analyze/YYMMDD_debug_<slug>_repro.py` — minimal reproduction
- `analyze/YYMMDD_debug_<slug>_h1.py` ... `_h5.py` — hypothesis checks
- Regression test in `test/test_regression_<slug>.py`

Report includes:
- Root cause (if found)
- Fix applied (if resolved)
- Evidence trail (hypothesis ledger)
- Verdict: RESOLVED / UNRESOLVED

## On Unresolved (after 5 hypotheses)

- All hypothesis results documented
- Most likely remaining causes listed
- Specific questions for researcher (max 3)
- All artifacts preserved for future investigation

## Rules

- Reproduce first, fix second — no fix without working repro
- Max 5 hypotheses — if not enough, escalate to researcher
- Minimal fix only — no refactoring, no scope creep
- Regression test mandatory for every fix
- All scripts go in `analyze/` — permanent record
