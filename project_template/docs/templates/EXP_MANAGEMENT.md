# Experiment Management Guideline
_Reproducibility · Traceability · Automation Standard_

---

## 0. Purpose
이 문서는 프로젝트 내 모든 실험을  
**재현 가능(reproducible)** 하고  
**추적 가능(traceable)** 하며  
**정돈된 구조로 관리**하기 위한 표준을 정의한다.

적용 대상:
- 개발자
- 연구자
- 실험 자동화 스크립트 작성자
- 논문 작성 시 실험 재현이 필요한 모든 구성원

---

## 1. Experiment ID (exp_id)
모든 실험에는 고유한 ID를 부여해야 하며, ID는 아래 규칙을 따른다.

### 1.1 Format
```
<PROJECT>-<YYMMDD>-<NN>
```
예시:
```
FRAG3D-250112-01
FRAG3D-250228-03
FRAG3D_SCHEDULER-250401-02
```
### 1.2 Definitions

| 필드          | 설명                               |
| ----------- | -------------------------------- |
| `<PROJECT>` | 프로젝트 명 또는 약어 (FRAG3D, FRAG3D_SCHEDULER 등) |
| `<YYMMDD>`  | 실험 **계획** 날짜                     |
| `<NN>`      | 해당 날짜에 계획된 n번째 실험 그룹 (01부터 시작)   |

### 1.3 Experiment vs Version

| 개념 | 설명 | 예시 |
| --- | --- | --- |
| **Experiment (exp_id)** | 특정 측면을 밝히기 위한 관련 실행들의 집합 | `FRAG3D-251231-01`: FM Overfitting Test |
| **Version (version_N)** | 해당 실험 내 개별 실행 | `version_0`, `version_1`, ... |

하나의 실험(exp_id) 아래 여러 버전(version)이 존재할 수 있다:
- 파라미터 튜닝을 위한 반복 실행
- 버그 수정 후 재실행
- 다른 시드로 재현성 검증

### 1.4 Rules
- 실험 실행 시 exp_id는 명시적으로 전달하거나 자동 생성한다.
- 날짜가 바뀌면 번호(NN)를 다시 01부터 시작한다.
- exp_id는 **실험 디렉토리명 · 로그 파일명 · 결과 파일명 · config 기록** 모두에서 동일해야 한다.
- 각 실행(run)은 version_N 하위 디렉토리에 저장된다.

---

## 2. Experiment Directory Structure

모든 실험은 다음과 같이 **독립된 디렉토리**로 기록된다:

```
experiments/
├── FRAG3D-251231-01/           # Experiment: FM Overfitting Test
│   ├── version_0/              # 첫 번째 실행
│   │   ├── hydra/              # Hydra config snapshots
│   │   ├── checkpoint/         # Model checkpoints
│   │   ├── wandb/              # WandB run files
│   │   ├── train_config.yaml   # Training config snapshot
│   │   └── train.log           # Training log
│   ├── version_1/              # 두 번째 실행 (파라미터 조정 등)
│   │   └── ...
│   └── version_2/              # 세 번째 실행
│       └── ...
├── FRAG3D-251231-02/           # 다른 실험
│   └── ...
└── registry.csv                # 전체 실험 목록
```

### 2.1 Required Files (per version)

