"""주가 방향성 예측 평가 지표"""
from __future__ import annotations

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score

from stock_practice_utils import FEATURE_POOL, make_stock_feature_frame, time_split_frame

LESSON_10MIN = "주가 예측에서는 accuracy 하나보다 precision, recall, AUC를 함께 봐야 신호 품질을 더 잘 읽을 수 있다."
PRACTICE_30MIN = "로지스틱 회귀로 다음 날 상승 여부를 예측하고 주요 평가 지표를 한 번에 비교한다."


def run() -> dict:
    df = make_stock_feature_frame(seed=46, n=300, noise=0.018)
    features = FEATURE_POOL[2:8]
    x_train, x_test, y_train, y_test = time_split_frame(df, features, "target_up", test_size=0.25)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    prob = model.predict_proba(x_test)[:, 1]

    return {
        "chapter": "chapter10",
        "topic": "주가 방향성 예측 평가 지표",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision": round(float(precision_score(y_test, pred)), 4),
        "recall": round(float(recall_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
        "positive_signal_ratio": round(float(pred.mean()), 4),
    }


if __name__ == "__main__":
    print(run())
