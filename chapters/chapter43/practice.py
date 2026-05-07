# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""재현 가능한 실험 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: RandomForestClassifier를(을) 랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.
from sklearn.ensemble import RandomForestClassifier
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "random_state를 고정하면 같은 코드에서 같은 결과를 얻기 쉽다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "시드 고정 전/후 예측 결과 차이를 비교한다."


# 설명: '_run_model' 함수를 정의해요.
def _run_model(random_state: int | None) -> tuple[np.ndarray, np.ndarray]:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=260,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=8,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=5,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=1,
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=123,
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.3, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = RandomForestClassifier(n_estimators=120, random_state=random_state)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    model.fit(X_train, y_train)
    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = model.predict(X_test)
    # 설명: 'pred, y_test'을(를) 함수 호출 측에 반환해요.
    return pred, y_test


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'pred_free_1, y_test' 변수에 값을 계산해서 저장해요.
    pred_free_1, y_test = _run_model(random_state=None)
    # 설명: 'pred_free_2, _' 변수에 값을 계산해서 저장해요.
    pred_free_2, _ = _run_model(random_state=None)

    # 설명: 'pred_fixed_1, y_test_fixed' 변수에 값을 계산해서 저장해요.
    pred_fixed_1, y_test_fixed = _run_model(random_state=42)
    # 설명: 'pred_fixed_2, _' 변수에 값을 계산해서 저장해요.
    pred_fixed_2, _ = _run_model(random_state=42)

    # 설명: 합계를 계산해요.
    free_diff = int((pred_free_1 != pred_free_2).sum())
    # 설명: 합계를 계산해요.
    fixed_diff = int((pred_fixed_1 != pred_fixed_2).sum())

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter43",
        # 설명: 이 코드를 실행해요.
        "topic": "재현 가능한 실험",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
        "accuracy_fixed": round(float(accuracy_score(y_test_fixed, pred_fixed_1)), 4),
        # 설명: 이 코드를 실행해요.
        "prediction_diff_without_seed": free_diff,
        # 설명: 이 코드를 실행해요.
        "prediction_diff_with_seed": fixed_diff,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
