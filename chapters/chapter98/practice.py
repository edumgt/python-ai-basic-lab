# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""최종 미니 프로젝트 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: accuracy_score, f1_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score, f1_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: Pipeline를(을) 전처리와 모델을 하나로 묶는 Pipeline 도구를 불러와요.
from sklearn.pipeline import Pipeline
# 설명: StandardScaler를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import StandardScaler


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "최종 프로젝트는 문제정의-전처리-학습-평가-보고까지 한 흐름으로 완성한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "합성 데이터 하나로 end-to-end 분류 파이프라인을 실행한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 'n' 변수에 값을 계산해서 저장해요.
    n = 260

    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: '"study_minutes": rng.normal(45, 15, size' 변수에 값을 계산해서 저장해요.
            "study_minutes": rng.normal(45, 15, size=n),
            # 설명: '"attendance_rate": rng.uniform(0.6, 1.0, size' 변수에 값을 계산해서 저장해요.
            "attendance_rate": rng.uniform(0.6, 1.0, size=n),
            # 설명: '"quiz_score": rng.normal(70, 12, size' 변수에 값을 계산해서 저장해요.
            "quiz_score": rng.normal(70, 12, size=n),
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = (
        # 설명: 이 코드를 실행해요.
        0.02 * df["study_minutes"]
        # 설명: 이 코드를 실행해요.
        + 1.8 * df["attendance_rate"]
        # 설명: 이 코드를 실행해요.
        + 0.03 * df["quiz_score"]
        # 설명: '+ rng.normal(0, 0.35, size' 변수에 값을 계산해서 저장해요.
        + rng.normal(0, 0.35, size=n)
        # 설명: 이 코드를 실행해요.
        > 4.2
    # 설명: 이 코드를 실행해요.
    ).astype(int)

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'df, y, test_size' 변수에 값을 계산해서 저장해요.
        df, y, test_size=0.25, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = Pipeline(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요.
            ("scaler", StandardScaler()),
            # 설명: 로지스틱 회귀 분류 모델을 생성해요.
            ("classifier", LogisticRegression(max_iter=500, random_state=42)),
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    model.fit(X_train, y_train)
    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = model.predict(X_test)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter98",
        # 설명: 이 코드를 실행해요.
        "topic": "최종 미니 프로젝트",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 정수형으로 변환해요.
        "train_rows": int(len(X_train)),
        # 설명: 값을 정수형으로 변환해요.
        "test_rows": int(len(X_test)),
        # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        # 설명: 정밀도와 재현율의 조화평균인 F1 점수를 계산해요.
        "f1": round(float(f1_score(y_test, pred)), 4),
        # 설명: 이 코드를 실행해요.
        "pipeline_steps": ["scaler", "classifier"],
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
