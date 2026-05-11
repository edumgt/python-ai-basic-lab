"""주가 예측 검증 전략"""
from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import TimeSeriesSplit

from stock_practice_utils import FEATURE_POOL, make_stock_feature_frame, time_split_frame

LESSON_10MIN = "주가 예측은 미래 데이터가 과거 학습에 섞이면 안 되므로 시간 순서를 지키는 검증이 중요하다."
PRACTICE_30MIN = "TimeSeriesSplit으로 주가 방향성 모델을 여러 구간에서 검증하고 마지막 홀드아웃 성능과 비교한다."


def run() -> dict:
    df = make_stock_feature_frame(seed=47, n=320, noise=0.019)
    features = FEATURE_POOL[2:8]
    x = df[features]
    y = df["target_up"]

    tscv = TimeSeriesSplit(n_splits=5)
    scores = []
    for train_idx, test_idx in tscv.split(x):
        model = LogisticRegression(max_iter=1000)
        model.fit(x.iloc[train_idx], y.iloc[train_idx])
        pred = model.predict(x.iloc[test_idx])
        scores.append(float(accuracy_score(y.iloc[test_idx], pred)))

    x_train, x_test, y_train, y_test = time_split_frame(df, features, "target_up", test_size=0.2)
    holdout_model = LogisticRegression(max_iter=1000)
    holdout_model.fit(x_train, y_train)
    holdout_pred = holdout_model.predict(x_test)

    return {
        "chapter": "chapter11",
        "topic": "주가 예측 검증 전략",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "cv_scores": [round(score, 4) for score in scores],
        "cv_mean": round(float(np.mean(scores)), 4),
        "cv_std": round(float(np.std(scores)), 4),
        "holdout_accuracy": round(float(accuracy_score(y_test, holdout_pred)), 4),
    }


if __name__ == "__main__":
    print(run())
