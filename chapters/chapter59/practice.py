# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""앙상블 개념 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: RandomForestClassifier, VotingClassifier를(을) 랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: DecisionTreeClassifier를(을) 결정 트리 모델 도구를 불러와요.
from sklearn.tree import DecisionTreeClassifier


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "여러 모델을 결합하면 단일 모델보다 안정적인 예측을 얻을 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "개별 모델과 Voting 앙상블 성능을 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=320,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=10,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=6,
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

    # 설명: 로지스틱 회귀 분류 모델을 생성해요.
    lr = LogisticRegression(max_iter=500, random_state=42)
    # 설명: 결정 트리 분류 모델을 생성해요.
    dt = DecisionTreeClassifier(max_depth=5, random_state=42)
    # 설명: 여러 결정 트리를 앙상블한 랜덤 포레스트 분류 모델을 생성해요.
    rf = RandomForestClassifier(n_estimators=140, random_state=42)

    # 설명: 'voting' 변수에 값을 계산해서 저장해요.
    voting = VotingClassifier(
        # 설명: 'estimators' 변수에 값을 계산해서 저장해요.
        estimators=[("lr", lr), ("dt", dt), ("rf", rf)],
        # 설명: 'voting' 변수에 값을 계산해서 저장해요.
        voting="hard",
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'models' 변수에 값을 계산해서 저장해요.
    models = {
        # 설명: 이 코드를 실행해요.
        "logistic_regression": lr,
        # 설명: 이 코드를 실행해요.
        "decision_tree": dt,
        # 설명: 이 코드를 실행해요.
        "random_forest": rf,
        # 설명: 이 코드를 실행해요.
        "voting_ensemble": voting,
    # 설명: 이 코드를 실행해요.
    }

    # 설명: 'scores: dict[str, float]' 변수에 값을 계산해서 저장해요.
    scores: dict[str, float] = {}
    # 설명: 각 원소를 순서대로 꺼내며 반복해요.
    for name, model in models.items():
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        model.fit(X_train, y_train)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = model.predict(X_test)
        # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
        scores[name] = round(float(accuracy_score(y_test, pred)), 4)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter59",
        # 설명: 이 코드를 실행해요.
        "topic": "앙상블 개념",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "accuracy": scores,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
