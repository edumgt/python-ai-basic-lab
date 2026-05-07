"""주식 클러스터링과 군집 해석 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

LESSON_10MIN = "군집화는 정답 없이 구조를 파악해 유사 종목군을 찾는 방법이다."
PRACTICE_30MIN = "종목 특징을 표준화하고 K-Means로 군집을 구성해 해석한다."


def run() -> dict:
    stocks = pd.DataFrame(
        {
            "ticker": ["A", "B", "C", "D", "E", "F", "G", "H"],
            "annual_return": [0.18, 0.16, 0.05, 0.04, 0.11, 0.09, 0.03, 0.15],
            "volatility": [0.28, 0.25, 0.12, 0.10, 0.2, 0.16, 0.09, 0.24],
            "per": [26, 24, 12, 10, 18, 15, 9, 23],
        }
    )

    features = stocks[["annual_return", "volatility", "per"]]
    X = StandardScaler().fit_transform(features)
    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    stocks["cluster"] = model.fit_predict(X)

    summary = (
        stocks.groupby("cluster")[["annual_return", "volatility", "per"]]
        .mean()
        .round(4)
        .astype(float)
        .to_dict(orient="index")
    )

    return {
        "chapter": "chapter109",
        "topic": "주식 클러스터링과 군집 해석",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "cluster_summary": summary,
        "assignments": stocks[["ticker", "cluster"]].to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
