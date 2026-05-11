"""SVM으로 주가 방향성 예측"""
from __future__ import annotations

from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from stock_practice_utils import FEATURE_POOL, make_stock_feature_frame, time_split_frame

LESSON_10MIN = "SVM은 상승/하락 샘플 사이 경계를 가장 넓게 벌려 주가 방향성 분류를 안정적으로 만들려 한다."
PRACTICE_30MIN = "수익률·변동성·이동평균 특성으로 다음 날 주가 방향을 분류한다."


def run() -> dict:
    df = make_stock_feature_frame(seed=49, n=320, noise=0.018)
    features = FEATURE_POOL[2:8]
    x_train, x_test, y_train, y_test = time_split_frame(df, features, "target_up", test_size=0.25)

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("svc", SVC(kernel="rbf", C=3.0, gamma="scale", random_state=42)),
        ]
    )
    model.fit(x_train, y_train)
    pred = model.predict(x_test)

    return {
        "chapter": "chapter100",
        "topic": "SVM으로 주가 방향성 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
    }


if __name__ == "__main__":
    print(run())
