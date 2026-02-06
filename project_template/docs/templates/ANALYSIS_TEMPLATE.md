# Analysis Script Guideline

## Purpose

This template defines the structure for reproducible analysis scripts stored in `analyze/`.
These scripts document the process of identifying, diagnosing, and resolving issues where
correctness depends on non-obvious behavior — whether from external libraries, numerical
computation, framework semantics, or internal project logic.

## When to Write an Analysis Script

- Unexpected or ambiguous behavior from any library or framework
- Numerical stability or precision concerns
- Implicit assumptions in existing code that need verification
- Any situation where the correct fix is not self-evident and depends on empirical observation

## File Naming Convention

```
analyze/<YYMMDD>_<short_description>.py
```

Examples:
- `analyze/260130_rdkit_brics_bond_order.py`
- `analyze/260201_egnn_gradient_stability.py`
- `analyze/260203_pyg_heterodata_edge_index.py`

## Required Structure

Every analysis script should contain the following sections, using inline comments or
docstrings:

```python
"""
Analysis: <title>
Date: YYYY-MM-DD
Related progress log: docs/progress/YYMMDD.md (if applicable)

Problem:
    <What unexpected behavior or question prompted this analysis?>

Conclusion:
    <Fill in AFTER running the analysis. Summarize the finding and its
     implication for the implementation.>
"""

# --- Setup ---
# Imports and minimal input data needed to reproduce the issue.
# If real data is required, provide clear instructions on how to obtain it.

# --- Observation ---
# Code that demonstrates the behavior in question.
# Print/log outputs that make the key observations visible without a debugger.

# --- Diagnosis ---
# Isolate the root cause. Vary inputs, check edge cases, compare with
# documentation or source code behavior.

# --- Verification ---
# Confirm the proposed fix or workaround resolves the issue.
# Show before/after if applicable.
```

## Principles

1. **Self-contained**: The script must run independently (`python analyze/<script>.py`)
   without requiring the full training pipeline or special environment setup beyond the
   project's standard dependencies.
2. **Observable**: All key findings must be printed to stdout/stderr. Do not rely on
   breakpoints or variable inspection.
3. **Minimal**: Include only the code necessary to demonstrate the issue. Avoid pulling in
   unrelated modules.
4. **Conclusive**: The docstring `Conclusion` field must be filled in after the analysis.
   An analysis without a stated conclusion is incomplete.
