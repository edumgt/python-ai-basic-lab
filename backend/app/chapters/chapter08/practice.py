"""랜덤포레스트로 주가 방향성 예측"""
from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from stock_practice_utils import FEATURE_POOL, make_stock_feature_frame, time_split_frame, top_items

LESSON_10MIN = "랜덤포레스트는 여러 트리의 투표로 다음 날 상승 확률을 더 안정적으로 계산한다."
PRACTICE_30MIN = "가격·거래량 특성으로 랜덤포레스트를 학습해 F1, AUC, 특성 중요도를 비교한다."


def run() -> dict:
    df = make_stock_feature_frame(seed=44, n=320, noise=0.02)
    features = FEATURE_POOL
    x_train, x_test, y_train, y_test = time_split_frame(df, features, "target_up", test_size=0.25)

    model = RandomForestClassifier(n_estimators=220, max_depth=6, min_samples_leaf=6, random_state=42)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    prob = model.predict_proba(x_test)[:, 1]

    importance = {name: float(score) for name, score in zip(features, model.feature_importances_)}
    return {
        "chapter": "chapter08",
        "topic": "랜덤포레스트로 주가 방향성 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
        "latest_up_probability": round(float(prob[-1]), 4),
        "feature_importance": top_items(importance, limit=6),
    }


if __name__ == "__main__":
    print(run())
