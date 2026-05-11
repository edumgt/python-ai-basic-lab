# AI/ML Basic Class — 퀀트를 위한 머신러닝과 딥러닝

114개 챕터 실습 코드 + FastAPI 백엔드 + 주식 AI 실험실(웹 앱)로 구성된 AI/ML 학습 환경입니다.  
챕터를 선택하고 **"실행"** 버튼만 누르면 Python 코드와 실행 결과를 브라우저에서 바로 확인할 수 있습니다.

---

## 사전 준비 — Docker 환경 구성

> 이 실습 환경은 **Docker로 Ollama · Qdrant 등이 미리 설치된 상태**를 전제로 합니다.  
> Docker를 처음 접하는 분은 먼저 아래 커리큘럼을 수강하세요.

### 선수 repo - https://github.com/edumgt/edumgt-lab-init
### 선수 repo - https://github.com/edumgt/investment-analysis
### 선수 repo - https://github.com/edumgt/docker-class

---

## 프로젝트 진행 전 Serving 인프라 구축

### https://github.com/edumgt/aws-ec2-alb-lab
### https://github.com/edumgt/openstack-private-cloud
### https://github.com/edumgt/python-crawling-lab


---

### 1단계: Docker Desktop 설치

| OS | 설치 링크 | 비고 |
|---|---|---|
| **Windows** | [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/) | WSL2 백엔드 권장 |
| **macOS** | [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/) | Apple Silicon 지원 |
| **Linux** | [Docker Engine](https://docs.docker.com/engine/install/) | Compose Plugin 함께 설치 |

설치 후 정상 동작 확인:

```bash
docker version
docker compose version
```

> **Windows WSL2 포트 충돌 시**  
> PowerShell에서 `netsh interface portproxy show all` 로 포트 현황 확인.  
> 자세한 트러블슈팅은 [docker-class → WSL 포트 80 문제 해결](https://github.com/edumgt/docker-class#7-wsl-%ED%8F%AC%ED%8A%B8-80-%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85) 참고.

---

### 2단계: 프로젝트 클론

```bash
git clone https://github.com/edumgt/python-ai-basic-lab
cd python-ai-basic-lab
```

---

### 3단계: 전체 AI 스택 실행 (Docker Compose)

```bash
# 빌드 후 백그라운드 실행
docker compose up --build -d
```

컨테이너가 실행되면 다음 서비스가 준비됩니다:

| 서비스 | 컨테이너명 | 역할 | 접속 주소 |
|---|---|---|---|
| `app` | `ai-lab-app` | FastAPI 학습 서버 · 주식 AI 실험실 | http://localhost:8000 |
| `ollama` | `ai-lab-ollama` | 로컬 LLM — 자연어 설명 생성 | http://localhost:11434 |
| `qdrant` | `ai-lab-qdrant` | 벡터 DB — 의미 기반 검색 | http://localhost:6333 |

---

### 4단계: Ollama 언어 모델 다운로드

```bash
# llama3.2 모델 다운로드 (최초 1회, 약 2GB)
docker exec ai-lab-ollama ollama pull llama3.2

# 사용 가능한 모델 확인
docker exec ai-lab-ollama ollama list
```

> **더 큰 모델을 원한다면**  
> `docker exec ai-lab-ollama ollama pull llama3.1`  (8B, 약 5GB)  
> 모델명은 `docker-compose.yml`의 `OLLAMA_MODEL` 환경변수로 변경합니다.

> **GPU 가속 (NVIDIA)**  
> `docker-compose.yml`의 GPU 섹션 주석을 해제하면 응답 속도가 크게 향상됩니다.

---

### 5단계: 브라우저에서 접속

| URL | 설명 |
|---|---|
| http://localhost:8000 | AI/ML 챕터 실습 환경 |
| http://localhost:8000/lab | 📊 주식 AI 실험실 (직접 데이터 입력 + AI 분석) |
| http://localhost:8000/docs | FastAPI Swagger UI |
| http://localhost:6333/dashboard | Qdrant 대시보드 |

---

### Docker 관리 명령어

```bash
# 실행 상태 확인
docker compose ps

# 실시간 로그 확인
docker compose logs -f app
docker compose logs -f ollama

# 재시작
docker compose restart app

# 중지 (데이터 유지)
docker compose down

# 완전 초기화 (볼륨 포함 삭제)
docker compose down -v
```

---

### 로컬 Python으로 실행 (Docker 없이)

Docker 없이 직접 실행하는 방법입니다. Ollama는 별도 실행이 필요합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Ollama URL을 환경변수로 지정:

```bash
export OLLAMA_URL=http://localhost:11434   # Ollama가 다른 호스트에 있다면 해당 주소로
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 학습 목표

- 머신러닝 핵심 모델 (회귀, SVM, Random Forest, Ensemble/XGBoost/LightGBM) 이해 및 실습
- 딥러닝 모델 (MLP, CNN, RNN/LSTM, Transformer) 구조 파악 및 퀀트 적용
- 하이퍼파라미터 튜닝 (GridSearch, Optuna), 교차 검증 (Purged K-Fold, Walk-Forward) 실습
- 클러스터링 (K-Means, DBSCAN, Hierarchical) 을 통한 종목 군집화
- 최신 시계열 Transformer 모델 (PatchTST, TFT, iTransformer) 학습
- **주식 AI 실험실**: 주가 데이터를 직접 입력해 ML/DL 모델로 분석하고 Ollama AI의 자연어 설명 체험

---

## 프로젝트 구성

```
python-ai-basic-lab/
├── chapters/           # chapter01 ~ chapter114 (README.md + practice.py)
├── docs/               # 모듈 6 학습 문서 (16.md ~ 26.md) + 용어 사전
├── backend/app/        # FastAPI 서버 (챕터 실행 API + 주식 분석 API + Ollama 연동)
├── frontend/           # 브라우저 UI
│   ├── index.html      # 챕터 학습 SPA
│   ├── stock_lab.html  # 주식 AI 실험실
│   ├── app.js          # 챕터 학습 로직
│   └── stock_lab.js    # 실험실 그리드·차트·챗봇 로직
├── scripts/            # 자동 생성 및 검증 스크립트
├── Dockerfile          # FastAPI 앱 이미지
├── docker-compose.yml  # app + ollama + qdrant
└── requirements.txt    # pip 의존성 목록
```

---

## 학습 로드맵

### 모듈 1–5: 기초 과정 (chapter01 ~ 99)

| 모듈 | 챕터 범위 | 주제 |
|------|-----------|------|
| 모듈 1 | chapter01 ~ 05 | Python·NumPy·Pandas·확률·선형대수 기초 |
| 모듈 2 | chapter06 ~ 15 | 데이터 분석·전처리·피처 엔지니어링 |
| 모듈 3 | chapter16 ~ 20 | 머신러닝 기초 (회귀·트리·군집·평가) |
| 모듈 4 | chapter21 ~ 30 | 딥러닝 기초 (신경망·역전파·CNN 기초) |
| 모듈 5 | chapter31 ~ 99 | 심화 (하이퍼파라미터·앙상블·시계열·배포) |

각 챕터: **10분 개념 학습 + 30분 Python 실습**

### 모듈 6: 퀀트 ML/DL 실전 (chapter100 ~ 114 + docs/16~26.md)

| 문서 | Day | 주제 | 관련 챕터 |
|------|-----|------|-----------|
| [docs/16.md](docs/16.md) | Day 029–030 | 머신러닝 개요 & 선형/로지스틱 회귀 | chapter05, 06, 11 |
| [docs/17.md](docs/17.md) | Day 031 | SVM (Support Vector Machine) | chapter100 |
| [docs/18.md](docs/18.md) | Day 032 | Decision Tree & Random Forest | chapter07, 08 |
| [docs/19.md](docs/19.md) | Day 033 | 앙상블 & Gradient Boosting (XGBoost, LightGBM) | chapter09, 110 |
| [docs/20.md](docs/20.md) | Day 034 | 클러스터링 (K-Means, DBSCAN, Hierarchical) | chapter09, 109 |
| [docs/21.md](docs/21.md) | Day 035 | 딥러닝 기초 (MLP, BatchNorm, Dropout) | chapter21–29 |
| [docs/22.md](docs/22.md) | Day 036 | CNN (1D-CNN, Grad-CAM) | chapter30 |
| [docs/23.md](docs/23.md) | Day 037 | RNN & LSTM (Attention-LSTM) | chapter101, 102 |
| [docs/24.md](docs/24.md) | Day 038 | Transformer 기초 (Self-Attention) | chapter103 |
| [docs/25.md](docs/25.md) | Day 039 | 시계열 Transformer (PatchTST, TFT, iTransformer) | chapter103, 112 |
| [docs/26.md](docs/26.md) | Day 040 | 성능 평가 & 하이퍼파라미터 튜닝 | chapter10, 11, 107, 108, 112 |

---

## 퀀트 핵심 개념

| 개념 | 설명 |
|------|------|
| **IC (Information Coefficient)** | 예측값과 실제 수익률의 Pearson 상관 |
| **Rank IC** | 순위 기반 Spearman 상관 — 이상치에 강건 |
| **ICIR** | IC / IC 표준편차 — 신호 일관성 측정 |
| **Walk-Forward Validation** | 미래 데이터 누출 방지 시계열 교차 검증 |
| **Purged K-Fold** | 학습/검증 경계에 Embargo 기간 추가 |
| **Long-Short Backtest** | 상위/하위 분위 포트폴리오 수익률 비교 |

---

## 문서 인덱스

| 문서 | 설명 |
|------|------|
| [docs/Dict.md](docs/Dict.md) | AI/ML·퀀트 용어 사전 (한국어, 개발자 눈높이) |
| [docs/16.md](docs/16.md) | 머신러닝 개요, 선형·로지스틱 회귀, 삼성전자 데이터셋 |
| [docs/17.md](docs/17.md) | SVM — 주가 구분선 긋기 |
| [docs/18.md](docs/18.md) | Decision Tree · Random Forest — 스무고개 모델 |
| [docs/19.md](docs/19.md) | 앙상블 · Gradient Boosting · XGBoost · LightGBM |
| [docs/20.md](docs/20.md) | 클러스터링 — 비슷한 종목끼리 자동 분류 |
| [docs/21.md](docs/21.md) | 딥러닝 기초 — MLP로 주가 방향 예측 |
| [docs/22.md](docs/22.md) | CNN — 주가 차트 패턴 탐지 |
| [docs/23.md](docs/23.md) | RNN · LSTM — 주가 흐름 기억하기 |
| [docs/24.md](docs/24.md) | Transformer · Attention — 중요한 날 집중하기 |
| [docs/25.md](docs/25.md) | PatchTST · TFT · iTransformer — 더 스마트한 예측 |
| [docs/26.md](docs/26.md) | 모델 평가 · 투자 시뮬레이션 · 하이퍼파라미터 튜닝 |
