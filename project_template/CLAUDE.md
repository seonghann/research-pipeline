# Project: <PROJECT_NAME>

> Project-specific Claude Code config.
> Global research pipeline rules are in `~/.claude/CLAUDE.md`.
> This file adds project-specific context.

## Project Overview

<!-- Brief description of what this project does -->

**Research Goal**:

**Current Phase**:

**Key References**:
- [[docs/obsidian/...]]

---

## Project-Specific Context

### Data
- Dataset location: `data/`
- Key data characteristics:

### Model Architecture
- Main model: `src/model/`
- Key design decisions:

### Dependencies
- Core: PyTorch, PyG, RDKit, etc.
- Config: Hydra/OmegaConf
- Experiment tracking: wandb

---

## Active Hypotheses

<!-- Updated periodically during project compaction -->

- [검증중] ...
- [채택] ...

---

## Project-Specific Rules

<!-- Add any rules specific to this project that supplement the global config -->

### Naming Conventions
- Experiment ID prefix: `<PROJECT>`

### Special Considerations
- (e.g., "RDKit mol objects are not picklable — always convert to SMILES for serialization")

---

## Quick Links

- Latest progress: `docs/progress/` (most recent file)
- Research context: `docs/obsidian/`
- Experiment registry: `experiments/registry.csv`
