# 🤖 AI/ML Basic Class — 초등학생도 할 수 있는 인공지능 실습

> **Python + 웹 브라우저**만 있으면 바로 시작할 수 있는, 초등학생·입문자 친화 AI/ML 실습 프로젝트입니다.

기존 Markdown 자료(수학/통계 용어, 수식-코드 매핑, Python 예제)를 바탕으로 **99개 챕터 실습 코드**와 **FastAPI 백엔드 + 프론트엔드 웹 앱**을 구성했습니다.
챕터를 선택하고 **"실행"** 버튼만 누르면, Python 코드와 실행 결과를 브라우저에서 바로 확인할 수 있습니다.

---

## 📁 프로젝트 구성

| 경로 | 설명 |
|---|---|
| `chapters/chapter01` ~ `chapter99` | 챕터별 `README.md` + `practice.py` (실습 코드) |
| `backend/app/main.py` | FastAPI 백엔드 — 챕터 코드 실행 API 제공 |
| `frontend/` | 웹 브라우저 UI — 소스 보기 · 실행 · 결과 확인 |
| `DOCS/` | 학습 문서 인덱스 및 확장 설명 (수식↔코드 매핑, 용어 사전 등) |
| `scripts/` | 자동 생성·검증 스크립트 |
| `pyproject.toml` | Python 의존성 및 프로젝트 메타데이터 (Poetry) |
| `poetry.lock` | 고정된 의존성 버전 잠금 파일 |

---

## 🚀 실행 방법

```bash
# 1. Poetry 설치 (최초 1회)
pip install poetry

# 2. 의존성 설치 (가상환경 자동 생성)
poetry install

# 3. 서버 실행
poetry run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8888
```

브라우저에서 **`http://localhost:8888`** 에 접속하면 좌측 챕터 메뉴에서 원하는 챕터를 선택하고 실행 결과(JSON)를 확인할 수 있습니다.

### 런타임 스모크 테스트

```bash
./scripts/runtime_smoke_check.sh
```

### 초등학생 친화 자산 자동 생성 (주석 · 설명 문서 · 음성)

```bash
python3 scripts/generate_kids_assets.py --mode all
```

---

## 🧒 초등학생 친화 구성

| 자산 | 설명 |
|---|---|
| **줄 단위 설명 주석** | 모든 Python 소스(챕터 + 백엔드)에 쉬운 한글 주석 추가 |
| **`python_explain.md`** | 각 폴더마다 코드 흐름을 풀어 쓴 설명 문서 |
| **`python_explain_ko_female.mp3`** | 설명 문서를 한국 여성 음성(TTS)으로 변환한 오디오 파일 |

---

## 📚 학습 로드맵

### 기초 과정 (chapter01 ~ 30)

| 구간 | 주제 |
|---|---|
| **chapter01 ~ 04** | 데이터/수학 기초 (NumPy · Pandas · 확률 · 선형대수) |
| **chapter05 ~ 11** | 핵심 ML 모델 + 평가/검증 (회귀 · 트리 · 군집 · 지표) |
| **chapter12 ~ 18** | 실무형 전처리 · 재현성 · 배포 준비 |
| **chapter19 ~ 20** | FastAPI 서빙 및 통합 미니 프로젝트 |
| **chapter21** | 신경망 전체 흐름 요약 (Forward → Backward → 학습) |
| **chapter22 ~ 30** | 신경망 세부 실습 (행렬 · 활성화 · 소프트맥스 · 손실 · 역전파 · 최적화 · CNN) |

### 확장 과정 (chapter31 ~ 99)

| 구간 | 주제 |
|---|---|
| **chapter31 ~ 44** | 전처리 심화 · 피처 엔지니어링 · 재현성 |
| **chapter45 ~ 55** | 모델 평가 심화 (혼동행렬 · F1 · ROC · 학습곡선) |
| **chapter56 ~ 66** | 하이퍼파라미터 튜닝 · 앙상블 · 에러 분석 |
| **chapter67 ~ 77** | 신경망 심화 (활성화 · 손실 · 경사하강 · 정규화) |
| **chapter78 ~ 88** | 이미지 · 텍스트 · 시계열 · 생성형 AI 입문 |
| **chapter89 ~ 99** | 실전 프로젝트 (문제 정의 → 배포 → 윤리 → 발표 → 회고) |

- 각 챕터: **10분 개념 학습 + 30분 Python 실습**
- 전체 커리큘럼 문서: `DOCS/chapter01_99_restructured_ko.md`
- `chapter31~99`는 초급자용 스타터 코드(`run()` + phase별 demo)가 포함되어 바로 확장 가능합니다.

---

## 🖥️ 실행 화면 캡처

프론트엔드 웹 앱에서 챕터를 선택하고 실행한 화면입니다. 좌측에는 Python 소스 코드, 우측에는 실행 결과(JSON)가 표시됩니다.

### Chapter 01 · 데이터와 NumPy 기초

![Chapter01 - 데이터와 NumPy 기초 실행 결과](docs/images/chapter01_numpy_basics.png)

> NumPy 배열을 생성하고 평균(mean)과 표준편차(std)를 계산하는 기초 실습입니다.

### Chapter 05 · 선형회귀 (Linear Regression)

![Chapter05 - 선형회귀 실행 결과](docs/images/chapter05_linear_regression.png)

> scikit-learn의 `LinearRegression`으로 회귀 모델을 학습하고 MSE를 출력합니다.

### Chapter 08 · 랜덤포레스트 (Random Forest)

![Chapter08 - 랜덤포레스트 실행 결과](docs/images/chapter08_random_forest.png)

> `RandomForestClassifier`로 분류 모델을 학습한 뒤 F1 Score를 측정합니다.

### Chapter 21 · 신경망 기초와 학습 (Forward / Backward)

![Chapter21 - 신경망 기초와 학습 실행 결과](docs/images/chapter21_neural_network.png)

> 순전파(Forward) → 역전파(Backward) → 경사하강법을 NumPy로 직접 구현하여 학습 정확도를 확인합니다.

### Chapter 28 · 2층 신경망 학습 루프

![Chapter28 - 2층 신경망 fitting 루프 실행 결과](docs/images/chapter28_2layer_nn_fitting.png)

> 2층 신경망을 반복 학습하여 초기 손실 → 최종 손실 감소와 train_accuracy 달성 과정을 확인합니다.

---

## 📖 문서 인덱스

| 문서 | 설명 |
|---|---|
| `DOCS/README.md` | 전체 문서 목차 |
| `DOCS/Dict.md` | AI/ML 용어 사전 (한국어) |
| `DOCS/ai_ml_formula_to_code_mapping_ko.md` | 수식 ↔ Python 코드 매핑 |
| `DOCS/ai_ml_python_examples_expanded_ko.md` | Python 예제 모음 (확장판) |
| `DOCS/chapter01_99_restructured_ko.md` | 전체 99챕터 커리큘럼 |
| `DOCS/chapter22_30_index_ko.md` | 신경망 챕터(22~30) 색인 |
