"""경제지표로 주가 예측 보조 신호 만들기"""
from __future__ import annotations

import numpy as np
import pandas as pd

LESSON_10MIN = "금리·물가·유가 변화는 다음 달 주식 시장 수익률을 예측할 때 쓰는 거시 환경 신호가 된다."
PRACTICE_30MIN = "매크로 변화율로 다음 달 주가 예측 점수를 만들고 상승/하락 환경을 해석한다."


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
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    changes = {
        k: float((latest[k] - prev[k]) / prev[k])
        for k in ["rate_proxy", "inflation_proxy", "oil_proxy"]
    }
    predicted_monthly_return = 0.04 * changes["inflation_proxy"] - 0.06 * changes["rate_proxy"] - 0.03 * changes["oil_proxy"]

    preview_df = df.tail(5).copy()
    preview_df["date"] = preview_df["date"].astype(str)
    preview_df[["rate_proxy", "inflation_proxy", "oil_proxy"]] = preview_df[["rate_proxy", "inflation_proxy", "oil_proxy"]].round(4)

    return {
        "chapter": "chapter104",
        "topic": "경제지표로 주가 예측 보조 신호 만들기",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "data_source": source,
        "mom_changes": {k: round(v, 6) for k, v in changes.items()},
        "predicted_next_month_return": round(float(predicted_monthly_return), 6),
        "predicted_market_environment": "bullish" if predicted_monthly_return >= 0 else "bearish",
        "preview": preview_df.to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
