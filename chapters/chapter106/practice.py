"""기술적 분석 지표 확장 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd

LESSON_10MIN = "기술적 분석은 가격 움직임을 규칙화해 진입/청산 판단에 활용한다."
PRACTICE_30MIN = "RSI, MACD, 볼린저밴드를 계산하고 캔들 패턴을 요약한다."


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    diff = close.diff()
    up = diff.clip(lower=0)
    down = -diff.clip(upper=0)
    avg_gain = up.rolling(period).mean()
    avg_loss = down.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def run() -> dict:
    close = pd.Series(
        [100, 102, 101, 103, 106, 104, 107, 109, 108, 111, 113, 112, 114, 116, 117, 115, 118, 121, 122, 124],
        dtype=float,
    )
    dates = pd.date_range("2026-01-01", periods=len(close), freq="B")
    open_ = close.shift(1).fillna(close.iloc[0] - 1)
    high = np.maximum(open_, close) + 1.2
    low = np.minimum(open_, close) - 1.1

    df = pd.DataFrame({"date": dates, "open": open_, "high": high, "low": low, "close": close})

    df["rsi_14"] = _rsi(df["close"])
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    ma20 = df["close"].rolling(20).mean()
    std20 = df["close"].rolling(20).std()
    df["bb_upper"] = ma20 + 2 * std20
    df["bb_lower"] = ma20 - 2 * std20

    df["candle_type"] = np.where(df["close"] >= df["open"], "bullish", "bearish")
    preview_df = df.tail(6).copy()
    preview_df["date"] = preview_df["date"].astype(str)
    numeric_cols = preview_df.select_dtypes(include=["number"]).columns
    preview_df[numeric_cols] = preview_df[numeric_cols].round(4)

    return {
        "chapter": "chapter106",
        "topic": "기술적 분석 지표 확장",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "latest_rsi_14": round(float(df["rsi_14"].iloc[-1]), 4),
        "latest_macd": round(float(df["macd"].iloc[-1]), 4),
        "latest_macd_signal": round(float(df["macd_signal"].iloc[-1]), 4),
        "latest_bb_upper": round(float(df["bb_upper"].iloc[-1]), 4),
        "latest_bb_lower": round(float(df["bb_lower"].iloc[-1]), 4),
        "bullish_count": int((df["candle_type"] == "bullish").sum()),
        "bearish_count": int((df["candle_type"] == "bearish").sum()),
        "preview": preview_df.astype(str).to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
