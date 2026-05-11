# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""클래스 불균형 처리 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: f1_score, precision_score, recall_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import f1_score, precision_score, recall_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "불균형 데이터에서는 class_weight 등 보정 기법이 필요할 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "기본 모델과 class_weight=balanced 모델을 비교한다."


# 설명: '_scores' 함수를 정의해요.
def _scores(y_true, y_pred) -> dict[str, float]:
    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 양성으로 예측한 것 중 실제 양성 비율(정밀도)을 계산해요.
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        # 설명: 실제 양성 중 양성으로 예측한 비율(재현율)을 계산해요.
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        # 설명: 정밀도와 재현율의 조화평균인 F1 점수를 계산해요.
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=500,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=12,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=6,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=2,
        # 설명: 'weights' 변수에 값을 계산해서 저장해요.
        weights=[0.93, 0.07],
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=42,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.3, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 로지스틱 회귀 분류 모델을 생성해요.
    base = LogisticRegression(max_iter=500, random_state=42)
    # 설명: 로지스틱 회귀 분류 모델을 생성해요.
    balanced = LogisticRegression(max_iter=500, class_weight="balanced", random_state=42)

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    base.fit(X_train, y_train)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    balanced.fit(X_train, y_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_base = base.predict(X_test)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_balanced = balanced.predict(X_test)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter62",
        # 설명: 이 코드를 실행해요.
        "topic": "클래스 불균형 처리",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "base_model": _scores(y_test, pred_base),
        # 설명: 이 코드를 실행해요.
        "balanced_model": _scores(y_test, pred_balanced),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
