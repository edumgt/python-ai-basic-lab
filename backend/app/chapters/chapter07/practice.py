"""의사결정트리로 주가 방향성 예측"""
from __future__ import annotations

from sklearn.metrics import accuracy_score, f1_score
from sklearn.tree import DecisionTreeClassifier

from stock_practice_utils import FEATURE_POOL, make_stock_feature_frame, time_split_frame, top_items

LESSON_10MIN = "의사결정트리는 '이동평균 괴리가 크면?', '거래량이 급증하면?' 같은 규칙으로 다음 날 방향을 나눈다."
PRACTICE_30MIN = "주가 특성으로 결정트리를 학습해 분기 깊이와 중요 특성을 확인한다."


def run() -> dict:
    df = make_stock_feature_frame(seed=43, n=280, noise=0.019)
    features = FEATURE_POOL[2:]
    x_train, x_test, y_train, y_test = time_split_frame(df, features, "target_up", test_size=0.25)

    model = DecisionTreeClassifier(max_depth=4, min_samples_leaf=8, random_state=42)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)

    importance = {name: float(score) for name, score in zip(features, model.feature_importances_)}
    return {
        "chapter": "chapter07",
        "topic": "의사결정트리로 주가 방향성 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "tree_depth": int(model.get_depth()),
        "leaf_count": int(model.get_n_leaves()),
        "top_feature_importance": top_items(importance, limit=5),
    }


if __name__ == "__main__":
    print(run())
