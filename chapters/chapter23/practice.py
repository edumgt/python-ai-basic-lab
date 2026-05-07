# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""활성화 함수 비교"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 'sigmoid' 함수를 정의해요.
def sigmoid(x: np.ndarray) -> np.ndarray:
    # 설명: '1 / (1 + np.exp(-x))'을(를) 함수 호출 측에 반환해요.
    return 1 / (1 + np.exp(-x))


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 시작~끝 범위를 균등 간격으로 나눈 배열을 생성해요.
    x = np.linspace(-3, 3, 7)
    # 설명: 음수는 0으로, 양수는 그대로 유지하는 ReLU 활성화 함수예요.
    relu = np.maximum(0, x)
    # 설명: 'sig' 변수에 값을 계산해서 저장해요.
    sig = sigmoid(x)
    # 설명: 쌍곡 탄젠트(tanh) 활성화 함수를 원소별로 계산해요.
    tanh = np.tanh(x)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter23",
        # 설명: 이 코드를 실행해요.
        "topic": "활성화 함수 비교",
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "x": np.round(x, 3).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "relu": np.round(relu, 3).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "sigmoid": np.round(sig, 3).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "tanh": np.round(tanh, 3).tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
