# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""미니 복습 프로젝트 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: make_regression를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_regression
# 설명: RandomForestRegressor를(을) 랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.
from sklearn.ensemble import RandomForestRegressor
# 설명: LinearRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LinearRegression
# 설명: mean_absolute_error, mean_squared_error를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import mean_absolute_error, mean_squared_error
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "같은 데이터로 여러 모델을 비교해 볼 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "선형회귀와 랜덤포레스트의 오차를 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_regression(n_samples=160, n_features=5, noise=14, random_state=42)

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.25, random_state=42
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 선형 회귀 모델(y = w·x + b)을 생성해요.
    linear = LinearRegression()
    # 설명: 랜덤 포레스트 회귀 모델을 생성해요.
    forest = RandomForestRegressor(n_estimators=120, random_state=42)

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    linear.fit(X_train, y_train)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    forest.fit(X_train, y_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_linear = linear.predict(X_test)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_forest = forest.predict(X_test)

    # 설명: 오차 제곱 평균(MSE)을 계산해요 — 클수록 예측이 부정확해요.
    rmse_linear = float(np.sqrt(mean_squared_error(y_test, pred_linear)))
    # 설명: 오차 제곱 평균(MSE)을 계산해요 — 클수록 예측이 부정확해요.
    rmse_forest = float(np.sqrt(mean_squared_error(y_test, pred_forest)))

    # 설명: 예측 오차 절댓값의 평균(MAE)을 계산해요.
    mae_linear = float(mean_absolute_error(y_test, pred_linear))
    # 설명: 예측 오차 절댓값의 평균(MAE)을 계산해요.
    mae_forest = float(mean_absolute_error(y_test, pred_forest))

    # 설명: 'better_model' 변수에 값을 계산해서 저장해요.
    better_model = "linear_regression" if rmse_linear <= rmse_forest else "random_forest"

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter33",
        # 설명: 이 코드를 실행해요.
        "topic": "미니 복습 프로젝트",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "rmse": {
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "linear_regression": round(rmse_linear, 4),
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "random_forest": round(rmse_forest, 4),
        # 설명: 이 코드를 실행해요.
        },
        # 설명: 이 코드를 실행해요.
        "mae": {
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "linear_regression": round(mae_linear, 4),
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "random_forest": round(mae_forest, 4),
        # 설명: 이 코드를 실행해요.
        },
        # 설명: 이 코드를 실행해요.
        "better_model_by_rmse": better_model,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
