# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""결측치 처리 전략 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: 'sklearn.impute' 모듈에서 SimpleImputer를(을) 불러와요.
from sklearn.impute import SimpleImputer
# 설명: LinearRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LinearRegression
# 설명: mean_squared_error를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import mean_squared_error
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "결측치는 삭제와 대체 중 어떤 전략이 나은지 비교해야 한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "drop, mean, median 전략의 회귀 오차를 비교한다."


# 설명: '_rmse' 함수를 정의해요.
def _rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    # 설명: 'float(np.sqrt(mean_squared_error(y_true, y_pred)))'을(를) 함수 호출 측에 반환해요.
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 'n' 변수에 값을 계산해서 저장해요.
    n = 220

    # 설명: 'X' 변수에 값을 계산해서 저장해요.
    X = rng.normal(0, 1, size=(n, 3))
    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = 12 * X[:, 0] - 4 * X[:, 1] + 2 * X[:, 2] + rng.normal(0, 1.8, size=n)

    # 설명: 'missing_mask1' 변수에 값을 계산해서 저장해요.
    missing_mask1 = rng.random(n) < 0.18
    # 설명: 'missing_mask2' 변수에 값을 계산해서 저장해요.
    missing_mask2 = rng.random(n) < 0.12
    # 설명: 'X[missing_mask1, 0]' 변수에 값을 계산해서 저장해요.
    X[missing_mask1, 0] = np.nan
    # 설명: 'X[missing_mask2, 1]' 변수에 값을 계산해서 저장해요.
    X[missing_mask2, 1] = np.nan

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.3, random_state=42
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'train_ok' 변수에 값을 계산해서 저장해요.
    train_ok = ~np.isnan(X_train).any(axis=1)
    # 설명: 'test_ok' 변수에 값을 계산해서 저장해요.
    test_ok = ~np.isnan(X_test).any(axis=1)

    # 설명: 'drop_rmse' 변수에 값을 계산해서 저장해요.
    drop_rmse = None
    # 설명: 조건 (train_ok.sum() > 5 and test_ok.sum() > 1)이 참인지 확인해요.
    if train_ok.sum() > 5 and test_ok.sum() > 1:
        # 설명: 선형 회귀 모델(y = w·x + b)을 생성해요.
        drop_model = LinearRegression()
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        drop_model.fit(X_train[train_ok], y_train[train_ok])
        # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
        drop_pred = drop_model.predict(X_test[test_ok])
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        drop_rmse = round(_rmse(y_test[test_ok], drop_pred), 4)

    # 설명: 'mean_imputer' 변수에 값을 계산해서 저장해요.
    mean_imputer = SimpleImputer(strategy="mean")
    # 설명: 'median_imputer' 변수에 값을 계산해서 저장해요.
    median_imputer = SimpleImputer(strategy="median")

    # 설명: 변환기(스케일러 등)를 학습하고 동시에 데이터를 변환해요.
    X_train_mean = mean_imputer.fit_transform(X_train)
    # 설명: 이미 학습된 변환기로 데이터를 변환해요.
    X_test_mean = mean_imputer.transform(X_test)
    # 설명: 변환기(스케일러 등)를 학습하고 동시에 데이터를 변환해요.
    X_train_median = median_imputer.fit_transform(X_train)
    # 설명: 이미 학습된 변환기로 데이터를 변환해요.
    X_test_median = median_imputer.transform(X_test)

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    mean_model = LinearRegression().fit(X_train_mean, y_train)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    median_model = LinearRegression().fit(X_train_median, y_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_mean = mean_model.predict(X_test_mean)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_median = median_model.predict(X_test_median)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter38",
        # 설명: 이 코드를 실행해요.
        "topic": "결측치 처리 전략",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 합계를 계산해요.
        "missing_count": int(np.isnan(X).sum()),
        # 설명: 이 코드를 실행해요.
        "usable_rows_drop": {
            # 설명: 합계를 계산해요.
            "train": int(train_ok.sum()),
            # 설명: 합계를 계산해요.
            "test": int(test_ok.sum()),
        # 설명: 이 코드를 실행해요.
        },
        # 설명: 이 코드를 실행해요.
        "rmse": {
            # 설명: 이 코드를 실행해요.
            "dropna": drop_rmse,
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "mean_impute": round(_rmse(y_test, pred_mean), 4),
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            "median_impute": round(_rmse(y_test, pred_median), 4),
        # 설명: 이 코드를 실행해요.
        },
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
