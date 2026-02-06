# Research Pipeline for Claude Code

Claude Code 기반 AI 연구 워크플로우 자동화 셋업.

클라우드 서버에서 clone → `setup.sh` 실행 → 바로 사용.

## Philosophy

```
discuss (사람) → /go "task" (자동) → checkpoint에서만 판단 → 여러 프로젝트 동시 운용
```

**핵심 원칙:**
- **Hard Disc Logging**: 모든 중요한 결정/분석/결과는 파일로 남긴다 (세션 메모리 X)
- **Discuss-first**: 자동화는 충분한 논의 후에만 시작
- **Checkpoint 패턴**: 각 phase 완료 시 사람이 y/n/edit 결정
- **Context 누적**: `analyze/*.py` + `docs/progress/*.md` + git commit = 영구 기록

## Quick Start

```bash
# 1. Clone
git clone <this-repo> ~/research-pipeline
cd ~/research-pipeline

# 2. Install global config (→ ~/.claude/)
chmod +x setup.sh
./setup.sh install

# 3. Initialize a project
./setup.sh init ~/projects/my-project MyProject

# 4. Start working
cd ~/projects/my-project
claude  # Claude Code 시작
```

## What Gets Installed

### Global (`~/.claude/`)

| File | Purpose |
|------|---------|
| `CLAUDE.md` | 연구 파이프라인 규칙 (전 프로젝트 공통) |
| `settings.json` | 권한 설정 (git push 차단 등) |
| `commands/go.md` | `/go` — 전체 사이클 자동화 |
| `commands/prereport.md` | `/prereport` — pre-report 생성 |
| `commands/analyze.md` | `/analyze` — 분석 스크립트 생성/실행 |
| `commands/impl.md` | `/impl` — pre-report 기반 구현 |
| `commands/verify.md` | `/verify` — 검증 실행 |
| `commands/status.md` | `/status` — 프로젝트 현황 |
| `agents/prereport.md` | Pre-report 생성 (독립 context) |
| `agents/analyzer.md` | 분석 스크립트 작성/실행 (독립 context) |
| `agents/verifier.md` | 검증 실행 (독립 context) |

### Project Template

```
my-project/
├── CLAUDE.md                          # 프로젝트별 컨텍스트
├── docs/
│   ├── templates/
│   │   ├── SUMMARY_TEMPLATE.md        # progress log 템플릿
│   │   ├── ANALYSIS_TEMPLATE.md       # analyze 스크립트 가이드
│   │   ├── DEV_GUIDELINE.md           # 코딩 스타일
│   │   └── EXP_MANAGEMENT.md          # 실험 관리
│   ├── progress/                      # task별 progress log
│   ├── experiment/                    # 실험 계획/결과
│   └── obsidian/                      # 상위 연구 문서 (git pull)
├── analyze/                           # 분석 스크립트 (영구 보존)
├── experiments/                       # 실험 디렉토리
│   └── registry.csv
├── src/                               # 핵심 모듈
├── scripts/                           # 실행 스크립트
├── cfgs/                              # config files
└── test/                              # 테스트
```

## Workflow

### 일반적인 세션 흐름

```
1. /status                              ← 현재 상태 파악
2. 대화 (discuss phase)                  ← 문제 이해, 가설 설정
3. /analyze "이 현상이 왜 발생하는지?"      ← 필요 시 분석
4. /go "protein stereo fix"             ← 방향 확정 후 자동 사이클
   ├── Phase 1: pre-report → ⏸ 확인
   ├── Phase 2: implementation → ⏸ 확인
   ├── Phase 3: verification → ⏸ 확인
   └── Phase 4: post-report + commit
5. /compact                             ← 다음 태스크로
```

### 단계별 실행도 가능

```
/prereport "task description"   ← pre-report만
/impl                           ← 구현만 (pre-report 필요)
/verify                         ← 검증만
```

## Hard Disc Logging

```
commit A (260204)
├── docs/progress/260204_protein_stereo.md   ← pre-report
├── analyze/260204_protein_stereo_check.py   ← 분석 (실행 가능)
└── src/data/protein.py                      ← 아직 안 바뀜

commit B (260205)
├── docs/progress/260204_protein_stereo.md   ← post-report 추가
├── analyze/260204_protein_stereo_check.py   ← 그대로 (증거 보존)
├── src/data/protein.py                      ← fix 적용
```

하나의 commit에 **왜(progress) → 뭘 분석(analyze) → 뭘 바꿈(src)** 이 전부 들어감.

## Wiki-Link Convention

`[[파일명]]` 으로 cross-reference:

```markdown
## Context
이 태스크는 [[docs/progress/260204_protein_processing_bugfixes.md]] 에서 발견된
문제를 해결하기 위함. 분석 결과는 [[analyze/260204_protein_stereo_check.py]] 참조.

## 가설 상태
- [채택] star atom approach → 근거: [[analyze/260204_protein_stereo_check.py]]
- [기각] template hardcode → 근거: [[analyze/260204_stereo_template_test.py]]
```

Claude Code는 `[[...]]`를 보면 해당 파일을 읽어 context를 복원.

## Customization

### MCP 추가 (선택)

`~/.claude/settings.json`에 MCP 서버 설정 추가:

```json
{
  "mcpServers": {
    "wandb": {
      "command": "npx",
      "args": ["-y", "@wandb/mcp-server"]
    }
  }
}
```

### Agent/Command 추가

`~/.claude/agents/`나 `~/.claude/commands/`에 `.md` 파일 추가.

## Multiple Projects

여러 프로젝트를 동시에 운용할 때:

```bash
# 프로젝트별 초기화
./setup.sh init ~/projects/fragfm3d FragFM3D
./setup.sh init ~/projects/degpred DegPred

# 각 프로젝트에서 독립적으로 작업
cd ~/projects/fragfm3d && claude
cd ~/projects/degpred && claude

# 각각 /status로 현황 확인, /go로 태스크 실행
```

Global config(`~/.claude/`)는 공유, project config(`CLAUDE.md`)는 프로젝트별 독립.
