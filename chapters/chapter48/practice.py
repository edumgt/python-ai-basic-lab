# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""F1 점수 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: f1_score, precision_score, recall_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import f1_score, precision_score, recall_score


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "F1 점수는 정밀도와 재현율의 균형을 한 숫자로 본다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "불균형 데이터에서 F1이 높은 모델을 찾는다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true = np.array([0] * 80 + [1] * 20, dtype=int)

    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    pred_high_precision = np.array(([0] * 78) + ([1] * 2) + ([0] * 10) + ([1] * 10), dtype=int)
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    pred_high_recall = np.array(([0] * 65) + ([1] * 15) + ([0] * 3) + ([1] * 17), dtype=int)

    # 설명: 'report' 함수를 정의해요.
    def report(pred: np.ndarray) -> dict[str, float]:
        # 설명: '{'을(를) 함수 호출 측에 반환해요.
        return {
            # 설명: 양성으로 예측한 것 중 실제 양성 비율(정밀도)을 계산해요.
            "precision": round(float(precision_score(y_true, pred, zero_division=0)), 4),
            # 설명: 실제 양성 중 양성으로 예측한 비율(재현율)을 계산해요.
            "recall": round(float(recall_score(y_true, pred, zero_division=0)), 4),
            # 설명: 정밀도와 재현율의 조화평균인 F1 점수를 계산해요.
            "f1": round(float(f1_score(y_true, pred, zero_division=0)), 4),
        # 설명: 이 코드를 실행해요.
        }

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter48",
        # 설명: 이 코드를 실행해요.
        "topic": "F1 점수",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "model_high_precision": report(pred_high_precision),
        # 설명: 이 코드를 실행해요.
        "model_high_recall": report(pred_high_recall),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
