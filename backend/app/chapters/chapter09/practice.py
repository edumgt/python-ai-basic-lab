"""주가 예측용 시장 국면 군집화"""
from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from stock_practice_utils import make_stock_feature_frame, preview_records

LESSON_10MIN = "군집화는 상승/하락 정답 대신 비슷한 가격 움직임을 묶어 주가 예측 전에 시장 국면을 나누는 데 쓸 수 있다."
PRACTICE_30MIN = "수익률·변동성·거래량 비율로 시장 국면을 3개 군집으로 나누고 군집별 상승 확률을 본다."


def run() -> dict:
    df = make_stock_feature_frame(seed=45, n=280, noise=0.02)
    features = ["ret_1d", "ret_5d", "vol_10", "vol_ratio", "ma_gap"]
    scaled = StandardScaler().fit_transform(df[features])
    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["regime"] = model.fit_predict(scaled)

    summary = (
        df.groupby("regime")[features + ["target_up"]]
        .mean()
        .round(4)
        .rename(columns={"target_up": "up_rate"})
        .to_dict(orient="index")
    )

    preview_df = df[["date", "close", "ret_1d", "vol_ratio", "regime", "target_up"]].copy()
    preview_df["target_up"] = preview_df["target_up"].map({0: "down", 1: "up"})

    return {
        "chapter": "chapter09",
        "topic": "주가 예측용 시장 국면 군집화",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "cluster_count": 3,
        "regime_summary": summary,
        "preview": preview_records(preview_df, ["date", "close", "ret_1d", "vol_ratio", "regime", "target_up"], tail=6),
    }


if __name__ == "__main__":
    print(run())
