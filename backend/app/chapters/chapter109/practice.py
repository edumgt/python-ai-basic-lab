"""주가 예측용 종목 군집 해석"""
from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

LESSON_10MIN = "비슷한 수익률·변동성 종목을 묶으면 같은 예측 모델을 적용할 종목군을 찾는 데 도움이 된다."
PRACTICE_30MIN = "종목 특징을 군집화하고 군집별 평균 수익률/변동성으로 예측 성격을 해석한다."


def run() -> dict:
    stocks = pd.read_csv("data/stocks_features.csv")
    features = stocks[["annual_return", "volatility", "per"]]
    scaled = StandardScaler().fit_transform(features)
    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    stocks["cluster"] = model.fit_predict(scaled)

    summary = (
        stocks.groupby("cluster")[["annual_return", "volatility", "per"]]
        .mean()
        .round(4)
        .to_dict(orient="index")
    )

    return {
        "chapter": "chapter109",
        "topic": "주가 예측용 종목 군집 해석",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "cluster_summary": summary,
        "assignments": stocks[["ticker", "cluster"]].to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
