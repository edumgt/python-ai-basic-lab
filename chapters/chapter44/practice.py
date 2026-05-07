# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""미니 복습 프로젝트 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd
# 설명: ColumnTransformer를(을) 컬럼별 다른 전처리를 조합하는 ColumnTransformer 도구를 불러와요.
from sklearn.compose import ColumnTransformer
# 설명: 'sklearn.impute' 모듈에서 SimpleImputer를(을) 불러와요.
from sklearn.impute import SimpleImputer
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: Pipeline를(을) 전처리와 모델을 하나로 묶는 Pipeline 도구를 불러와요.
from sklearn.pipeline import Pipeline
# 설명: OneHotEncoder, StandardScaler를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "원본 데이터를 전처리 파이프라인으로 학습 가능한 형태로 바꿀 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "결측치 처리 + 인코딩 + 스케일링을 묶어 분류 모델을 만든다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 'n' 변수에 값을 계산해서 저장해요.
    n = 180

    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: '"study_hours": rng.normal(4.5, 1.1, size' 변수에 값을 계산해서 저장해요.
            "study_hours": rng.normal(4.5, 1.1, size=n),
            # 설명: '"sleep_hours": rng.normal(7.0, 0.8, size' 변수에 값을 계산해서 저장해요.
            "sleep_hours": rng.normal(7.0, 0.8, size=n),
            # 설명: '"city": rng.choice(["Seoul", "Busan", "Daegu"], size' 변수에 값을 계산해서 저장해요.
            "city": rng.choice(["Seoul", "Busan", "Daegu"], size=n, p=[0.45, 0.35, 0.20]),
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'missing_idx' 변수에 값을 계산해서 저장해요.
    missing_idx = rng.choice(df.index, size=20, replace=False)
    # 설명: 'df.loc[missing_idx[:10], "study_hours"]' 변수에 값을 계산해서 저장해요.
    df.loc[missing_idx[:10], "study_hours"] = np.nan
    # 설명: 'df.loc[missing_idx[10:], "city"]' 변수에 값을 계산해서 저장해요.
    df.loc[missing_idx[10:], "city"] = np.nan

    # 설명: 'target' 변수에 값을 계산해서 저장해요.
    target = (
        # 설명: 결측값(NaN)을 지정한 값으로 채워요.
        (df["study_hours"].fillna(df["study_hours"].mean()) * 0.7)
        # 설명: 이 코드를 실행해요.
        + (df["sleep_hours"] * 0.3)
        # 설명: '+ rng.normal(0, 0.7, size' 변수에 값을 계산해서 저장해요.
        + rng.normal(0, 0.7, size=n)
        # 설명: 이 코드를 실행해요.
        > 5.5
    # 설명: 이 코드를 실행해요.
    ).astype(int)

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'df, target, test_size' 변수에 값을 계산해서 저장해요.
        df, target, test_size=0.25, random_state=42, stratify=target
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'num_cols' 변수에 값을 계산해서 저장해요.
    num_cols = ["study_hours", "sleep_hours"]
    # 설명: 'cat_cols' 변수에 값을 계산해서 저장해요.
    cat_cols = ["city"]

    # 설명: 컬럼 종류(수치형·범주형)별로 다른 전처리를 적용해요.
    preprocessor = ColumnTransformer(
        # 설명: 'transformers' 변수에 값을 계산해서 저장해요.
        transformers=[
            # 설명: 이 코드를 실행해요.
            (
                # 설명: 이 코드를 실행해요.
                "num",
                # 설명: 전처리 단계와 모델을 하나의 파이프라인으로 연결해요.
                Pipeline(
                    # 설명: 이 코드를 실행해요.
                    [
                        # 설명: '("imputer", SimpleImputer(strategy' 변수에 값을 계산해서 저장해요.
                        ("imputer", SimpleImputer(strategy="mean")),
                        # 설명: 데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요.
                        ("scaler", StandardScaler()),
                    # 설명: 이 코드를 실행해요.
                    ]
                # 설명: 이 코드를 실행해요.
                ),
                # 설명: 이 코드를 실행해요.
                num_cols,
            # 설명: 이 코드를 실행해요.
            ),
            # 설명: 이 코드를 실행해요.
            (
                # 설명: 이 코드를 실행해요.
                "cat",
                # 설명: 전처리 단계와 모델을 하나의 파이프라인으로 연결해요.
                Pipeline(
                    # 설명: 이 코드를 실행해요.
                    [
                        # 설명: '("imputer", SimpleImputer(strategy' 변수에 값을 계산해서 저장해요.
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        # 설명: 범주형 값을 0/1 이진 벡터로 변환하는 인코더를 생성해요.
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    # 설명: 이 코드를 실행해요.
                    ]
                # 설명: 이 코드를 실행해요.
                ),
                # 설명: 이 코드를 실행해요.
                cat_cols,
            # 설명: 이 코드를 실행해요.
            ),
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = Pipeline(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            ("preprocessor", preprocessor),
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
    # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
    acc = float(accuracy_score(y_test, pred))

    # 설명: 이미 학습된 변환기로 데이터를 변환해요.
    transformed_sample = model.named_steps["preprocessor"].transform(X_test.head(3))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter44",
        # 설명: 이 코드를 실행해요.
        "topic": "미니 복습 프로젝트",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 정수형으로 변환해요.
        "train_rows": int(len(X_train)),
        # 설명: 값을 정수형으로 변환해요.
        "test_rows": int(len(X_test)),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "accuracy": round(acc, 4),
        # 설명: 값을 파이썬 리스트로 변환해요.
        "transformed_shape_sample": list(transformed_sample.shape),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
