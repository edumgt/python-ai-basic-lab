"""SVM으로 시장 상태 분류 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

LESSON_10MIN = "SVM은 클래스 사이 마진을 크게 만드는 경계를 학습한다."
PRACTICE_30MIN = "수익률과 변동성으로 시장 국면(상승/하락)을 분류한다."


def run() -> dict:
    rng = np.random.default_rng(42)
    n = 320
    ret_5d = rng.normal(0.002, 0.015, n)
    vol_20d = rng.normal(0.018, 0.006, n).clip(0.004, None)
    trend = rng.normal(0.0, 1.0, n)

    score = 3.2 * ret_5d - 1.1 * vol_20d + 0.12 * trend + rng.normal(0, 0.02, n)
    y = (score > np.median(score)).astype(int)
    X = pd.DataFrame({"ret_5d": ret_5d, "vol_20d": vol_20d, "trend": trend})

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("svc", SVC(kernel="rbf", C=3.0, gamma="scale", random_state=42)),
        ]
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    return {
        "chapter": "chapter100",
        "topic": "SVM으로 시장 상태 분류",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
    }


if __name__ == "__main__":
    print(run())
