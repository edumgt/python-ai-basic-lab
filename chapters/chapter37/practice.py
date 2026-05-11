# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""파이프라인 기초 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: Pipeline를(을) 전처리와 모델을 하나로 묶는 Pipeline 도구를 불러와요.
from sklearn.pipeline import Pipeline
# 설명: StandardScaler를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import StandardScaler


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "전처리와 모델을 파이프라인으로 묶으면 실수를 줄일 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "StandardScaler와 LogisticRegression을 한 줄 흐름으로 실행한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=220,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=8,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=5,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=1,
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=42,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.25, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 전처리와 모델을 하나로 묶은 Pipeline 객체를 생성해요.
    pipe = Pipeline(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요.
            ("scaler", StandardScaler()),
            # 설명: 로지스틱 회귀 분류 모델을 생성해요.
            ("model", LogisticRegression(max_iter=500, random_state=42)),
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    pipe.fit(X_train, y_train)
    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = pipe.predict(X_test)
    # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
    acc = float(accuracy_score(y_test, pred))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter37",
        # 설명: 이 코드를 실행해요.
        "topic": "파이프라인 기초",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 파이썬 리스트로 변환해요.
        "pipeline_steps": list(pipe.named_steps.keys()),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "accuracy": round(acc, 4),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "sample_predictions": pred[:10].tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
