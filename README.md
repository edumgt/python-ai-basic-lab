# AI/ML Basic Class — 퀀트를 위한 머신러닝과 딥러닝

114개 챕터 실습 코드 + FastAPI 백엔드 + 브라우저 기반 웹 앱으로 구성된 AI/ML 학습 환경입니다.
챕터를 선택하고 **"실행"** 버튼만 누르면 Python 코드와 실행 결과를 브라우저에서 바로 확인할 수 있습니다.

---

## 학습 목표

- 머신러닝 핵심 모델 (회귀, SVM, Random Forest, Ensemble/XGBoost/LightGBM) 이해 및 실습
- 딥러닝 모델 (MLP, CNN, RNN/LSTM, Transformer) 구조 파악 및 퀀트 적용
- 하이퍼파라미터 튜닝 (GridSearch, Optuna), 교차 검증 (Purged K-Fold, Walk-Forward) 실습
- 클러스터링 (K-Means, DBSCAN, Hierarchical) 을 통한 종목 군집화
- 최신 시계열 Transformer 모델 (PatchTST, TFT, iTransformer) 학습

---

## 프로젝트 구성

```
python-ai-basic-lab/
├── chapters/           # chapter01 ~ chapter114 (README.md + practice.py)
├── docs/               # 모듈 6 학습 문서 (16.md ~ 26.md) + 용어 사전
├── backend/app/        # FastAPI 서버 (챕터 실행 API + 학습 문서 API)
├── frontend/           # 브라우저 UI (사이드바 · 소스 보기 · 실행 · README)
├── scripts/            # 자동 생성 및 검증 스크립트
└── pyproject.toml      # Poetry 의존성 관리
```

---

## 실행 방법

```bash
cd /home/ubuntu/python-ai-basic-lab
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]" jinja2 numpy pandas scikit-learn matplotlib seaborn python-multipart
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8888
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
| [docs/Dict.md](docs/Dict.md) | AI/ML 수학·통계 용어 사전 (한국어) |
| [docs/16.md](docs/16.md) | 머신러닝 개요, 회귀, IC/Rank IC, 금융 지표 수식↔코드 |
| [docs/17.md](docs/17.md) | SVM 이론, 커널 트릭, SVR |
| [docs/18.md](docs/18.md) | Decision Tree, Random Forest, SHAP |
| [docs/19.md](docs/19.md) | XGBoost, LightGBM, Optuna, 스태킹 앙상블 |
| [docs/20.md](docs/20.md) | K-Means, DBSCAN, 계층적 군집화, 종목 클러스터링 |
| [docs/21.md](docs/21.md) | PyTorch MLP, 학습 루프, 시장 레짐 감지 |
| [docs/22.md](docs/22.md) | 1D-CNN, 멀티채널 OHLCV, Grad-CAM |
| [docs/23.md](docs/23.md) | LSTM/GRU, Attention-LSTM, IC 평가 |
| [docs/24.md](docs/24.md) | Self-Attention, Multi-Head, Positional Encoding |
| [docs/25.md](docs/25.md) | PatchTST, TFT, iTransformer |
| [docs/26.md](docs/26.md) | 퀀트 평가 지표, Purged K-Fold, Optuna 튜닝 |
