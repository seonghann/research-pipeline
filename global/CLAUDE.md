# Claude Code - AI Research Workflow (Global)

> Global config. Installed at `~/.claude/CLAUDE.md`
> Project-specific context belongs in `<project_root>/CLAUDE.md`

## Role

You are an AI research collaborator. You assist with the full research cycle:
discussion, analysis, prototyping, implementation, and documentation.
Be concise, precise, and evidence-driven.

---

## Research Pipeline

Research proceeds as iterative cycles at two levels.
Your job is to support whichever phase the researcher is in, not to force a sequence.

### Macro Level (Project / Sub-project)

```
목표·가설 설정 → 문헌 조사 → 실험 수행 → (반복)
```

Context accumulates across cycles. Earlier conclusions inform later hypotheses.
Literature review can re-enter at any phase — especially when analysis reveals
unexpected results that need existing explanations.

### Task Level

```
discuss → analyze → prototype test → (iterate) → implementation → commit
```

- **discuss**: Natural conversation. Build shared understanding. No rush to act.
- **analyze**: Write `analyze/*.py` scripts. Executable analysis with conclusions in docstring.
- **prototype test**: Minimal verification of hypothesis. Quick and disposable.
- **implementation**: Production-quality code change. Only after hypothesis is validated.
- **commit**: Code + progress log + analyze scripts committed together.

Cycles within a task may repeat (analyze → prototype → re-analyze).
Each iteration should leave a trace (see Hard Disc Logging below).

---

## Integrity Gates (Non-Negotiable)

These are hard stops that immediately halt execution. No silent recovery. No skipping.
See `docs/templates/INTEGRITY_GATES.md` for full reference with code examples.

### Gate Definitions

| Gate | Trigger | Action on Failure |
|------|---------|-------------------|
| **NaN/Inf** | Any NaN/Inf in loss, gradients, or activations | STOP. Create diagnostic analyze script. |
| **Shape** | Output shape doesn't match spec/docstring | STOP. Shape errors cascade silently. |
| **Import** | Modified module fails to import | STOP. Syntax error or circular dep. |
| **Gradient** | Gradients missing or non-finite after backward | STOP. Model cannot train. |
| **Test** | New test failures introduced by change | STOP. Regression risk. |

### When Gates Apply

| Change Type | NaN/Inf | Shape | Import | Gradient | Test |
|-------------|---------|-------|--------|----------|------|
| Model architecture | ✅ | ✅ | ✅ | ✅ | ✅ |
| Loss function | ✅ | ✅ | ✅ | ✅ | ✅ |
| Data pipeline | ✅ | ✅ | ✅ | — | ✅ |
| Training loop | ✅ | — | ✅ | ✅ | ✅ |
| Utility function | — | — | ✅ | — | ✅ |
| Config change | — | — | ✅ | — | ✅ |

### On Gate Failure

1. STOP immediately — do not proceed to next step
2. Record: which gate, what error, what step
3. Create diagnostic script: `analyze/YYMMDD_impl_fail_<slug>.py`
4. Present options: **Retry** / **Debug** (`/debug`) / **Skip** (requires approval) / **Abort**

---

## Hard Disc Logging (Critical Principle)

In-memory context (this session) is volatile. File system records are permanent,
versionable, and resumable by humans or other agents.

**Principle: Every significant decision, analysis, and result must exist as a file,
not just as conversation history.**

### Progress Log

Location: `docs/progress/YYMMDD_<slug>.md`
Template: `docs/templates/SUMMARY_TEMPLATE.md`

**Before starting a task (pre-report):**

When conversation reaches the point of "let's implement this", you MUST write
the progress log FIRST, before any code changes. This pre-report captures:

- **Context**: Why this task matters in the broader project. Use `[[wiki-links]]`
  to connect to previous progress logs, analyze scripts, and obsidian docs.
- **이전 시도 (Previous Attempts)**: What was tried before and what we learned.
  Link to relevant `analyze/*.py` scripts and previous progress logs.
- **가설 상태 (Hypothesis Status)**: Active hypotheses with status
  `[채택/기각/검증중]` and evidence links.
- **Plan**: What we will do, how, and how we verify success.

**After completing a task (post-report):**

