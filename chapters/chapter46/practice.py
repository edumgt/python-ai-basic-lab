# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""혼동행렬 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: confusion_matrix를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import confusion_matrix


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "혼동행렬은 정답과 예측의 조합을 한 번에 보여준다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "TN, FP, FN, TP 값을 직접 읽어본다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0], dtype=int)
    # 설명: 모델이 예측한 레이블 배열을 정의해요.
    y_pred = np.array([1, 0, 0, 1, 0, 1, 1, 0, 0, 0], dtype=int)

    # 설명: 'cm' 변수에 값을 계산해서 저장해요.
    cm = confusion_matrix(y_true, y_pred)
    # 설명: 'tn, fp, fn, tp' 변수에 값을 계산해서 저장해요.
    tn, fp, fn, tp = cm.ravel()

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter46",
        # 설명: 이 코드를 실행해요.
        "topic": "혼동행렬",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "confusion_matrix": cm.tolist(),
        # 설명: 값을 정수형으로 변환해요.
        "tn": int(tn),
        # 설명: 값을 정수형으로 변환해요.
        "fp": int(fp),
        # 설명: 값을 정수형으로 변환해요.
        "fn": int(fn),
        # 설명: 값을 정수형으로 변환해요.
        "tp": int(tp),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
