# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""학습곡선 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: StratifiedKFold, learning_curve를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import StratifiedKFold, learning_curve


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "학습곡선으로 데이터 양이 늘 때 성능이 어떻게 변하는지 볼 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "train/test score 곡선을 계산해 추세를 확인한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=320,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=10,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=6,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=2,
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=42,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = LogisticRegression(max_iter=500, random_state=42)
    # 설명: K-폴드 교차검증 분할기를 생성해요.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # 설명: 'train_sizes, train_scores, valid_scores' 변수에 값을 계산해서 저장해요.
    train_sizes, train_scores, valid_scores = learning_curve(
        # 설명: 이 코드를 실행해요.
        model,
        # 설명: 이 코드를 실행해요.
        X,
        # 설명: 이 코드를 실행해요.
        y,
        # 설명: 시작~끝 범위를 균등 간격으로 나눈 배열을 생성해요.
        train_sizes=np.linspace(0.2, 1.0, 5),
        # 설명: K-폴드 교차검증 분할기를 생성해요.
        cv=cv,
        # 설명: 'scoring' 변수에 값을 계산해서 저장해요.
        scoring="accuracy",
        # 설명: 'n_jobs' 변수에 값을 계산해서 저장해요.
        n_jobs=None,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter53",
        # 설명: 이 코드를 실행해요.
        "topic": "학습곡선",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "train_sizes": train_sizes.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "train_score_mean": np.round(train_scores.mean(axis=1), 4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "valid_score_mean": np.round(valid_scores.mean(axis=1), 4).tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