| 파일                    | 설명                                      |
| --------------------- | --------------------------------------- |
| **train_config.yaml** | 해당 실행의 전체 config snapshot              |
| **hydra/**            | Hydra config snapshots                  |
| **train.log**         | stdout, stderr, training logs           |
| **checkpoint/**       | model weights (topk_map.txt 포함)         |
| **wandb/**            | WandB run files (optional)              |

---

## 3. Automatic Experiment Setup
실험 실행 스크립트(e.g., `scripts/run_train.py`)는 다음을 자동으로 수행해야 한다:

### 3.1 exp_id 생성 또는 수신
- `--exp-id <ID>` 지정 시 그대로 사용한다.
- 미지정 시 `<PROJECT>-<YYMMDD>-<NN>` 형식으로 자동 생성한다.
- 자동 생성 시 experiments 디렉토리 내 NN을 자동 증가시키도록 구현한다.

### 3.2 experiment directory 생성

```
experiments/<exp_id>/
````

### 3.3 필수 파일 자동 기록

| 항목        | 방식                                            |
| --------- | --------------------------------------------- |
| config 복사 | `cfgs/...yaml → experiments/<id>/config.yaml` |
| git hash  | `git rev-parse HEAD`                          |
| env 정보    | Python, Torch, CUDA 버전 자동 기록                  |
| run args  | `" ".join(sys.argv)`                          |

### 3.4 trainer/evaluator에 exp_dir 전달
```python
trainer = Trainer(cfg, exp_dir=Path(exp_dir))
trainer.run()
````

---

## 4. Config Management

### 4.1 Config immutability
실험 시작 후 config는:
- YAML 복사본이 생성되며,
- 절대 수정해서는 안 된다.

변경이 필요한 경우:
- 새로운 config 파일 생성
- 새로운 exp_id로 재실험

### 4.2 No hardcoded parameters
모든 실험 파라미터는 **오직 config에서만 관리**한다.

---

## 5. Logging Standards

### 5.1 Training logs 위치
```
experiments/<exp_id>/logs/train.log
```

### 5.2 stdout/stderr redirect
가능한 모든 실행 로그는 log 파일로 저장되도록 한다.

### 5.3 metrics logging format (권장)
`metrics.json` 예시:

```json
{
  "epoch": 100,
  "train_loss": 0.124,
  "val_loss": 0.138,
  "best_val": 0.128,
  "timestamp": "2025-01-12T03:20:12"
}
```

---

## 6. Experiment Registry (`experiments/registry.csv`)
registry.csv는 전체 실험 목록을 관리하는 파일이다.

예:
```csv
exp_id,project,date,description,config,commit
FRAG3D-251231-01,FRAG3D,251231,FM Overfitting Test,configs/train_overfit.yaml,9bd9ce9
FRAG3D-251231-02,FRAG3D,251231,Learning rate sweep,configs/train_lr_sweep.yaml,9bd9ce9
```

### 6.1 Updates
새 실험을 생성하는 스크립트가 registry.csv에 자동으로 한 줄 추가하는 것을 권장한다.

---

## 7. Experiment Log (`docs/experiment/<exp_id>.md`)

각 실험에 대한 상세 계획 및 결과를 기록하는 문서이다.

### 7.1 Location
```
docs/experiment/<exp_id>.md
```

### 7.2 Template
```markdown
# <exp_id>: <Experiment Title>

## Experiment Info
| Field | Value |
|-------|-------|
| exp_id | <exp_id> |
| Planned Date | YYYY-MM-DD |
| Status | Planned / In Progress / Completed / Aborted |

---

## Objective
이 실험을 통해 밝히고자 하는 것:
-

---

## Hypothesis
-

---

## Method
### Configuration
- Config file: `configs/xxx.yaml`
- Key parameters:
  -

### Success Criteria
| Metric | Threshold |
|--------|-----------|
| | |

---

## Versions
| Version | Date | Description | Status | Notes |
|---------|------|-------------|--------|-------|
| version_0 | YYYY-MM-DD | Initial run | | |
| version_1 | YYYY-MM-DD | Param adjustment | | |

---

## Results
### Summary
-

### Key Findings
-

### Plots / Figures
-

---

## Conclusion
-

---

## Next Steps
-
```

### 7.3 Guidelines
- 실험 계획 시 작성하고, 실행 중/후에 업데이트
- 각 version의 결과를 Versions 테이블에 기록
- 최종 결론과 다음 단계를 명시

---

## 8. Reproducibility Checklist

실험을 “완료”했다고 간주하기 위한 조건:
-  exp_id가 부여되었는가
-  experiment directory가 생성되었는가
-  config.yaml이 저장되었는가
-  git commit hash가 기록되었는가
-  env.txt가 존재하는가
-  run_args.txt가 존재하는가
-  logs/가 생성되었는가
-  results/metrics.json이 기록되었는가
-  checkpoint가 존재하는가
    
---

## 9. Directory Naming Conventions
### 9.1 root experiments folder
```
experiments/
```

### 9.2 each experiment
```
experiments/<exp_id>/
```

### 9.3 result file naming
```
metrics.json
plot_loss.png
samples_epoch001.pkl
```

### 9.4 checkpoint naming
```
best.ckpt
last.ckpt
epoch_050.ckpt (optional)
```

---

## 10. Removal / Archiving Policy
### 10.1 삭제 금지 원칙
실험 디렉토리는 **절대 삭제하지 않는다**.

### 10.2 오래된 실험 아카이브
필요할 경우:
```
experiments/archived/<year>/
```

### 10.3 용량 관리
- checkpoints/ 압축
- samples/ 일부만 유지

---

## 11. Recommended Toolkit (Optional)
- Python `pathlib` for file paths
- Hydra / OmegaConf for config management
- YAML / JSON for structured logs
- wandb / MLflow (optional)

---

## ✔ Summary
이 문서의 목적은 다음을 보장하는 것이다:
- 실험 단위 스냅샷을 통해 **완전 재현성 확보**
- exp_id 기반의 **일관된 추적성 확보**
- config-driven 구조를 통한 안정적인 실험 관리
- 코드/실험/결과를 명확히 분리해 **논문화 및 장기 유지보수 가능**


