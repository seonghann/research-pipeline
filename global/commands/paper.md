# /paper — Search Research Papers

Search arXiv for papers relevant to current research.

## Usage
```
/paper <topic, method, or specific question>
```

## Examples
```
/paper "diffusion models for 3D molecular generation"
/paper "equivariant neural networks for protein structure"
/paper "fragment-based drug design with deep learning, last 2 years"
```

## Behavior

**Delegate to `@paper-fetcher` agent:**

```
Task("Papers: <query>")
```

The paper-fetcher will:
1. Search arXiv via MCP
2. Filter and rank top 3-5 relevant papers
3. Return structured summaries with key ideas, methods, results

## When to Use

- During **discuss** phase — "what's the state of the art in X?"
- During **analyze** phase — "is there existing work on this approach?"
- When reviewer/colleague mentions a method you're unfamiliar with
- When exploring a new research direction

## Output

Structured paper summaries (under 800 tokens) with:
- Title, authors, arXiv ID
- Key idea and method summary
- Relevance to your question
- Suggested follow-up searches

## Notes

- Requires `arxiv` MCP server configured in `~/.claude.json`
- Only searches arXiv — not Google Scholar, Semantic Scholar, etc.
- Does NOT download full papers — summaries only
- For deep reading, use the arXiv ID to find the full paper yourself
