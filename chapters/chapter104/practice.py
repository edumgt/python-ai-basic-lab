"""경제지표 데이터 수집과 해석 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd

LESSON_10MIN = "매크로 지표는 투자 의사결정의 큰 방향을 정하는 신호다."
PRACTICE_30MIN = "금리/물가/유가 지표를 수집해 최근 변화율을 비교한다."


def _fallback_data() -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", periods=12, freq="ME")
    return pd.DataFrame(
        {
            "date": dates,
            "rate_proxy": np.linspace(3.1, 3.6, len(dates)),
            "inflation_proxy": np.linspace(2.0, 2.4, len(dates)) + np.sin(np.arange(len(dates)) / 3) * 0.06,
            "oil_proxy": np.linspace(72, 79, len(dates)) + np.cos(np.arange(len(dates)) / 4) * 1.5,
        }
    )


def run() -> dict:
    source = "fallback"
    df = _fallback_data()

    try:
        import yfinance as yf  # type: ignore

        tickers = {
            "rate_proxy": "^TNX",
            "inflation_proxy": "TIP",
            "oil_proxy": "CL=F",
        }
        frames = []
        for col, ticker in tickers.items():
            data = yf.download(ticker, period="1y", interval="1mo", progress=False)
            if data.empty or "Close" not in data.columns:
                raise ValueError("insufficient data")
            s = data["Close"].dropna().rename(col)
            frames.append(s)
        joined = pd.concat(frames, axis=1).dropna().reset_index()
        joined.columns = ["date", *tickers.keys()]
        if len(joined) >= 6:
            df = joined.tail(12).copy()
            source = "yfinance"
    except Exception:
        pass

    latest = df.iloc[-1]
    prev = df.iloc[-2]
    changes = {
        k: round(float((latest[k] - prev[k]) / prev[k]), 6)
        for k in ["rate_proxy", "inflation_proxy", "oil_proxy"]
    }

    return {
        "chapter": "chapter104",
        "topic": "경제지표 데이터 수집과 해석",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "data_source": source,
        "rows": int(len(df)),
        "mom_changes": changes,
        "preview": df.tail(5).round(4).astype(str).to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
