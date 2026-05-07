# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""피처 중요도 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: RandomForestClassifier를(을) 랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.
from sklearn.ensemble import RandomForestClassifier


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "트리 기반 모델은 어떤 입력이 중요한지 점수로 보여줄 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "랜덤포레스트의 feature importance를 정렬해 본다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=260,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=6,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=3,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=1,
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=42,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 지정 범위의 정수 시퀀스를 생성해요.
    feature_names = [f"feature_{i}" for i in range(X.shape[1])]

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = RandomForestClassifier(n_estimators=160, random_state=42)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    model.fit(X, y)

    # 설명: 'importances' 변수에 값을 계산해서 저장해요.
    importances = model.feature_importances_
    # 설명: 시퀀스를 정렬한 새 리스트를 반환해요.
    ranking = sorted(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            {
                # 설명: 이 코드를 실행해요.
                "feature": name,
                # 설명: 값을 부동소수점(실수)형으로 변환해요.
                "importance": round(float(score), 4),
            # 설명: 이 코드를 실행해요.
            }
            # 설명: 각 원소를 순서대로 꺼내며 반복해요.
            for name, score in zip(feature_names, importances)
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'key' 변수에 값을 계산해서 저장해요.
        key=lambda x: x["importance"],
        # 설명: 'reverse' 변수에 값을 계산해서 저장해요.
        reverse=True,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter54",
        # 설명: 이 코드를 실행해요.
        "topic": "피처 중요도",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "importance_ranking": ranking,
        # 설명: 배열 원소의 합계를 계산해요.
        "importance_sum": round(float(np.sum(importances)), 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
