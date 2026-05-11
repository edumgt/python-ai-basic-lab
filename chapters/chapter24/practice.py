# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""소프트맥스 확률 해석"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 'softmax' 함수를 정의해요.
def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    # 설명: 'scaled' 변수에 값을 계산해서 저장해요.
    scaled = logits / temperature
    # 설명: 수치 안정성을 위해 로짓에서 최댓값을 빼요 (오버플로 방지).
    shifted = scaled - np.max(scaled, axis=1, keepdims=True)
    # 설명: 이동된 로짓에 지수 함수를 적용해요.
    exp_scores = np.exp(shifted)
    # 설명: 'exp_scores / np.sum(exp_scores, axis=1, keepdims=True)'을(를) 함수 호출 측에 반환해요.
    return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    logits = np.array([[2.0, 1.0, 0.1], [0.5, 0.2, 3.1]])
    # 설명: 'p_t1' 변수에 값을 계산해서 저장해요.
    p_t1 = softmax(logits, temperature=1.0)
    # 설명: 'p_t05' 변수에 값을 계산해서 저장해요.
    p_t05 = softmax(logits, temperature=0.5)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter24",
        # 설명: 이 코드를 실행해요.
        "topic": "소프트맥스",
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "logits": logits.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "probs_t1": np.round(p_t1, 4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "probs_t05": np.round(p_t05, 4).tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
