# 퀀트 특화 커리큘럼 매핑 (Chapter100~Chapter114)

이 문서는 기존 AI/ML 기초 99챕터 위에 **퀀트 금융 실습 트랙**을 추가한 매핑표입니다.

## Phase 1 - ML/DL 퀀트 기반 확장

- **Chapter100**: SVM으로 시장 상태 분류
- **Chapter101**: RNN 시계열 예측 기초
- **Chapter102**: LSTM 시계열 예측 기초
- **Chapter103**: Transformer 시계열 기초
- **Chapter84(개정)**: 주가 시계열 입문(이동평균/수익률/변동성)

## Phase 2 - 금융 도메인 지식

- **Chapter104**: 경제지표 데이터 수집과 해석 (금리/물가/유가 프록시)
- **Chapter105**: 재무제표 분석과 DCF 기초
- **Chapter106**: 기술적 분석 지표 확장 (RSI, MACD, 볼린저밴드, 캔들 타입)

## Phase 3 - 퀀트 모델링

- **Chapter107**: 백테스트 성과지표 구현 (MDD, Sharpe, Sortino)
- **Chapter108**: 포트폴리오 최적화 기초 (평균분산, Risk-Parity)
- **Chapter109**: 주식 클러스터링과 군집 해석

## Phase 4 - 실전 프로젝트

- **Chapter110**: 국내 주식 데이터 수집 기초 (FinanceDataReader/pykrx fallback)
- **Chapter111**: 네이버 금융 크롤링 기초 (BeautifulSoup)
- **Chapter112**: 주가 방향성 예측 미니 프로젝트
- **Chapter113**: 로보 어드바이저 미니 프로젝트
- **Chapter114**: 증권사 API 연동 개요 (KIS 스타일 주문 구조)

## 운영 가이드

1. 기본 학습자는 Chapter01~99를 먼저 수행합니다.
2. 퀀트 트랙 학습자는 Chapter84를 개정 버전으로 수행한 뒤 Chapter100~114를 순차 진행합니다.
3. 네트워크/외부 API 접근이 제한된 환경에서는 각 챕터의 fallback 데이터를 사용해 동일한 분석 흐름을 학습합니다.
