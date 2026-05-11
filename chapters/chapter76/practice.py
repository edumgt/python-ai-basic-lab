# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""과적합 방지(정규화/드롭아웃 개념) 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: LinearRegression, Ridge를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LinearRegression, Ridge
# 설명: mean_squared_error를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import mean_squared_error
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: Pipeline를(을) 전처리와 모델을 하나로 묶는 Pipeline 도구를 불러와요.
from sklearn.pipeline import Pipeline
# 설명: PolynomialFeatures를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import PolynomialFeatures


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "복잡한 모델은 과적합되기 쉬우며 정규화가 일반화 성능을 도울 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "고차 다항식 회귀에서 정규화 유무에 따른 train/test 오차를 비교한다."


# 설명: '_mse' 함수를 정의해요.
def _mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    # 설명: 'float(mean_squared_error(y_true, y_pred))'을(를) 함수 호출 측에 반환해요.
    return float(mean_squared_error(y_true, y_pred))


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)

    # 설명: 시작~끝 범위를 균등 간격으로 나눈 배열을 생성해요.
    x = np.linspace(-3, 3, 180)
    # 설명: 사인(sin) 값을 원소별로 계산해요.
    y = np.sin(1.3 * x) + rng.normal(0, 0.12, size=x.shape[0])
    # 설명: 배열의 형태를 바꿔요.
    X = x.reshape(-1, 1)

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.3, random_state=42
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 전처리 단계와 모델을 하나의 파이프라인으로 연결해요.
    no_reg = Pipeline(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: '("poly", PolynomialFeatures(degree' 변수에 값을 계산해서 저장해요.
            ("poly", PolynomialFeatures(degree=10, include_bias=False)),
            # 설명: 선형 회귀 모델(y = w·x + b)을 생성해요.
            ("model", LinearRegression()),
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 전처리 단계와 모델을 하나의 파이프라인으로 연결해요.
    ridge_reg = Pipeline(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: '("poly", PolynomialFeatures(degree' 변수에 값을 계산해서 저장해요.
            ("poly", PolynomialFeatures(degree=10, include_bias=False)),
            # 설명: L2 규제(계수 크기 제한)를 적용한 릿지 회귀 모델을 생성해요.
            ("model", Ridge(alpha=1.0)),
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    no_reg.fit(X_train, y_train)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    ridge_reg.fit(X_train, y_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_train_no = no_reg.predict(X_train)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_test_no = no_reg.predict(X_test)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_train_ridge = ridge_reg.predict(X_train)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_test_ridge = ridge_reg.predict(X_test)

    # 설명: 'train_no' 변수에 값을 계산해서 저장해요.
    train_no = _mse(y_train, pred_train_no)
    # 설명: 'test_no' 변수에 값을 계산해서 저장해요.
    test_no = _mse(y_test, pred_test_no)
    # 설명: 'train_ridge' 변수에 값을 계산해서 저장해요.
    train_ridge = _mse(y_train, pred_train_ridge)
    # 설명: 'test_ridge' 변수에 값을 계산해서 저장해요.
    test_ridge = _mse(y_test, pred_test_ridge)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter76",
        # 설명: 이 코드를 실행해요.
        "topic": "과적합 방지(정규화/드롭아웃 개념)",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "no_regularization": {
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "train_mse": round(train_no, 6),
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "test_mse": round(test_no, 6),
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "generalization_gap": round(test_no - train_no, 6),
        # 설명: 이 코드를 실행해요.
        },
        # 설명: 이 코드를 실행해요.
        "ridge_regularization": {
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "train_mse": round(train_ridge, 6),
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "test_mse": round(test_ridge, 6),
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "generalization_gap": round(test_ridge - train_ridge, 6),
        # 설명: 이 코드를 실행해요.
        },
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