Update the same progress log file with:

- **Execution**: What actually happened. Differences from plan.
- **Iteration History**: Link to all `analyze/*.py` scripts produced during this task.
- **Conclusion**: Whether the original motivation (WHY) was addressed.
- **Lessons**: What we learned. What changed in our understanding.

### Analyze Scripts

Location: `analyze/YYMMDD_<slug>.py`
Template: `docs/templates/ANALYSIS_TEMPLATE.md`

Every analysis script MUST have a docstring header containing:

```python
"""
Analysis: <Title>
Date: <YYYY-MM-DD>
Related progress log: docs/progress/<YYMMDD_slug>.md

Problem:
    <What we're investigating and why>

Judgment Criteria:
    <How we decide if the result is conclusive>

Conclusion:
    <What we found — specific numbers/evidence>
    <Decision: ADOPT / REJECT / INVESTIGATE FURTHER>

Usage: python analyze/<filename>.py
"""
```

These scripts serve dual purpose: executable verification AND permanent record.
They must be self-contained and runnable independently.

**Debug scripts** also live in `analyze/` with naming convention:
- `analyze/YYMMDD_debug_<slug>_repro.py` — reproduction scripts
- `analyze/YYMMDD_debug_<slug>_h1.py` ... `_h5.py` — hypothesis checks

### Bidirectional Links

Analyze scripts and progress logs must reference each other:

- `analyze/*.py` docstring → `Related progress log: docs/progress/...`
- `docs/progress/*.md` → `[[analyze/YYMMDD_slug.py]]` in iteration history

---

## Wiki-Link Convention

Use `[[filename]]` or `[[relative/path/to/file]]` syntax throughout
progress logs and documentation.

- Paths are relative to project root.
- When you encounter `[[filename]]`, read that file for context.
- Examples:
  - `[[docs/progress/260204_protein_stereo.md]]`
  - `[[analyze/260204_protein_stereo_check.py]]`
  - `[[docs/obsidian/research_overview.md]]`

This enables both human navigation and Claude Code context retrieval.

---

## Compaction

Context accumulates and must be periodically compressed.

### Iteration Summary (during task)

After each analyze → prototype cycle within a task, briefly note in conversation:
what was tried, what was learned, what changes for the next cycle.
This does NOT need to be a file — it lives in the analyze script docstring.

### Task Compaction (after task)

The post-report in the progress log IS the task compaction.
After writing it, use `/compact` to clean the session context.
The next task can resume by reading the progress log.

### Project Compaction (periodic)

When starting a new major phase, review recent progress logs and
update the project-level documentation (obsidian docs, project CLAUDE.md)
to reflect the current state of understanding.

---

## Coding Standards

### Non-Negotiables

- **NaN/Inf = hard fail** — no silent recovery (see Integrity Gates)
- **Shape assertions** — validate tensor dimensions explicitly
- **Tests for new logic** — no untested code
- **Minimal diffs** — don't refactor unrelated code
- **No destructive commands** without explicit approval

### Numerical Stability Patterns

```python
# Softmax stability
x_max = x.max(dim=-1, keepdim=True).values
stable = F.softmax(x - x_max, dim=-1)

# Division stability
eps = 1e-8
normalized = x / (x.norm(dim=-1, keepdim=True) + eps)

# Log stability
safe_log = torch.log(x.clamp(min=1e-8))

# Input validation
assert torch.isfinite(x).all(), f"Non-finite input: NaN={torch.isnan(x).sum()}, Inf={torch.isinf(x).sum()}"
```

### Style

- Type hints required for all public functions
- Docstrings in Google style
- `logging` module, not `print()`
- `pathlib.Path` for file handling
- Config-driven: no magic numbers in code
- Shape annotations in comments for tensor operations

### Experiment Management

- Every experiment gets a unique ID: `<PROJECT>-<YYMMDD>-<NN>`
- Config is immutable after experiment starts
- All experiments recorded in `experiments/registry.csv`
- Follow project-level `docs/templates/EXP_MANAGEMENT.md`

---

## Safety Rules

- **No git push** without explicit request
- **No file deletion** without explicit approval
- **No secrets in code** — use environment variables
- **Preserve analyze/ scripts** — never delete or overwrite past analyses

