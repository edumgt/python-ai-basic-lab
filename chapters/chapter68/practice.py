# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""활성화 함수 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "활성화 함수는 직선만으로는 못 배우는 복잡한 패턴을 학습하게 돕는다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "ReLU, Sigmoid, Tanh 값을 같은 입력에서 비교한다."


# 설명: '_sigmoid' 함수를 정의해요.
def _sigmoid(x: np.ndarray) -> np.ndarray:
    # 설명: '1.0 / (1.0 + np.exp(-x))'을(를) 함수 호출 측에 반환해요.
    return 1.0 / (1.0 + np.exp(-x))


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 시작~끝 범위를 균등 간격으로 나눈 배열을 생성해요.
    x = np.linspace(-3, 3, 13)
    # 설명: 음수는 0으로, 양수는 그대로 유지하는 ReLU 활성화 함수예요.
    relu = np.maximum(0.0, x)
    # 설명: 'sigmoid' 변수에 값을 계산해서 저장해요.
    sigmoid = _sigmoid(x)
    # 설명: 쌍곡 탄젠트(tanh) 활성화 함수를 원소별로 계산해요.
    tanh = np.tanh(x)

    # 설명: 'sample_idx' 변수에 값을 계산해서 저장해요.
    sample_idx = [2, 4, 6, 8, 10]
    # 설명: 'table' 변수에 값을 계산해서 저장해요.
    table = [
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "x": round(float(x[i]), 2),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "relu": round(float(relu[i]), 4),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "sigmoid": round(float(sigmoid[i]), 4),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "tanh": round(float(tanh[i]), 4),
        # 설명: 이 코드를 실행해요.
        }
        # 설명: 각 원소를 순서대로 꺼내며 반복해요.
        for i in sample_idx
    # 설명: 이 코드를 실행해요.
    ]

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter68",
        # 설명: 이 코드를 실행해요.
        "topic": "활성화 함수",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "x_values": x.round(2).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "relu": relu.round(4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "sigmoid": sigmoid.round(4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "tanh": tanh.round(4).tolist(),
        # 설명: 이 코드를 실행해요.
        "sample_table": table,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
