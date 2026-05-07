# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""에러 분석 노트 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd
# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: RandomForestClassifier를(을) 랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.
from sklearn.ensemble import RandomForestClassifier
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "성능 수치만 보지 말고 어떤 샘플에서 틀렸는지 확인해야 개선 포인트가 보인다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "오분류 샘플을 표로 뽑아 에러 노트를 만든다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=280,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=6,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=4,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=1,
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=42,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 지정 범위의 정수 시퀀스를 생성해요.
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(X, columns=feature_names)
    # 설명: 'df["target"]' 변수에 값을 계산해서 저장해요.
    df["target"] = y

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'df[feature_names], df["target"], test_size' 변수에 값을 계산해서 저장해요.
        df[feature_names], df["target"], test_size=0.25, random_state=42, stratify=df["target"]
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = RandomForestClassifier(n_estimators=160, random_state=42)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    model.fit(X_train, y_train)
    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = model.predict(X_test)

    # 설명: 'review' 변수에 값을 계산해서 저장해요.
    review = X_test.copy().reset_index(drop=True)
    # 설명: 'review["true"]' 변수에 값을 계산해서 저장해요.
    review["true"] = y_test.reset_index(drop=True)
    # 설명: 'review["pred"]' 변수에 값을 계산해서 저장해요.
    review["pred"] = pred
    # 설명: 'errors' 변수에 값을 계산해서 저장해요.
    errors = review[review["true"] != review["pred"]].copy()

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter64",
        # 설명: 이 코드를 실행해요.
        "topic": "에러 분석 노트",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 정수형으로 변환해요.
        "test_rows": int(len(review)),
        # 설명: 값을 정수형으로 변환해요.
        "error_rows": int(len(errors)),
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "error_rate": round(float(len(errors) / len(review)), 4),
        # 설명: 지정된 소수점 자릿수에서 반올림해요.
        "error_samples": errors.head(5).round(4).to_dict(orient="records"),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
