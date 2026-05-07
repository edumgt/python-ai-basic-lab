"""주가 시계열 입문 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd

LESSON_10MIN = "시계열 데이터는 시간 순서를 보존하고 추세와 변동성을 함께 관찰해야 한다."
PRACTICE_30MIN = "주가 종가 데이터로 이동평균과 일간 수익률을 계산한다."


def _load_close_prices() -> pd.DataFrame:
    try:
        import yfinance as yf  # type: ignore

        data = yf.download("^KS11", period="2mo", interval="1d", progress=False)
        if not data.empty and "Close" in data.columns:
            close = data[["Close"]].dropna().rename(columns={"Close": "close"}).reset_index()
            close.columns = ["date", "close"]
            close["date"] = pd.to_datetime(close["date"])
            return close.tail(40).reset_index(drop=True)
    except Exception:
        pass

    rng = np.random.default_rng(42)
    dates = pd.date_range("2026-01-01", periods=40, freq="B")
    drift = np.linspace(2400, 2550, num=40)
    noise = rng.normal(0, 18, size=40)
    close = np.maximum(1200, drift + noise)
    return pd.DataFrame({"date": dates, "close": close})


def run() -> dict:
    df = _load_close_prices().copy()
    df["ma_5"] = df["close"].rolling(window=5).mean()
    df["ma_20"] = df["close"].rolling(window=20).mean()
    df["daily_return"] = df["close"].pct_change()
    volatility_20 = float(df["daily_return"].rolling(20).std().iloc[-1])

    return {
        "chapter": "chapter84",
        "topic": "주가 시계열 입문",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "rows": int(len(df)),
        "latest_close": round(float(df["close"].iloc[-1]), 4),
        "latest_ma_5": round(float(df["ma_5"].iloc[-1]), 4),
        "latest_ma_20": round(float(df["ma_20"].iloc[-1]), 4),
        "latest_daily_return": round(float(df["daily_return"].iloc[-1]), 6),
        "volatility_20": round(volatility_20, 6),
        "preview": df.tail(7).round(4).astype(str).to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
