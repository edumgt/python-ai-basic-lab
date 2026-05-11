"""주가 예측용 국내 주식 데이터 준비"""
from __future__ import annotations

import numpy as np
import pandas as pd

from stock_practice_utils import preview_records

LESSON_10MIN = "주가 예측은 먼저 날짜별 종가 데이터를 모으고 수익률·이동평균 같은 입력 특성으로 바꿔야 시작할 수 있다."
PRACTICE_30MIN = "국내 주식 종가를 읽어 예측용 입력 컬럼을 만들고 마지막 구간을 점검한다."


def _fallback() -> pd.DataFrame:
    dates = pd.date_range("2026-03-01", periods=40, freq="B")
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
            df = df.tail(60)
            source = "FinanceDataReader"
    except Exception:
        pass

    df["ret_1d"] = df["close"].pct_change()
    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_20"] = df["close"].rolling(20).mean()
    df["target_up"] = (df["close"].shift(-1) > df["close"]).astype(int)
    df = df.dropna().reset_index(drop=True)

    return {
        "chapter": "chapter110",
        "topic": "주가 예측용 국내 주식 데이터 준비",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "data_source": source,
        "rows": int(len(df)),
        "latest_close": round(float(df["close"].iloc[-1]), 4),
        "latest_target_up": "up" if int(df["target_up"].iloc[-1]) == 1 else "down",
        "feature_preview": preview_records(df, ["date", "close", "ret_1d", "ma_5", "ma_20", "target_up"], tail=6),
    }


if __name__ == "__main__":
    print(run())
