# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""ROC-AUC 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: auc, roc_curve를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import auc, roc_curve


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "ROC 곡선은 임계값을 바꿔도 모델이 얼마나 잘 구분하는지 보여준다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "ROC 곡선 좌표와 AUC 값을 계산한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1, 1, 0], dtype=int)
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    y_score = np.array([0.12, 0.33, 0.88, 0.74, 0.41, 0.92, 0.25, 0.61, 0.80, 0.30])

    # 설명: 'fpr, tpr, thresholds' 변수에 값을 계산해서 저장해요.
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    # 설명: 값을 부동소수점(실수)형으로 변환해요.
    auc_value = float(auc(fpr, tpr))

    # 설명: 'points' 변수에 값을 계산해서 저장해요.
    points = [
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "fpr": round(float(fpr[i]), 4),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "tpr": round(float(tpr[i]), 4),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "threshold": round(float(thresholds[i]), 4),
        # 설명: 이 코드를 실행해요.
        }
        # 설명: 각 원소를 순서대로 꺼내며 반복해요.
        for i in range(len(fpr))
    # 설명: 이 코드를 실행해요.
    ]

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter49",
        # 설명: 이 코드를 실행해요.
        "topic": "ROC-AUC",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "auc": round(auc_value, 4),
        # 설명: 이 코드를 실행해요.
        "roc_points": points,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
