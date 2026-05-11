"""로지스틱 회귀로 주가 방향성 예측"""
from __future__ import annotations

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

from stock_practice_utils import FEATURE_POOL, make_stock_feature_frame, time_split_frame, top_items

LESSON_10MIN = "로지스틱 회귀는 주가가 내일 오를 확률을 0~1 사이 값으로 예측하는 가장 기본적인 분류 모델이다."
PRACTICE_30MIN = "가격·거래량 기반 특성으로 다음 거래일 상승 여부를 예측하고 정확도·AUC·계수를 읽는다."


def run() -> dict:
    df = make_stock_feature_frame(seed=42, n=280, noise=0.017)
    features = FEATURE_POOL[2:8]
    x_train, x_test, y_train, y_test = time_split_frame(df, features, "target_up", test_size=0.25)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    prob = model.predict_proba(x_test)[:, 1]

    coef_map = {name: float(value) for name, value in zip(features, model.coef_[0])}
    latest_prob = float(prob[-1])

    return {
        "chapter": "chapter06",
        "topic": "로지스틱 회귀로 주가 방향성 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision": round(float(precision_score(y_test, pred)), 4),
        "recall": round(float(recall_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
        "latest_up_probability": round(latest_prob, 4),
        "latest_signal": "up" if latest_prob >= 0.5 else "down",
        "top_coefficients": top_items(coef_map, limit=5),
    }


if __name__ == "__main__":
    print(run())
