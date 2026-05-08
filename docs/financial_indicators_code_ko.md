# 금융 지표 수식 ↔ Python 코드 매핑

아래 표는 퀀트 실습에서 자주 쓰는 지표를 수식 직관과 Python 코드 형태로 연결합니다.

## 1) 수익률/리스크 지표

| 지표 | 수식(요약) | Python 예시(요약) |
|---|---|---|
| 일간 수익률 | `r_t = P_t / P_{t-1} - 1` | `ret = close.pct_change()` |
| 누적 수익률 | `∏(1+r_t)-1` | `cum = (1+ret).cumprod()-1` |
| 최대낙폭(MDD) | `min(E_t / max(E_{1..t}) - 1)` | `dd = equity/equity.cummax()-1; mdd=dd.min()` |
| Sharpe Ratio | `mean(r)/std(r) * sqrt(252)` | `sharpe = ret.mean()/ret.std()*np.sqrt(252)` |
| Sortino Ratio | `mean(r)/std(r<0) * sqrt(252)` | `sortino = ret.mean()/downside_std*np.sqrt(252)` |

## 2) 기술적 지표

| 지표 | 수식(요약) | Python 예시(요약) |
|---|---|---|
| 이동평균(MA) | `MA_n = (1/n) Σ P_{t-i}` | `ma = close.rolling(n).mean()` |
| RSI | `100 - 100/(1+RS)` | `rsi = 100 - 100/(1+avg_gain/avg_loss)` |
| MACD | `EMA(12)-EMA(26)` | `macd = ema12 - ema26` |
| 볼린저밴드 | `MA ± 2σ` | `upper = ma20 + 2*std20` |

## 3) 포트폴리오 지표

| 항목 | 수식(요약) | Python 예시(요약) |
|---|---|---|
| 기대수익률 | `w^T μ` | `port_ret = w @ mu` |
| 변동성 | `sqrt(w^T Σ w)` | `port_vol = np.sqrt(w @ cov @ w)` |
| 리스크 패리티(단순) | `w_i ∝ 1/σ_i` | `w = (1/vol); w/=w.sum()` |

## PineScript ↔ Python 동등 코드 대조표

| PineScript 개념 | PineScript 예시 | Python 동등 코드 |
|---|---|---|
| 이동평균 | `ma = ta.sma(close, 20)` | `ma = close.rolling(20).mean()` |
| RSI | `rsi = ta.rsi(close, 14)` | `rsi = rsi_func(close, 14)` |
| MACD | `[m,s,h] = ta.macd(close,12,26,9)` | `macd=ema12-ema26; signal=macd.ewm(span=9).mean()` |
| 골든크로스 진입 | `longCond = ta.crossover(ma5, ma20)` | `long_cond = (ma5.shift(1)<=ma20.shift(1)) & (ma5>ma20)` |
| 전략 진입 | `strategy.entry("L", strategy.long)` | `if long_cond.iloc[-1]: signal="buy"` |

## 참고

- PineScript는 TradingView 실행 환경이 필요하며 이 저장소에서는 Python으로 동일 개념을 재현합니다.
- 지표 계산 시 결측치 초기 구간(`rolling` 윈도우 이전)을 반드시 처리해야 합니다.
