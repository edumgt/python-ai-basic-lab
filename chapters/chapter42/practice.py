# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""데이터 누수 이해 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "미래 정보가 입력에 섞이면 평가 점수가 비정상적으로 높아진다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "누수 특성 포함/제외 정확도를 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 'n' 변수에 값을 계산해서 저장해요.
    n = 240

    # 설명: 'hours' 변수에 값을 계산해서 저장해요.
    hours = rng.normal(5, 1.2, size=n)
    # 설명: 'attendance' 변수에 값을 계산해서 저장해요.
    attendance = rng.normal(80, 10, size=n)

    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = (hours * 0.7 + attendance * 0.03 + rng.normal(0, 0.8, size=n) > 6.0).astype(int)

    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "hours": hours,
            # 설명: 이 코드를 실행해요.
            "attendance": attendance,
            # 설명: 이 코드를 실행해요.
            "target": y,
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 의도적인 누수: target을 거의 그대로 보여주는 컬럼
    # 설명: 'df["future_hint"]' 변수에 값을 계산해서 저장해요.
    df["future_hint"] = df["target"] + rng.normal(0, 0.02, size=n)

    # 설명: 'X_safe' 변수에 값을 계산해서 저장해요.
    X_safe = df[["hours", "attendance"]]
    # 설명: 'X_leak' 변수에 값을 계산해서 저장해요.
    X_leak = df[["hours", "attendance", "future_hint"]]
    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = df["target"]

    # 설명: 데이터를 학습용과 테스트용으로 분리해요.
    Xs_train, Xs_test, ys_train, ys_test = train_test_split(
        # 설명: 'X_safe, y, test_size' 변수에 값을 계산해서 저장해요.
        X_safe, y, test_size=0.3, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 데이터를 학습용과 테스트용으로 분리해요.
    Xl_train, Xl_test, yl_train, yl_test = train_test_split(
        # 설명: 'X_leak, y, test_size' 변수에 값을 계산해서 저장해요.
        X_leak, y, test_size=0.3, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    safe_model = LogisticRegression(max_iter=500).fit(Xs_train, ys_train)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    leak_model = LogisticRegression(max_iter=500).fit(Xl_train, yl_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    safe_acc = float(accuracy_score(ys_test, safe_model.predict(Xs_test)))
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    leak_acc = float(accuracy_score(yl_test, leak_model.predict(Xl_test)))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter42",
        # 설명: 이 코드를 실행해요.
        "topic": "데이터 누수 이해",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "safe_features": ["hours", "attendance"],
        # 설명: 이 코드를 실행해요.
        "leak_feature": "future_hint",
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "accuracy_without_leak": round(safe_acc, 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "accuracy_with_leak": round(leak_acc, 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
