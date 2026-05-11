# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""간단한 피처 엔지니어링 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd
# 설명: LinearRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LinearRegression
# 설명: r2_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import r2_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "원본 특성만 쓰는 것보다 새 특성을 만들면 성능이 좋아질 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "파생 특성 추가 전/후 R2를 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 'n' 변수에 값을 계산해서 저장해요.
    n = 200

    # 설명: 'study_hours' 변수에 값을 계산해서 저장해요.
    study_hours = rng.uniform(1, 6, size=n)
    # 설명: 'sleep_hours' 변수에 값을 계산해서 저장해요.
    sleep_hours = rng.uniform(5, 9, size=n)

    # 설명: 평가 점수를 계산해서 저장해요.
    score = 8 * study_hours + 4 * sleep_hours + 2 * study_hours * sleep_hours + rng.normal(0, 2.0, size=n)

    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "study_hours": study_hours,
            # 설명: 이 코드를 실행해요.
            "sleep_hours": sleep_hours,
            # 설명: 이 코드를 실행해요.
            "score": score,
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'base_features' 변수에 값을 계산해서 저장해요.
    base_features = ["study_hours", "sleep_hours"]
    # 설명: 'engineered' 변수에 값을 계산해서 저장해요.
    engineered = df.copy()
    # 설명: 'engineered["study_x_sleep"]' 변수에 값을 계산해서 저장해요.
    engineered["study_x_sleep"] = engineered["study_hours"] * engineered["sleep_hours"]
    # 설명: 'engineered["study_per_sleep"]' 변수에 값을 계산해서 저장해요.
    engineered["study_per_sleep"] = engineered["study_hours"] / engineered["sleep_hours"]

    # 설명: 'X_base' 변수에 값을 계산해서 저장해요.
    X_base = df[base_features]
    # 설명: 'X_eng' 변수에 값을 계산해서 저장해요.
    X_eng = engineered[["study_hours", "sleep_hours", "study_x_sleep", "study_per_sleep"]]
    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = df["score"]

    # 설명: 데이터를 학습용과 테스트용으로 분리해요.
    Xb_train, Xb_test, y_train, y_test = train_test_split(
        # 설명: 'X_base, y, test_size' 변수에 값을 계산해서 저장해요.
        X_base, y, test_size=0.25, random_state=42
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 데이터를 학습용과 테스트용으로 분리해요.
    Xe_train, Xe_test, _, _ = train_test_split(X_eng, y, test_size=0.25, random_state=42)

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    base_model = LinearRegression().fit(Xb_train, y_train)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    eng_model = LinearRegression().fit(Xe_train, y_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    base_r2 = float(r2_score(y_test, base_model.predict(Xb_test)))
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    eng_r2 = float(r2_score(y_test, eng_model.predict(Xe_test)))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter41",
        # 설명: 이 코드를 실행해요.
        "topic": "간단한 피처 엔지니어링",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "base_features": base_features,
        # 설명: 이 코드를 실행해요.
        "engineered_features": ["study_x_sleep", "study_per_sleep"],
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "r2_base": round(base_r2, 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "r2_engineered": round(eng_r2, 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
