# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""미니 복습 프로젝트 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: RandomForestClassifier를(을) 랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.
from sklearn.ensemble import RandomForestClassifier
# 설명: f1_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import f1_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: DecisionTreeClassifier를(을) 결정 트리 모델 도구를 불러와요.
from sklearn.tree import DecisionTreeClassifier


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "기준 모델과 개선 모델을 같은 테스트셋에서 비교해야 개선 폭을 신뢰할 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "baseline 대비 개선률을 계산해 보고서 형태로 출력한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=420,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=12,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=7,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=2,
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

    # 설명: 결정 트리 분류 모델을 생성해요.
    baseline = DecisionTreeClassifier(max_depth=3, random_state=42)
    # 설명: 여러 결정 트리를 앙상블한 랜덤 포레스트 분류 모델을 생성해요.
    improved = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)

    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    baseline.fit(X_train, y_train)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    improved.fit(X_train, y_train)

    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    f1_base = float(f1_score(y_test, baseline.predict(X_test)))
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    f1_improved = float(f1_score(y_test, improved.predict(X_test)))

    # 설명: 값을 부동소수점(실수)형으로 변환해요.
    improvement_pct = float((f1_improved - f1_base) / max(abs(f1_base), 1e-9) * 100)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter66",
        # 설명: 이 코드를 실행해요.
        "topic": "미니 복습 프로젝트",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "baseline_f1": round(f1_base, 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "improved_f1": round(f1_improved, 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "improvement_percent": round(improvement_pct, 2),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
