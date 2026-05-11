"""주가 방향성 예측 미니 프로젝트 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

LESSON_10MIN = "방향성 예측은 데이터 누수를 피하고 미래를 기준으로 평가해야 한다."
PRACTICE_30MIN = "수익률, 이동평균 괴리, 변동성으로 다음 날 상승 여부를 예측한다."


def run() -> dict:
    rng = np.random.default_rng(42)
    n = 260
    base = np.cumsum(rng.normal(0.0006, 0.012, n)) + 100
    df = pd.DataFrame({"close": base})
    df["ret_1d"] = df["close"].pct_change()
    df["ret_5d"] = df["close"].pct_change(5)
    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_20"] = df["close"].rolling(20).mean()
    df["ma_gap"] = df["ma_5"] / df["ma_20"] - 1
    df["vol_10"] = df["ret_1d"].rolling(10).std()
    df["target"] = (df["ret_1d"].shift(-1) > 0).astype(int)
    df = df.dropna().reset_index(drop=True)

    X = df[["ret_1d", "ret_5d", "ma_gap", "vol_10"]]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, shuffle=False
    )

    model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    return {
        "chapter": "chapter112",
        "topic": "주가 방향성 예측 미니 프로젝트",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "feature_importance": {
            name: round(float(score), 4)
            for name, score in zip(X.columns, model.feature_importances_)
        },
    }


if __name__ == "__main__":
    print(run())