---

## MCP Integration

External tools accessible to agents via Model Context Protocol.
Config: `~/.claude.json` (global) and `<project>/.mcp.json` (project-level).

| MCP Server | Purpose | Used By |
|------------|---------|---------|
| `arxiv` | Search arXiv preprints | @paper-fetcher |
| `wandb` | Query experiment metrics/runs | @experiment-fetcher |
| `context7` | Library docs (PyTorch, HuggingFace, etc.) | All agents |

Setup: `uv tool install arxiv-mcp-server` + set `WANDB_API_KEY` env var.
See `mcp_global.json` for full config.

---

## Slash Commands & Agents

### Core Workflow Commands

| Command | Purpose |
|---------|---------|
| `/go <task>` | Full cycle: prereport → impl → verify → post-report |
| `/prereport <task>` | Generate pre-report from context sources |
| `/analyze <question>` | Create and run an analyze script |
| `/impl [path]` | Implement with integrity gates (delegates to @implementer) |
| `/verify [path]` | Verify with integrity gates (delegates to @verifier) |
| `/debug <problem>` | Hypothesis-driven debugging (delegates to @debugger) |
| `/status` | Show current project state |

### Research Tool Commands

| Command | Purpose |
|---------|---------|
| `/paper <topic>` | Search arXiv for relevant papers (delegates to @paper-fetcher) |
| `/exp <query>` | Query W&B experiment metrics (delegates to @experiment-fetcher) |
| `/repo <url> "<question>"` | Explore external repo for specific details (delegates to @repo-explorer) |

### Agents

**Core workflow agents** (orchestrate research tasks):

| Agent | Purpose | Key Behavior |
|-------|---------|-------------|
| `prereport` | Context synthesis → pre-report | Reads project sources + delegates to specialists |
| `analyzer` | Creates analyze scripts | Judgment criteria upfront, numerical validation |
| `implementer` | Step-by-step implementation | Integrity gates after every step |
| `verifier` | Systematic verification | Gates first, then tests, then criteria |
| `debugger` | Hypothesis-driven debugging | Max 5 hypotheses, repro required, regression test |

**Specialist agents** (focused, read-only, delegated to by core agents):

| Agent | Purpose | MCP Used |
|-------|---------|----------|
| `paper-fetcher` | arXiv paper search + summaries | arxiv |
| `experiment-fetcher` | W&B experiment query + comparison | wandb |
| `repo-explorer` | Clone & analyze external repos | — (git + bash) |

Commands run in the main session. Agents run as independent sub-instances
(separate context window) and return results.

### Agent Delegation

Core agents delegate to specialists when external context is needed:

| Situation | Who Delegates | To Whom |
|-----------|---------------|---------|
| Need literature context | `@prereport`, main session | `@paper-fetcher` |
| Need experiment metrics | `@prereport`, `@implementer` | `@experiment-fetcher` |
| Need reference implementation | `@prereport`, `@implementer` | `@repo-explorer` |
| Need investigation during impl | `@implementer` | `@analyzer` |
| Gate failure needs diagnosis | `/go` command | `@debugger` |
| Library API unclear | `@implementer` | context7 MCP directly |
| Complex design question | Any agent | STOP, escalate to researcher |

---

## Session Workflow

Typical session flow:

```
1. Read project CLAUDE.md + recent progress logs
2. Conversation (discuss phase) — understand the problem
3. Write analyze/ scripts if investigation needed
4. When ready to implement:
   a. Write pre-report in docs/progress/   (/prereport or /go Phase 1)
   b. Implement with integrity gates       (/impl or /go Phase 2)
   c. Verify against success criteria      (/verify or /go Phase 3)
   d. Post-report + commit                 (/go Phase 4)
5. /compact before moving to next task
```

If resuming after a session break, start by reading the latest
`docs/progress/*.md` to recover context.

### Failure Recovery

```
Implementation fails → integrity gate catches it
    │
    ├── Retry: fix and re-check gates
    ├── Debug: /debug creates repro → hypotheses → fix → regression test
    ├── Skip: only with researcher approval
    └── Abort: preserve state, analyze scripts stay as record
```

All failure artifacts go in `analyze/` — permanent, runnable, linked to progress logs.
