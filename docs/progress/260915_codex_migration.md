# Codex migration

## Context and authorization
2026-09-15: User requested full migration of the local research workflow, reproducible
research-pipeline updates, verification, commit and push. Remote machines have not
been selected or accessed. DMRL research code is outside this change.

Sources: [[global/CLAUDE.md]], [[global/commands/go.md]], [[setup.sh]].
Existing app import contains 9/10 commands and no standalone custom agent files.
The repository has newer graph/archive guidance than the imported global instructions.

## Plan and success criteria
- Preserve Claude assets; generate Codex AGENTS, 10 skills and 8 custom agent TOMLs.
- Preserve research phase checkpoints, integrity gates and permanent records.
- Replace platform-specific paths/delegation; avoid automatic destructive rollback.
- Install with unique backups, preserve unrelated config and support repeated runs.
- Merge missing MCP definitions without serializing credentials; record readiness.
- Adopt existing project guidance without changing scientific claims.
- Test isolated installation, repeatability, backups, config preservation and project adoption.
- Verify CLI can load the resulting configuration; commit and push this repository only.

## Execution and results

- Generated and validated 10 Codex skills, including the previously missing
  `source-command-go`, and 8 native custom-agent TOML files.
- Converted global and project instruction paths to `AGENTS.md` and Codex config paths.
- Replaced Claude-only `Task(...)` assumptions with native delegation plus an inline fallback.
- Removed automatic whole-worktree rollback and automatic temporary-clone deletion from the
  Codex distribution. Task commits stage explicit task-owned files only.
- Added a Python 3.11+/`uv` installer that preserves unrelated config, creates timestamped
  private backups, forwards `WANDB_API_KEY` by name, and is repeatable.
- Added Codex installation, server, tmux, skill invocation and regeneration documentation.
- Installed locally: 10 skills, 8 agents, global instructions, rules and config merge.
  Backup: `~/.codex/migration-backups/20260915T082008.264326Z/`.
- Adopted `/Users/ksh/obsidian/dev_code/DMRL/AGENTS.md`; scientific guidance was preserved and
  only known platform-path spelling was corrected.
- Isolated installer tests: 3 passed, 0 failed. Skill validation: 10 passed, 0 failed.
- `codex --strict-config doctor`: 21 checks OK, 0 failed. One optional warning remains because
  `WANDB_API_KEY` was not set in the prior Claude configuration or current shell.
- Active B200 host resolved as `nhn_dmrl_ts` (`DMRL-260615`). Its pipeline checkout was clean
  and was fast-forwarded to this migration. Official standalone Codex CLI 0.154.0, 10 skills,
  8 agents and the DMRL project guidance were installed. Backup:
  `~/.codex/migration-backups/20260915T082613.533926Z/`.
- Server validation: config parsed, standalone runtime and HTTPS reachability passed. Interactive
  ChatGPT authentication remains user-bound; WebSocket was unavailable but HTTPS fallback was
  reachable. `WANDB_API_KEY` is also unset on both hosts.

## Conclusion

The local and active B200 workflows are migrated and reproducible from this repository. Claude
assets remain available. The server requires one user-bound ChatGPT device login before its first
Codex session. Long jobs remain independent named tmux processes whose launch metadata belongs in
progress logs.
