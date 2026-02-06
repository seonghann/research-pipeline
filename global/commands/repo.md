# /repo — Explore External Repository

Clone and analyze an external repository to extract specific implementation details.

## Usage
```
/repo <github URL> "<what to find>"
```

## Examples
```
/repo https://github.com/user/diffusion-model "how is the denoising score matching loss implemented?"
/repo https://github.com/user/equivariant-gnn "encoder architecture and attention mechanism"
/repo https://github.com/user/fragment-vae "training loop and sampling procedure"
```

## Behavior

**Delegate to `@repo-explorer` agent:**

```
Task("Explore repo: <url> — <what to find>")
```

The repo-explorer will:
1. Shallow-clone the repo to `/tmp/`
2. Scan structure, find relevant code
3. Extract and summarize the specific information requested
4. Clean up (remove clone)

## When to Use

- Found a paper's reference implementation and want to understand specifics
- Colleague shared a repo and you need to understand their approach
- Want to compare your implementation with an existing one
- Need to understand a library's internal behavior

## Output

Structured analysis (under 1000 tokens) with:
- Repo structure overview
- Answer to the specific question with `<file:line>` references
- Relevant code snippets (max 30 lines)
- How it relates to your project
- Caveats (license, deps, assumptions)

## Rules

- Cloned to `/tmp/` only — never into your project
- Read-only — no code is copied into your project
- If you want to adopt a pattern, implement it yourself based on the understanding
- Check the license before using any ideas
