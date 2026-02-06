# 📘 **Development & Coding Style Guideline (Pure Version)**

# **1. Core Principles**

### 🔹 1.1 Readability > Cleverness
한 줄이라도 더 명확하게 보이면 그게 항상 더 좋은 코드다.  
연구 특성상 재현성과 유지보수가 중요하므로 “한 번에 이해되는 코드”가 최우선이다.
### 🔹 1.2 Deterministic & Config-driven
seed, 경로, 하이퍼파라미터 등은 하드코딩하지 않고 반드시 config에서 주입한다.
### 🔹 1.3 Separation of Concerns
데이터 처리, 모델 정의, 학습 로직, 유틸 함수, 실행 스크립트를 철저히 분리한다.
### 🔹 1.4 최소 의존성
지나친 dependency 추가를 피하고, 환경을 깔끔하게 유지한다.

---

# **2. Project Structure Rules**

최소 요구 구조:
```
project/
  ├── src/            # 핵심 모듈 (dataset, model, utils, trainer 등)
  ├── cfgs/           # config files (YAML)
  ├── analyze/           # config files (YAML)
  ├── scripts/        # run scripts, training/eval entrypoints
  ├── test/           # unit tests
  ├── data/           # datasets (raw/symlink)
  ├── notebooks/      # exploratory work only
  └── docs/           # documentation (incl. this guideline)
```

원칙:
- `src/` = 라이브러리처럼 동작하도록 설계
- `scripts/` = 항상 얇게 유지 (config load → module instantiate → run())
- `notebooks/` = 절대 로직/모델/핵심 코드 포함 금지
- `test/` = 주요 모듈의 유닛 테스트 작성
    
---

# **3. Naming Standards**

### 🔹 Python Naming

| 항목      | 규칙                  | 예시                               |
| ------- | ------------------- | -------------------------------- |
| 변수      | lower_snake_case    | `learning_rate`, `num_steps`     |
| 함수      | lower_snake_case    | `build_model()`, `load_data()`   |
| 클래스     | CamelCase           | `GraphEncoder`, `DiffusionModel` |
| 상수      | UPPER_SNAKE_CASE    | `DEFAULT_LR = 1e-3`              |
| private | leading underscore  | `_compute_mask()`                |
| 파일명     | lower_snake_case.py | `graph_encoder.py`               |

**금지:**
- `data1`, `test2`, `foo`, `bar` 같은 의미 없는 이름
- `model2.py`, `new_model.py` 같은 히스토리 드러나는 파일명

---

# **4. Module Design Rules**

### 🔹 4.1 한 함수는 한 가지 역할만
비대한 함수 금지. 책임 단일화.
### 🔹 4.2 파일 크기 규칙
- 한 파일은 500줄을 넘기지 않는 것을 권장
- 모델 구조가 크면 **Encoder / Decoder / Core module**로 분리
- utils 남용 금지 → 기능별 폴더로 명확히 나누기
### 🔹 4.3 Docstring 필수
- 모든 public 함수/클래스에는 아래 형태의 docstring을 포함:
```python
def compute_loss(pred: Tensor, target: Tensor) -> Tensor:
    """
    Compute reconstruction loss.

    Args:
        pred (Tensor): predicted output.
        target (Tensor): ground truth.

    Returns:
        Tensor: scalar loss value.
    """
```

### 🔹 4.4 Avoid Side Effects
함수는 외부 전역 변수를 조작하지 않는다.

---

# **5. Logging & Error Handling**

### 🔹 5.1 print() 금지 → logger 사용
권장 패턴:
```python
import logging
logger = logging.getLogger(__name__)
```

### 🔹 5.2 broad exception 금지

나쁜 예:
```python
try:
    ...
except:
    pass
```

좋은 예:
```python
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise
```

### 🔹 5.3 에러는 반드시 기록하고 재발 방지 주석을 남긴다.

---

# **6. Type Hints & Static Analysis**

### 🔹 6.1 Type hints는 필수
```python
def forward(self, x: Tensor, mask: Tensor | None = None) -> Tensor:
```

### 🔹 6.2 권장 도구
- **ruff** (format + lint)
- **black** (formatter)
- **pyright** or **basedpyright** (type checking)
- **isort** (import 정렬)
### 🔹 6.3 Formatting Rule
- black default style 사용
- trailing comma 허용
- line length는 88 or 100으로 통일

---

# **7. Config Rules**

### 🔹 7.1 모든 하이퍼파라미터는 config에 기록
- 모델 구조
- 데이터 경로
- 학습 설정
- seed

### 🔹 7.2 코드 내부에서 magic number 금지
나쁜 예:
```python
x = self.encoder(x, layers=4)
```

좋은 예:
```python
x = self.encoder(x, layers=self.config.model.layers)
```

### 🔹 7.3 config는 재사용 가능하고 모듈화되어야 한다
- base.yaml + override 구조 권장
- 체계적인 cfgs/ 구조 유지

---

# **8. Training/Evaluation Script Rules**
### 🔹 8.1 run scripts는 최소 로직만 포함
형식:
```python
def main():
    cfg = load_config()
    set_seed(cfg.seed)

    model = build_model(cfg.model)
    trainer = Trainer(model, cfg)

    trainer.run()
```

### 🔹 8.2 scripts에서 src-import를 직접 수정하지 않는다
src는 항상 독립적으로 테스트 가능해야 함.

---

# **9. Git Workflow**

### 🔹 9.1 Commit은 작고 의미 있게
“하나의 logical change = 하나의 commit"
### 🔹 9.2 Commit message rule
```
[feat] add graph encoder
[fix] handle dimension mismatch in sampler
[refactor] clean training loop
[docs] update guidelines
[style] reformat using black
```
### 🔹 9.3 Branch naming

```
feature/<name>
fix/<bugname>
refactor/<module>
```

---

# **10. Testing Standards**

### 🔹 10.1 test/ 디렉토리는 필수
- model forward
- loss function
- data transforms
- utility functions

### 🔹 10.2 notebooks로 테스트하지 말 것
노트북은 분석용, 테스트는 고립된 환경에서 해야 한다.

---

# **11. Dependency Rules**

- dependency는 반드시 `requirements.txt` 또는 `environment.yml`로 관리
- deprecated library 사용 금지
- 직접 구현 가능한 것에 heavy dependency 추가 금지
- 버전 호환성 체크 필수

---

# **12. Code Safety Rules**
- global mutable state를 피한다
- random seed는 반드시 config에서 제어
- device/cuda 관련 코드는 명확히 기록
- path handling은 `pathlib.Path` 사용
