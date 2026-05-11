"""기술적 지표로 다음 날 주가 방향 예측"""
from __future__ import annotations

import numpy as np
import pandas as pd

LESSON_10MIN = "기술적 지표는 다음 날 주가 방향 예측에 쓸 수 있는 가격·거래량 기반 신호를 숫자로 바꾼 것이다."
PRACTICE_30MIN = "RSI, MACD, 볼린저밴드를 계산하고 종합 점수로 다음 날 방향 신호를 만든다."


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    diff = close.diff()
    up = diff.clip(lower=0)
    down = -diff.clip(upper=0)
    avg_gain = up.rolling(period).mean()
    avg_loss = down.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def run() -> dict:
    df = pd.read_csv("data/stock_ohlcv.csv", parse_dates=["date"])
    df["rsi_14"] = _rsi(df["close"])
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    ma20 = df["close"].rolling(20).mean()
    std20 = df["close"].rolling(20).std()
    df["bb_upper"] = ma20 + 2 * std20
    df["bb_lower"] = ma20 - 2 * std20
    df = df.dropna().reset_index(drop=True)

    latest = df.iloc[-1]
    score = (
        (1 if latest["rsi_14"] < 70 else -1)
        + (1 if latest["macd"] > latest["macd_signal"] else -1)
        + (1 if latest["close"] > latest["bb_lower"] else -1)
    ) / 3

    return {
        "chapter": "chapter106",
        "topic": "기술적 지표로 다음 날 주가 방향 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "latest_rsi_14": round(float(latest["rsi_14"]), 4),
        "latest_macd": round(float(latest["macd"]), 4),
        "latest_macd_signal": round(float(latest["macd_signal"]), 4),
        "latest_close": round(float(latest["close"]), 4),
        "technical_prediction_score": round(float(score), 4),
        "predicted_direction": "up" if score >= 0 else "down",
    }


if __name__ == "__main__":
    print(run())
