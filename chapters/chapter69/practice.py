# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""소프트맥스 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "소프트맥스는 점수(logit)를 확률로 바꿔 총합이 1이 되게 만든다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "벡터를 softmax로 변환하고 합이 1인지 확인한다."


# 설명: 'softmax' 함수를 정의해요.
def softmax(logits: np.ndarray) -> np.ndarray:
    # 설명: 수치 안정성을 위해 로짓에서 최댓값을 빼요 (오버플로 방지).
    shifted = logits - logits.max(axis=-1, keepdims=True)
    # 설명: e의 거듭제곱(지수 함수)을 원소별로 계산해요.
    exp_values = np.exp(shifted)
    # 설명: 'exp_values / exp_values.sum(axis=-1, keepdims=True)'을(를) 함수 호출 측에 반환해요.
    return exp_values / exp_values.sum(axis=-1, keepdims=True)


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    logits = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [2.2, 0.7, -1.0],
            # 설명: 이 코드를 실행해요.
            [0.1, 1.9, 1.2],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 소프트맥스 출력 등 각 클래스의 확률 배열을 정의해요.
    probs = softmax(logits)
    # 설명: 'shifted_probs' 변수에 값을 계산해서 저장해요.
    shifted_probs = softmax(logits + 10.0)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter69",
        # 설명: 이 코드를 실행해요.
        "topic": "소프트맥스",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "logits": logits.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "probabilities": probs.round(4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "row_sum": probs.sum(axis=1).round(4).tolist(),
        # 설명: 배열에서 가장 큰 값이 있는 위치(인덱스)를 반환해요.
        "argmax_class": np.argmax(probs, axis=1).tolist(),
        # 설명: 두 배열의 모든 원소가 허용 오차 내에서 같은지 확인해요.
        "shift_invariant_check": bool(np.allclose(probs, shifted_probs, atol=1e-9)),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
