# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""단층 분류기 역전파 기초"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 'softmax' 함수를 정의해요.
def softmax(logits: np.ndarray) -> np.ndarray:
    # 설명: 수치 안정성을 위해 로짓에서 최댓값을 빼요 (오버플로 방지).
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    # 설명: e의 거듭제곱(지수 함수)을 원소별로 계산해요.
    ex = np.exp(shifted)
    # 설명: 'ex / np.sum(ex, axis=1, keepdims=True)'을(를) 함수 호출 측에 반환해요.
    return ex / np.sum(ex, axis=1, keepdims=True)


# 설명: 'one_hot' 함수를 정의해요.
def one_hot(y: np.ndarray, num_classes: int) -> np.ndarray:
    # 설명: 출력 결과를 저장할 배열을 초기화해요.
    out = np.zeros((len(y), num_classes))
    # 설명: 지정 범위의 연속 정수·간격 배열을 생성해요.
    out[np.arange(len(y)), y] = 1.0
    # 설명: 'out'을(를) 함수 호출 측에 반환해요.
    return out


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    X = np.array([[1.0, 2.0], [0.5, -1.0], [1.5, 0.3]])
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    y = np.array([0, 1, 0])

    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    W = np.array([[0.2, -0.1], [0.1, 0.3]])
    # 설명: 모든 원소가 0인 NumPy 배열을 생성해요.
    b = np.zeros((1, 2))

    # 설명: 'logits' 변수에 값을 계산해서 저장해요.
    logits = X @ W + b
    # 설명: 소프트맥스 출력 등 각 클래스의 확률 배열을 정의해요.
    probs = softmax(logits)
    # 설명: 'y_oh' 변수에 값을 계산해서 저장해요.
    y_oh = one_hot(y, 2)

    # 설명: 'n' 변수에 값을 계산해서 저장해요.
    n = X.shape[0]
    # 설명: 'dlogits' 변수에 값을 계산해서 저장해요.
    dlogits = (probs - y_oh) / n
    # 설명: 'dW' 변수에 값을 계산해서 저장해요.
    dW = X.T @ dlogits
    # 설명: 배열 원소의 합계를 계산해요.
    db = np.sum(dlogits, axis=0, keepdims=True)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter26",
        # 설명: 이 코드를 실행해요.
        "topic": "역전파 기울기",
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "probs": np.round(probs, 4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "dW": np.round(dW, 4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "db": np.round(db, 4).tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
