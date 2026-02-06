# /analyze — Create and Run Analysis Script

Investigate a specific question by creating a self-contained analysis script.

## Usage
```
/analyze <question or hypothesis to test>
```

## Behavior

Delegate to `@analyzer` agent with the question.

The agent will:
1. Understand what needs to be verified
2. Read relevant source code
3. Write `analyze/YYMMDD_<slug>.py` following ANALYSIS_TEMPLATE
4. Run the script
5. Fill in the Conclusion based on results

After the agent finishes, display:
- Script path
- Key findings (1-3 sentences)
- Recommended decision

## Notes

- This is the standalone version of ad-hoc analysis.
- The script modifies nothing — it only reads and reports.
- Use this during discuss phase when a question needs empirical verification
  before making a decision.
