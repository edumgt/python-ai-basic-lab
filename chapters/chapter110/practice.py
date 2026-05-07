"""국내 주식 데이터 수집 기초 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd

LESSON_10MIN = "국내 주식 데이터는 소스별 심볼과 컬럼 구조 차이를 먼저 확인해야 한다."
PRACTICE_30MIN = "KOSPI 종목의 날짜별 종가 데이터를 읽어 기초 요약을 만든다."


def _fallback() -> pd.DataFrame:
    dates = pd.date_range("2026-03-01", periods=15, freq="B")
    price = np.linspace(71000, 74800, len(dates)) + np.sin(np.arange(len(dates))) * 350
    return pd.DataFrame({"date": dates, "close": price})


def run() -> dict:
    source = "fallback"
    df = _fallback()

    try:
        import FinanceDataReader as fdr  # type: ignore

        live = fdr.DataReader("005930", "2026-01-01")
        if not live.empty and "Close" in live.columns:
            df = live[["Close"]].rename(columns={"Close": "close"}).reset_index()
            df.columns = ["date", "close"]
            df = df.tail(30)
            source = "FinanceDataReader"
    except Exception:
        try:
            from pykrx import stock  # type: ignore

            live = stock.get_market_ohlcv("20260101", "20260501", "005930")
            if not live.empty and "종가" in live.columns:
                df = live[["종가"]].rename(columns={"종가": "close"}).reset_index()
                df.columns = ["date", "close"]
                df = df.tail(30)
                source = "pykrx"
        except Exception:
            pass

    df["ret_1d"] = df["close"].pct_change()

    return {
        "chapter": "chapter110",
        "topic": "국내 주식 데이터 수집 기초",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "data_source": source,
        "rows": int(len(df)),
        "latest_close": round(float(df["close"].iloc[-1]), 4),
        "mean_daily_return": round(float(df["ret_1d"].mean()), 6),
        "preview": df.tail(6).round(4).astype(str).to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
