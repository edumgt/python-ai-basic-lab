# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""정밀도와 재현율 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: precision_score, recall_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import precision_score, recall_score


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "임계값을 바꾸면 정밀도와 재현율이 서로 반대로 움직일 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "여러 threshold에서 precision/recall을 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0], dtype=int)
    # 설명: 모델이 각 클래스에 대해 예측한 확률 배열을 정의해요.
    y_prob = np.array([0.91, 0.35, 0.76, 0.64, 0.21, 0.55, 0.72, 0.18, 0.43, 0.30])

    # 설명: 'thresholds' 변수에 값을 계산해서 저장해요.
    thresholds = [0.3, 0.5, 0.7]
    # 설명: 'metrics' 변수에 값을 계산해서 저장해요.
    metrics = []
    # 설명: 'thresholds'의 각 원소를 'th'로 받으며 반복해요.
    for th in thresholds:
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = (y_prob >= th).astype(int)
        # 설명: 이 코드를 실행해요.
        metrics.append(
            # 설명: 이 코드를 실행해요.
            {
                # 설명: 이 코드를 실행해요.
                "threshold": th,
                # 설명: 양성으로 예측한 것 중 실제 양성 비율(정밀도)을 계산해요.
                "precision": round(float(precision_score(y_true, pred, zero_division=0)), 4),
                # 설명: 실제 양성 중 양성으로 예측한 비율(재현율)을 계산해요.
                "recall": round(float(recall_score(y_true, pred, zero_division=0)), 4),
            # 설명: 이 코드를 실행해요.
            }
        # 설명: 이 코드를 실행해요.
        )

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter47",
        # 설명: 이 코드를 실행해요.
        "topic": "정밀도와 재현율",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "threshold_metrics": metrics,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
