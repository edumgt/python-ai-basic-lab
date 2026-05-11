# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""과적합과 과소적합 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: LinearRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LinearRegression
# 설명: r2_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import r2_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: Pipeline를(을) 전처리와 모델을 하나로 묶는 Pipeline 도구를 불러와요.
from sklearn.pipeline import Pipeline
# 설명: PolynomialFeatures를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import PolynomialFeatures


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "모델이 너무 단순하면 과소적합, 너무 복잡하면 과적합이 발생할 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "다항식 차수를 바꿔 train/test R2를 비교한다."


# 설명: '_fit_degree' 함수를 정의해요.
def _fit_degree(x_train: np.ndarray, x_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray, degree: int) -> dict[str, float]:
    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = Pipeline(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: '("poly", PolynomialFeatures(degree' 변수에 값을 계산해서 저장해요.
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            # 설명: 선형 회귀 모델(y = w·x + b)을 생성해요.
            ("linear", LinearRegression()),
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    model.fit(x_train, y_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_train = model.predict(x_train)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    pred_test = model.predict(x_test)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 결정계수(R²)로 모델이 분산을 얼마나 설명하는지 측정해요.
        "train_r2": round(float(r2_score(y_train, pred_train)), 4),
        # 설명: 결정계수(R²)로 모델이 분산을 얼마나 설명하는지 측정해요.
        "test_r2": round(float(r2_score(y_test, pred_test)), 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 시작~끝 범위를 균등 간격으로 나눈 배열을 생성해요.
    x = np.linspace(-3, 3, 220)
    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = 0.5 * x**3 - 2.0 * x + rng.normal(0, 2.0, size=x.shape[0])

    # 설명: 배열의 형태를 바꿔요.
    X = x.reshape(-1, 1)
    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 설명: 챕터·주제 정보와 실습 결과를 담을 딕셔너리를 초기화해요.
    result = {
        # 설명: '"degree_1": _fit_degree(X_train, X_test, y_train, y_test, degree' 변수에 값을 계산해서 저장해요.
        "degree_1": _fit_degree(X_train, X_test, y_train, y_test, degree=1),
        # 설명: '"degree_3": _fit_degree(X_train, X_test, y_train, y_test, degree' 변수에 값을 계산해서 저장해요.
        "degree_3": _fit_degree(X_train, X_test, y_train, y_test, degree=3),
        # 설명: '"degree_12": _fit_degree(X_train, X_test, y_train, y_test, degree' 변수에 값을 계산해서 저장해요.
        "degree_12": _fit_degree(X_train, X_test, y_train, y_test, degree=12),
    # 설명: 이 코드를 실행해요.
    }

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter52",
        # 설명: 이 코드를 실행해요.
        "topic": "과적합/과소적합",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "r2_by_degree": result,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
