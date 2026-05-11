# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""Grid Search 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: GridSearchCV, train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import GridSearchCV, train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "Grid Search는 정해 둔 후보를 전부 시도해 최적값을 찾는다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "C와 penalty 조합을 탐색해 최적 분류기를 찾는다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=320,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=12,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=7,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=2,
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=42,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.25, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = LogisticRegression(max_iter=500, solver="liblinear", random_state=42)
    # 설명: 'param_grid' 변수에 값을 계산해서 저장해요.
    param_grid = {
        # 설명: 이 코드를 실행해요.
        "C": [0.1, 1.0, 3.0, 10.0],
        # 설명: 이 코드를 실행해요.
        "penalty": ["l1", "l2"],
    # 설명: 이 코드를 실행해요.
    }

    # 설명: 'search' 변수에 값을 계산해서 저장해요.
    search = GridSearchCV(model, param_grid=param_grid, cv=4, scoring="accuracy", n_jobs=None)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    search.fit(X_train, y_train)

    # 설명: 학습된 모델의 성능 점수(기본: 정확도/R²)를 계산해요.
    test_score = float(search.score(X_test, y_test))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter57",
        # 설명: 이 코드를 실행해요.
        "topic": "Grid Search",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "best_params": search.best_params_,
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "best_cv_score": round(float(search.best_score_), 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "test_accuracy": round(test_score, 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
