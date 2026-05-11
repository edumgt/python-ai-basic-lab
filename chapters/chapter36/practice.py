# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""스케일링 개념 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: StandardScaler를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import StandardScaler


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "서로 단위가 다른 특성은 스케일을 맞추면 학습이 안정적이다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "스케일링 전후 분류 정확도를 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 'n' 변수에 값을 계산해서 저장해요.
    n = 180

    # 설명: 'feature_large' 변수에 값을 계산해서 저장해요.
    feature_large = rng.normal(loc=5000, scale=900, size=n)
    # 설명: 'feature_small' 변수에 값을 계산해서 저장해요.
    feature_small = rng.normal(loc=0.5, scale=0.12, size=n)
    # 설명: 'noise' 변수에 값을 계산해서 저장해요.
    noise = rng.normal(loc=0.0, scale=0.06, size=n)
    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = (feature_small + noise > 0.5).astype(int)

    # 설명: 'X' 변수에 값을 계산해서 저장해요.
    X = np.column_stack([feature_large, feature_small])

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.3, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 로지스틱 회귀 분류 모델을 생성해요.
    raw_model = LogisticRegression(max_iter=500)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    raw_model.fit(X_train, y_train)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    raw_pred = raw_model.predict(X_test)
    # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
    raw_acc = float(accuracy_score(y_test, raw_pred))

    # 설명: 데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요.
    scaler = StandardScaler()
    # 설명: 변환기(스케일러 등)를 학습하고 동시에 데이터를 변환해요.
    X_train_scaled = scaler.fit_transform(X_train)
    # 설명: 이미 학습된 변환기로 데이터를 변환해요.
    X_test_scaled = scaler.transform(X_test)

    # 설명: 로지스틱 회귀 분류 모델을 생성해요.
    scaled_model = LogisticRegression(max_iter=500)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    scaled_model.fit(X_train_scaled, y_train)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    scaled_pred = scaled_model.predict(X_test_scaled)
    # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
    scaled_acc = float(accuracy_score(y_test, scaled_pred))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter36",
        # 설명: 이 코드를 실행해요.
        "topic": "스케일링 개념",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "raw_feature_mean": X.mean(axis=0).round(3).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "raw_feature_std": X.std(axis=0).round(3).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "scaled_train_mean": X_train_scaled.mean(axis=0).round(3).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "scaled_train_std": X_train_scaled.std(axis=0).round(3).tolist(),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "accuracy_raw": round(raw_acc, 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "accuracy_scaled": round(scaled_acc, 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
