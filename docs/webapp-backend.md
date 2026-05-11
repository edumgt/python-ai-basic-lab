# 웹앱 백엔드(BE) 완전 해설서

> 이 문서는 "이 웹앱의 뒷부분 코드가 어떻게 생겼고, 무슨 일을 하는지"를  
> 초등학생도 이해할 수 있게 아주 쉽게 설명한 안내서입니다.

---

## 목차

1. [백엔드가 뭐예요?](#백엔드가-뭐예요)
2. [핵심 파일 한눈에 보기](#핵심-파일-한눈에-보기)
3. [웹앱 화면과 백엔드의 연결](#웹앱-화면과-백엔드의-연결)
4. [API란 무엇인가요?](#api란-무엇인가요)
5. [기능별 API 상세 설명](#기능별-api-상세-설명)
   - [시스템 상태 확인](#1-시스템-상태-확인)
   - [챕터 API - 학습 실습 코드 관리](#2-챕터-api---학습-실습-코드-관리)
   - [문서 API - 학습 문서 조회](#3-문서-api---학습-문서-조회)
   - [데이터셋 API - CSV 데이터 관리](#4-데이터셋-api---csv-데이터-관리)
   - [주식 AI 실험실 API](#5-주식-ai-실험실-api)
   - [예측 실험실 API - CSV 업로드 분석](#6-예측-실험실-api---csv-업로드-분석)
   - [DART 공시 투자 파이프라인 API](#7-dart-공시-투자-파이프라인-api)
   - [거시경제 투자 파이프라인 API](#8-거시경제-투자-파이프라인-api)
   - [뉴스 이벤트 컨설팅 API](#9-뉴스-이벤트-컨설팅-api)
   - [호텔-주가 실험실 API](#10-호텔-주가-실험실-api)
   - [AI 어시스턴트 API](#11-ai-어시스턴트-api)
6. [데이터가 여행하는 길 (흐름도)](#데이터가-여행하는-길-흐름도)
7. [주요 Python 라이브러리 소개](#주요-python-라이브러리-소개)
8. [서버를 직접 켜는 방법](#서버를-직접-켜는-방법)

---

## 백엔드가 뭐예요?

웹앱은 **프론트엔드(앞단)**와 **백엔드(뒷단)**로 나눌 수 있습니다.

| 구분 | 쉬운 비유 | 역할 |
|---|---|---|
| 프론트엔드 | 음식점 홀 (손님이 앉는 곳) | 화면, 버튼, 표를 보여주는 부분 |
| 백엔드 | 음식점 주방 (요리하는 곳) | 실제 계산, 데이터 저장, AI 분석을 담당하는 부분 |

즉, 여러분이 버튼을 누르면 **프론트엔드**가 주문을 받아 **백엔드**에 전달하고,  
백엔드가 요리(계산)를 끝내면 결과를 다시 화면에 보내줍니다.

---

## 핵심 파일 한눈에 보기

```
python-ai-basic-lab/
├── backend/
│   └── app/
│       ├── main.py              ← ★ 백엔드의 핵심! 모든 API가 여기에 있어요
│       ├── chapters/            ← 실습 코드 폴더 (chapter05, chapter06 ...)
│       ├── dart_utils.py        ← DART 공시 데이터 수집 도구
│       └── external_market_utils.py  ← FRED, World Bank 거시경제 데이터 도구
├── frontend/                    ← 화면(HTML/JS) 파일들
├── docs/                        ← 학습 문서들 (01.md ~ 12.md 등)
├── data/                        ← CSV 데이터 파일들
└── scripts/                     ← 데이터 갱신 스크립트
```

### `backend/app/main.py` 구조 요약

이 파일 하나에 **2,000줄 이상**의 코드가 있고, 크게 다음 블록으로 나뉩니다.

| 블록 | 하는 일 |
|---|---|
| 앱 초기화 | FastAPI 앱을 만들고 기본 설정을 합니다 |
| Pydantic 스키마 | 주고받는 데이터 모양을 정의합니다 |
| 내부 유틸리티 함수 | 여러 API가 공통으로 쓰는 작은 도구들 |
| 챕터 API | 학습 실습 코드 읽기·실행 |
| 문서 API | 마크다운 학습 문서 제공 |
| 데이터셋 API | CSV 데이터 목록과 미리보기 |
| 주식 AI 실험실 API | 주가 데이터로 ML 분석 |
| DART API | 공시·재무제표 파이프라인 |
| 거시경제 API | FRED, World Bank 거시 신호 |
| 뉴스 컨설팅 API | 뉴스를 읽고 업종 영향 분석 |
| 호텔-주가 API | 호텔 예약률 + 주가 멀티모델 |
| 어시스턴트 API | 자연어 질문을 실험실 화면으로 안내 |
| 프론트엔드 SPA 라우트 | 화면 파일(HTML) 제공 |

---

## 웹앱 화면과 백엔드의 연결

이 웹앱에는 여러 화면(페이지)이 있습니다.  
각 화면이 어떤 백엔드 주소를 사용하는지 정리하면 이렇습니다.

| 화면 주소 | 화면 이름 | 주로 쓰는 백엔드 API |
|---|---|---|
| `/` | 메인 학습 허브 | `/api/chapters`, `/api/docs` |
| `/lab` | 주식 AI 실험실 | `/api/stock/analyze`, `/api/datasets/…/adapted/stock-lab` |
| `/predict` | 예측 실험실 | `/api/stock/predict-target`, `/api/stock/sample-csv` |
| `/hotel-stock` | 호텔-주가 실험실 | `/api/hotel-stock/train` |
| `/datasets` | 데이터셋 허브 | `/api/datasets`, `/api/datasets/{id}` |
| `/dart` | DART 공시 투자 파이프라인 | `/api/dart/overview`, `/api/dart/companies` |
| `/macro` | 거시경제 투자 파이프라인 | `/api/macro/overview`, `/api/macro/train` |
| `/advisor` | 이벤트 투자 컨설팅 | `/api/stock/news-consult` |

---

## API란 무엇인가요?

**API**는 "Application Programming Interface"의 줄임말입니다.  
어렵게 들리지만 아주 쉽게 말하면 **"주문서"** 또는 **"소통 창구"**입니다.

🍔 예시: 음식점 주문

```
손님(프론트엔드) → 주문서 작성(API 요청) → 주방(백엔드) → 음식 나옴(API 응답)
```

웹앱에서는 이렇게 됩니다.

```
화면 버튼 클릭 → /api/stock/analyze 요청 → 서버에서 AI 계산 → 결과 JSON 응답
```

### API 주소 읽는 법

```
GET  /api/chapters          ← 챕터 목록 가져오기 (GET = 조회)
POST /api/stock/analyze     ← 주가 분석 실행하기 (POST = 데이터 보내고 처리)
```

- **GET**: 정보를 가져올 때 씁니다. (예: 책 목록 보기)
- **POST**: 내가 데이터를 보내고 결과를 받을 때 씁니다. (예: 주문 넣기)

---

## 기능별 API 상세 설명

### 1. 시스템 상태 확인

**주소**: `GET /api/health`  
**화면**: 내부적으로 서버가 살아 있는지 확인할 때 씁니다.

```
요청 → /api/health
응답 → { "status": "ok", "version": "2.0.0" }
```

쉽게 말하면: "서버야, 살아 있어?" "네, 살아 있어요!" 를 주고받는 통신입니다.

---

### 2. 챕터 API - 학습 실습 코드 관리

**메인 학습 허브(/) 화면에서 씁니다.**

#### 챕터 목록 조회

**주소**: `GET /api/chapters`

```
요청 → /api/chapters
응답 → [
  { "id": "chapter05", "title": "로지스틱 회귀", "topic": "분류", ... },
  { "id": "chapter06", "title": "결정 트리",     "topic": "분류", ... },
  ...
]
```

백엔드가 하는 일:

1. `backend/app/chapters/` 폴더를 열어요
2. `chapter*` 이름 폴더를 전부 찾아요
3. 각 폴더의 `README.md`에서 제목을 읽어요
4. 각 폴더의 `practice.py`에서 설명과 메타 정보를 읽어요
5. 목록으로 만들어서 돌려줘요

#### 챕터 상세 조회

**주소**: `GET /api/chapters/{챕터ID}`  
예시: `/api/chapters/chapter06`

```
응답 → {
  "id": "chapter06",
  "title": "결정 트리",
  "readme": "# 결정 트리 설명...",
  "has_run": true
}
```

#### 챕터 실습 코드 실행 ⭐ 중요!

**주소**: `POST /api/chapters/{챕터ID}/run`

이 API가 **"실행" 버튼**이 눌릴 때 실제로 Python 코드를 돌리는 부분입니다.

```
요청 → POST /api/chapters/chapter06/run
       { "params": {} }

백엔드 처리 과정:
  1. chapter06/practice.py 파일을 읽어요
  2. Python의 exec() 함수로 코드를 실행해요
  3. practice.py 안의 run() 함수를 호출해요
  4. 걸린 시간과 결과를 정리해요

응답 → {
  "chapter": "chapter06",
  "topic": "결정 트리",
  "result": { "accuracy": 0.78, ... },
  "elapsed_ms": 342.5,
  "stdout": "훈련 완료!\n정확도: 78.2%\n"
}
```

🔑 **초등학생 설명**: 실행 버튼을 누르면 서버가 그 챕터의 Python 코드를 실제로 실행하고 결과를 알려줍니다. 마치 서버 안에 있는 컴퓨터가 대신 숙제를 해주는 것 같아요!

#### 챕터 소스 코드 보기

**주소**: `GET /api/chapters/{챕터ID}/source`

practice.py 파일의 내용을 글자로 그대로 보내줍니다.

---

### 3. 문서 API - 학습 문서 조회

**메인 학습 허브(/) 화면에서 씁니다.**

#### 문서 목록 조회

**주소**: `GET /api/docs`

```
응답 → [
  { "id": "01", "title": "Day 1. AI 지도 산책", "filename": "01.md" },
  { "id": "02", "title": "Day 2. 모델 기본기",  "filename": "02.md" },
  ...
]
```

백엔드가 하는 일: `docs/` 폴더 안의 숫자 이름 `.md` 파일을 순서대로 정리해 줘요.

#### 문서 내용 조회

**주소**: `GET /api/docs/{문서ID}`  
예시: `/api/docs/01`

```
응답 → {
  "id": "01",
  "title": "Day 1. AI 지도 산책",
  "content": "# Day 1. AI 지도 산책...(전체 내용)"
}
```

---

### 4. 데이터셋 API - CSV 데이터 관리

**데이터셋 허브(/datasets) 화면에서 씁니다.**

이 웹앱에는 미리 준비된 CSV 데이터 파일들이 있습니다.

| 데이터셋 ID | 이름 | 용도 |
|---|---|---|
| `stock_ohlcv` | 대표 종목 OHLCV 시계열 | 주식 AI 실험실 |
| `dart_fundamentals` | DART 재무제표 팩터 | DART 공시 파이프라인 |
| `dart_disclosures` | DART 최근 공시 타임라인 | DART 공시 파이프라인 |
| `macro_fred_signals` | FRED 거시 신호 | 거시경제 파이프라인 |
| `external_invest_ml_dataset` | 외부 데이터 기반 투자 학습셋 | 거시경제 ML 학습 |
| `stocks_features` | 주식 클러스터링 특성 | 군집화 실습 |
| `traffic_timeseries` | 섹터 ETF 시계열 | 시계열 실습 |

#### 데이터셋 목록 조회

**주소**: `GET /api/datasets`

```
응답 → [
  { "id": "stock_ohlcv", "title": "대표 종목 OHLCV 시계열", "rows": 250, ... },
  ...
]
```

#### 데이터셋 상세 조회

**주소**: `GET /api/datasets/{데이터셋ID}`

```
응답 → {
  "id": "stock_ohlcv",
  "columns": ["date", "open", "high", "low", "close", "volume"],
  "preview": [ { "date": "2024-01-02", "close": 74200, ... }, ... ],
  "chart_hint": "timeseries"
}
```

`chart_hint`는 이 데이터를 어떤 차트로 보면 좋은지 힌트를 줍니다.

- `timeseries`: 꺾은선 차트 (날짜 데이터)
- `scatter`: 산점도 (숫자 두 개 비교)
- `bar`: 막대 차트

#### 주식 AI 실험실용 데이터 변환

**주소**: `GET /api/datasets/{데이터셋ID}/adapted/stock-lab`

```
응답 → {
  "rows": [
    { "date": "2024-01-02", "open": 73800, "high": 74500, "low": 73600, "close": 74200, "volume": 12500000 },
    ...
  ]
}
```

데이터가 40행보다 적으면 자동으로 추가 데이터를 만들어서 채워줍니다.  
(캔들 차트와 내일 예측 점을 그릴 수 있을 정도의 양이 필요하거든요!)

---

### 5. 주식 AI 실험실 API

**주식 AI 실험실(/lab) 화면에서 씁니다.**

이 API가 이 웹앱에서 가장 중요한 부분입니다.  
주가 데이터를 받아서 AI가 "내일 오를까, 내릴까?"를 예측하고  
여러 가지 점수와 그래프 데이터를 돌려줍니다.

**주소**: `POST /api/stock/analyze`

#### 요청 형식

```json
{
  "rows": [
    { "date": "2024-01-02", "close": 74200, "volume": 12500000 },
    { "date": "2024-01-03", "close": 74800, "volume": 13200000 },
    ...
  ],
  "model": "rf"
}
```

모델 선택지:
| 코드 | 이름 | 초등학생 비유 |
|---|---|---|
| `logistic` | 로지스틱 회귀 | 선 하나 그어서 위아래 나누기 |
| `rf` | 랜덤 포레스트 | 여러 친구들이 투표해서 결정 |
| `nn` | 신경망 | 뇌처럼 여러 층에서 계산 |
| `gbm` | 그래디언트 부스팅 | 틀린 문제를 조금씩 고쳐가기 |

#### 백엔드가 하는 일 (단계별)

```
1단계: 데이터 정리
  - 날짜 순서대로 정렬
  - 빈 값 채우기 (고가, 저가, 시가 없으면 종가로 채움)

2단계: 특성(힌트) 7개 계산
  ① ret        = 오늘 수익률 (종가 변화 %)
  ② ret_5      = 5일 수익률
  ③ ma5_gap    = 5일 이동평균선과 얼마나 차이나는지
  ④ ma20_gap   = 20일 이동평균선과 얼마나 차이나는지
  ⑤ vol_ratio  = 오늘 거래량이 평소(10일 평균)의 몇 배인지
  ⑥ range_pct  = 오늘 고가-저가 범위 비율
  ⑦ body_pct   = 캔들 몸통 비율 (시가 대비 종가 변화)

3단계: 목표값(정답) 만들기
  - 내일 종가 > 오늘 종가 → 1 (상승)
  - 내일 종가 ≤ 오늘 종가 → 0 (하락)

4단계: 학습/테스트 분리
  - 앞 80% 데이터로 학습
  - 뒤 20% 데이터로 점수 측정

5단계: AI 모델 학습 및 예측

6단계: 점수 계산
  - accuracy  (정확도): 전체 중 몇 개 맞혔는지
  - AUC       : 상승/하락을 얼마나 잘 구분하는지
  - precision : "상승"이라고 했을 때 진짜 상승한 비율

7단계: 매매 시뮬레이션 (백테스트)
  - 상승 확률 55% 이상일 때만 매수 신호
  - 전략 수익률 vs 그냥 가지고 있는 수익률 비교

8단계: 종가 예측 (회귀 모델)
  - 내일 종가를 숫자로 예측
  - 최근 20일 변동성을 기준으로 너무 극단적인 값은 조정

9단계: 결과 전송
```

#### 응답 예시

```json
{
  "model_name": "랜덤 포레스트",
  "accuracy": 0.6842,
  "auc": 0.7231,
  "precision": 0.7100,
  "feature_importance": {
    "ret": 0.2341,
    "vol_ratio": 0.1923,
    "ma5_gap": 0.1734,
    ...
  },
  "portfolio": [1.0, 1.012, 0.998, 1.021, ...],
  "buyhold":   [1.0, 1.011, 1.002, 1.015, ...],
  "portfolio_return": 8.32,
  "buyhold_return": 6.41,
  "signals": [
    { "date": "2024-06-01", "close": 75400, "signal": "매수", "prob": 67.3, "actual": "상승", "correct": true },
    ...
  ],
  "predicted_next_close": 75800,
  "predicted_next_date": "2024-06-10",
  "predicted_move_pct": 0.53
}
```

🔑 **초등학생 설명**: 버튼을 누르면 서버가 주가 데이터를 받아 특성 7개를 계산하고, AI 모델을 훈련시켜 "내일 오를까?" 점수와 내일 예상 가격까지 알려줍니다!

#### 신경망 시각화 (nn 모델 전용)

`model: "nn"` 을 선택하면 응답에 `nn_viz` 가 추가됩니다.  
이 데이터로 뉴런이 어떻게 연결되어 있는지 그림으로 그릴 수 있어요.

---

### 6. 예측 실험실 API - CSV 업로드 분석

**예측 실험실(/predict) 화면에서 씁니다.**

내가 직접 만든 CSV 파일을 올려서 회사별로 분석받는 기능입니다.

#### 샘플 CSV 다운로드

**주소**: `GET /api/stock/sample-csv`

서버가 자동으로 샘플 CSV를 만들어서 내려보내줍니다.

샘플에는 이 3개 회사 데이터가 들어 있어요:
- 롯데호텔 (500거래일)
- 포스코A&C (500거래일)
- 현대자동차 (500거래일)

CSV 형식:
```csv
date,company,close,volume
2024-01-02,롯데호텔,13000,900000
2024-01-02,포스코A&C,18000,250000
2024-01-02,현대자동차,230000,1200000
...
```

#### CSV 파일 업로드 & 분석

**주소**: `POST /api/stock/predict-target`

**필수 열 4개**: `date`, `company`, `close`, `volume`

```
요청: CSV 파일 + 모델 선택

백엔드가 하는 일:
  1. CSV 파일을 읽어요
  2. 회사별로 데이터를 나눠요
  3. 회사마다 특성 10개를 계산해요:
     - f1_daily_return  : 일간 수익률
     - f2_return_5d     : 5일 수익률
     - f3_ma5_ratio     : MA5 비율
     - f4_ma20_ratio    : MA20 비율
     - f5_vol_ratio     : 거래량 비율
     - f6_rsi           : RSI (14일)
     - f7_volatility    : 변동성
     - f8_golden_cross  : 골든크로스 여부
     - f9_momentum_20d  : 20일 모멘텀
     - f10_vol_change   : 거래량 변화율
  4. 회사마다 AI 모델을 훈련하고 예측해요
  5. 회사별 결과를 하나로 모아 돌려줘요
```

응답:
```json
{
  "model_name": "랜덤 포레스트",
  "companies": {
    "롯데호텔": {
      "accuracy": 0.70,
      "auc": 0.75,
      "pred_prob": 62.3,
      "pred_label": "상승",
      "feature_importance": { "f6_rsi": 0.183, ... }
    },
    "포스코A&C": { ... },
    "현대자동차": { ... }
  }
}
```

---

### 7. DART 공시 투자 파이프라인 API

**DART 공시 투자 파이프라인(/dart) 화면에서 씁니다.**

DART는 한국 금융감독원에서 운영하는 공시 시스템입니다.  
회사가 공식으로 낸 성적표(재무제표)와 소식(공시)을 모아 볼 수 있어요.

> ⚠️ 이 API를 쓰려면 먼저 `DART_API_KEY`를 넣고  
> `scripts/refresh_datasets.py`를 실행해서 CSV를 만들어야 해요!

#### DART 전체 현황

**주소**: `GET /api/dart/overview`

```
응답 → {
  "company_count": 15,
  "top_companies": [
    { "corp_name": "삼성전자", "signal_score": 87.3, "investment_view": "긍정" },
    ...
  ]
}
```

#### 회사 목록 조회

**주소**: `GET /api/dart/companies`

투자 신호 점수(signal_score) 순서로 정렬된 회사 목록을 줍니다.

#### 특정 회사 상세 조회

**주소**: `GET /api/dart/companies/{종목코드}`  
예시: `/api/dart/companies/005930` (삼성전자)

```
응답 → {
  "company": {
    "corp_name": "삼성전자",
    "signal_score": 87.3,
    "investment_view": "긍정",
    "consultant_note": "매출이 전년보다 커졌어요. 영업이익도 함께 좋아지고 있어요.",
    "revenue_yoy": 12.3,      ← 매출 전년 대비 성장률
    "operating_margin": 14.2, ← 영업이익률
    "debt_ratio": 38.5        ← 부채비율
  },
  "fundamentals": [ ... 연도별 재무 숫자 ... ],
  "disclosures": [ ... 최근 공시 10개 ... ]
}
```

**초등학생 설명**: 삼성전자 성적표를 보는 것처럼, 회사가 얼마나 벌었는지, 빚은 얼마나 있는지, 최근에 어떤 소식이 있는지 한 번에 볼 수 있어요!

---

### 8. 거시경제 투자 파이프라인 API

**거시경제 투자 파이프라인(/macro) 화면에서 씁니다.**

FRED(미국 연방준비제도 경제 데이터)와 World Bank(세계은행)에서  
금리, 물가, 실업률, GDP 같은 큰 시장 신호를 가져옵니다.

#### 거시경제 현황 조회

**주소**: `GET /api/macro/overview`

```
응답 → {
  "latest_macro": {
    "fred_fedfunds": 5.33,  ← 미국 기준금리 (%)
    "fred_cpi_yoy": 3.2,    ← 미국 소비자물가 상승률
    "fred_vix": 18.5,       ← 공포 지수 (VIX)
    "wb_gdp_growth": 2.8    ← 한국 GDP 성장률
  },
  "recommendations": [
    { "name": "DART",       "implemented": true,  "key_required": true },
    { "name": "FRED",       "implemented": true,  "key_required": false },
    { "name": "World Bank", "implemented": true,  "key_required": false },
    { "name": "KOSIS",      "implemented": false, "key_required": true  }
  ]
}
```

#### 거시경제 ML 모델 학습

**주소**: `POST /api/macro/train`

DART 재무 데이터 + FRED 거시 신호 + World Bank 지표를 합쳐서  
"다음 해에 영업이익이 좋아질까?"를 3가지 모델로 예측해요.

사용하는 특성 19개:
- 회사 재무 (매출, 영업이익, ROE, 부채비율 등)
- FRED 거시 신호 (금리, CPI, 실업률, VIX, 유가 등)
- World Bank 지표 (GDP 성장률, 수출 비중 등)

```
응답 → {
  "results": [
    { "model": "logistic", "accuracy": 0.72, "auc": 0.78 },
    { "model": "rf",       "accuracy": 0.75, "auc": 0.81 },
    { "model": "nn",       "accuracy": 0.73, "auc": 0.79 }
  ],
  "best_model": { "model": "rf", "accuracy": 0.75 }
}
```

---

### 9. 뉴스 이벤트 컨설팅 API

**이벤트 투자 컨설팅(/advisor) 화면에서 씁니다.**

뉴스 한 문장을 넣으면 어떤 업종에 좋고 나쁜지 분석해줍니다.

**주소**: `POST /api/stock/news-consult`

#### 요청 형식

```json
{
  "message": "중동 전쟁이 확대되며 유가가 급등하고 있습니다",
  "market_scope": "krx",
  "horizon": "1m",
  "risk_profile": "neutral",
  "holdings": ["삼성전자", "방산"]
}
```

#### 백엔드가 하는 일 (뉴스 테마 감지)

서버 안에 미리 준비된 **테마 도서관**이 있어요.

| 테마 키 | 이름 | 예시 키워드 |
|---|---|---|
| `war` | 전쟁·군사 충돌 | 전쟁, 미사일, 중동 |
| `drought` | 가뭄·기후 충격 | 가뭄, 폭염, 엘니뇨 |
| `inflation` | 물가 급등 | CPI, 물가, 인플레이션 |
| `rate_cut` | 금리 인하 | 금리 인하, pivot |
| `tariff` | 관세·규제 충격 | 관세, 규제, 반도체 규제 |

뉴스가 들어오면:
1. 키워드가 몇 개 맞는지 세요
2. TF-IDF(텍스트 유사도 계산)로 점수를 구해요
3. 합산 점수가 높은 테마 2개를 골라요
4. 그 테마의 업종 영향과 체크포인트를 합쳐요

응답:
```json
{
  "detected_themes": ["전쟁·군사 충돌"],
  "sector_impacts": [
    { "sector": "방산",     "score": 2,  "direction": "positive" },
    { "sector": "반도체",   "score": -1, "direction": "negative" },
    { "sector": "항공·여행","score": -2, "direction": "negative" }
  ],
  "risk_score": 53,
  "consultant_note": "전쟁·군사 충돌 뉴스로 해석됩니다. 위험자산을 줄이고..."
}
```

---

### 10. 호텔-주가 실험실 API

**호텔-주가 실험실(/hotel-stock) 화면에서 씁니다.**

호텔 예약률 데이터와 주가를 같이 보는 특별한 실험실입니다.

**주소**: `POST /api/hotel-stock/train`

#### 요청 형식

```json
{
  "model": "rf",
  "n_samples": 1000,
  "test_size": 0.3
}
```

모델 선택지:
- ML 모델: `logistic`, `dt`, `rf`, `gbm`, `svm`, `knn`
- DL 모델: `mlp_1`, `mlp_2`, `mlp_3`, `mlp_deep`

#### 백엔드가 하는 일

```
1. 가상의 호텔 예약률 데이터 생성
   - 호텔 30개 × 1000개월치
   - 계절성 포함 (성수기 7·8·12·1월에 예약률 높음)
   - 예약률과 주가를 연결 (예약률 높을수록 주가 상승 경향)

2. 특성 묶음 만들기
   - 호텔 특성 30개 (각 호텔 예약률)
   - 계절 특성 4개 (월, 분기, 계절, 성수기 여부)
   - 가격 특성 7개 (이전 달 종가, 3개월 수익률, MA3, MA6 등)

3. 학습 · 테스트 분리 후 모델 훈련

4. 결과 계산
   - 분류 점수 (accuracy, AUC)
   - 혼동 행렬 (TP, FP, TN, FN)
   - 특성 중요도 상위 10개
   - 예측 신호 테이블

5. 계절성 분석
   - 월별 예약률 평균
   - 월별 상승 비율
```

혼동 행렬 설명:
| 용어 | 뜻 |
|---|---|
| TP (True Positive) | "상승"이라고 했고, 진짜 상승 |
| FP (False Positive) | "상승"이라고 했는데, 실제 하락 (틀림) |
| TN (True Negative) | "하락"이라고 했고, 진짜 하락 |
| FN (False Negative) | "하락"이라고 했는데, 실제 상승 (틀림) |

---

### 11. AI 어시스턴트 API

**여러 화면의 AI 도우미 기능에서 씁니다.**

#### 자연어 질문으로 화면 안내

**주소**: `POST /api/assistant/route`

```json
요청: { "message": "삼성전자 내일 살까 말까?" }

백엔드가 하는 일:
  1. 질문 유형을 판단해요
     - "살까/매수/팔까" 키워드 → 매수 판단 (lab으로)
     - "종가/가격/얼마" 키워드 → 종가 예측 (predict로)
     - "분석/패턴/신호" 키워드 → 분석 (lab으로)
     - "전쟁/금리/뉴스" 키워드 → 이벤트 (advisor로)
  2. Ollama LLM이 연결되어 있으면 AI가 더 정확히 판단
  3. LLM이 없으면 규칙 기반으로 판단

응답: {
  "intent": "trading_decision",
  "company": "삼성전자",
  "route_label": "주식 AI 실험실",
  "route": "/lab?assistant=trading_decision&company=삼성전자",
  "description": "삼성전자 종목을 살지 말지 판단하는 질문으로 이해했어요."
}
```

#### AI 채팅 설명 요청

**주소**: `POST /api/chat`

분석 결과가 나온 후 "왜 이런 결과가 나왔어?"라고 물으면 AI가 설명해줍니다.

```json
요청: {
  "message": "왜 상승 확률이 높아?",
  "context": {
    "model_name": "랜덤 포레스트",
    "accuracy": 0.68,
    "feature_importance": { "vol_ratio": 0.23, "ma5_gap": 0.19 }
  }
}

Ollama 연결 시 → 풍부한 AI 설명
Ollama 없을 때 → 규칙 기반 설명:
  "'거래량 비율'이 가장 큰 영향을 미쳤습니다.
   이 값이 높을 때 상승 확률이 높았어요."
```

---

## 데이터가 여행하는 길 (흐름도)

주식 AI 실험실에서 "AI 분석 시작!" 버튼을 눌렀을 때 무슨 일이 일어나는지 따라가 봐요.

```
[사용자가 버튼 클릭]
        │
        ▼
[브라우저(프론트엔드)]
 주가 데이터 + 모델 선택을
 JSON으로 만들어서 보냄
        │
        ▼  POST /api/stock/analyze
[FastAPI 서버(백엔드)]
 ① 데이터 수신 및 유효성 검사 (25행 이상인지 확인)
 ② OHLCV 데이터 정리 (빈 값 채우기)
 ③ 특성 7개 계산
    - 수익률, 이동평균 괴리, 거래량 비율 등
 ④ 정답(target) 만들기
    - 내일 상승=1, 하락=0
 ⑤ 학습/테스트 80:20 분리
 ⑥ StandardScaler로 숫자 범위 통일
 ⑦ 선택한 AI 모델 학습 (sklearn)
 ⑧ 테스트 데이터로 예측
 ⑨ 점수 계산 (accuracy, AUC, precision)
 ⑩ 매매 시뮬레이션 (포트폴리오 vs 보유 수익률)
 ⑪ 종가 예측 (회귀 모델)
 ⑫ 결과를 JSON으로 정리
        │
        ▼  JSON 응답
[브라우저(프론트엔드)]
 결과를 받아서 화면에 표시:
 - 점수 카드 (accuracy, AUC...)
 - 캔들 차트
 - 내일 예측 점
 - 포트폴리오 곡선
 - 매매 신호 표
```

---

## 주요 Python 라이브러리 소개

이 백엔드는 여러 Python 패키지를 사용합니다.  
각 패키지가 무슨 역할인지 쉽게 알아봐요.

| 패키지 | 역할 | 초등학생 비유 |
|---|---|---|
| **FastAPI** | 웹 서버 틀 | 음식점 건물 (주방과 홀을 연결) |
| **pandas** | 표(데이터프레임) 처리 | 엑셀 같은 것을 Python에서 다루는 도구 |
| **numpy** | 숫자 계산 | 빠른 수학 계산기 |
| **scikit-learn** | AI 모델 | 여러 종류의 AI 모델 상자 모음 |
| **httpx** | 외부 서버에 요청 | 다른 가게에 주문하는 전화 |
| **uvicorn** | FastAPI를 실제로 켜는 도구 | 음식점 문 열기 |

### scikit-learn 안의 모델들

```
sklearn.linear_model
  └─ LogisticRegression   (로지스틱 회귀)
  └─ Ridge                (릿지 회귀, 종가 예측용)

sklearn.ensemble
  └─ RandomForestClassifier   (랜덤 포레스트 분류)
  └─ RandomForestRegressor    (랜덤 포레스트 회귀)
  └─ GradientBoostingClassifier  (그래디언트 부스팅 분류)
  └─ GradientBoostingRegressor   (그래디언트 부스팅 회귀)

sklearn.neural_network
  └─ MLPClassifier   (다층 퍼셉트론 신경망 분류)
  └─ MLPRegressor    (다층 퍼셉트론 신경망 회귀)

sklearn.preprocessing
  └─ StandardScaler  (데이터 범위 통일)

sklearn.metrics
  └─ accuracy_score, roc_auc_score, precision_score  (점수 계산)
```

---

## 서버를 직접 켜는 방법

### 방법 1. Poetry 사용 (권장)

```bash
# 의존성 설치
poetry install

# 서버 시작
poetry run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8888
```

### 방법 2. pip 사용

```bash
# 가상 환경 만들기
python -m venv .venv
source .venv/bin/activate    # 윈도우: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 시작
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8888
```

서버가 켜지면:
- 웹 화면: `http://localhost:8888`
- API 문서: `http://localhost:8888/docs` (FastAPI 자동 문서)

### 환경 변수 설정 (선택)

| 환경 변수 | 기본값 | 설명 |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama AI 서버 주소 |
| `OLLAMA_MODEL` | `llama3.2` | 사용할 AI 언어 모델 이름 |
| `DART_API_KEY` | (없음) | DART 공시 데이터를 받기 위한 키 |
| `NEWS_THEME_BACKEND` | `tfidf` | 뉴스 테마 분석 방식 (`tfidf` 또는 `sentence-transformer`) |

---

## 정리: 버튼 하나가 켜는 여정

초등학생이 이해할 수 있는 가장 짧은 설명으로 마무리하면:

> 화면에서 "AI 분석 시작!" 버튼을 누르면  
> 웹 브라우저가 서버(백엔드)에 데이터를 보내고,  
> 서버는 Python 코드로 숫자를 계산하고 AI를 훈련시켜서  
> "내일 오를 확률은 67%입니다" 같은 결과를 돌려줍니다.  
> 그러면 화면이 그 결과를 예쁘게 표로, 그래프로 보여줍니다.

**뒷단(백엔드) = 보이지 않는 주방**  
**앞단(프론트엔드) = 손님이 보는 홀**  
**API = 주문서 창구**

이 세 가지가 함께 움직여서 여러분이 보는 AI 주식 예측 웹앱이 만들어집니다! 🎉

---

➡️ 학습 흐름을 처음부터 보고 싶다면 [Day 1 문서](01.md)로 이동하세요.  
➡️ 어려운 낱말을 찾아보고 싶다면 [용어 사전](voca.md)을 열어보세요.
