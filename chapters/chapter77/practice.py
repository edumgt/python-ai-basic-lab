# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""미니 복습 프로젝트 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "순전파와 역전파를 반복하면 작은 신경망도 점점 오차를 줄일 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "numpy로 2층 신경망을 학습해 XOR 예제를 맞춘다."


# 설명: '_sigmoid' 함수를 정의해요.
def _sigmoid(x: np.ndarray) -> np.ndarray:
    # 설명: '1.0 / (1.0 + np.exp(-x))'을(를) 함수 호출 측에 반환해요.
    return 1.0 / (1.0 + np.exp(-x))


# 설명: '_bce_loss' 함수를 정의해요.
def _bce_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    # 설명: log(0) 방지를 위한 아주 작은 값(epsilon)을 정의해요.
    eps = 1e-9
    # 설명: 'float(-np.mean(y_true * np.log(y_pred + eps) + (1 - y_true) * np.log(1 - y_pred + eps)))'을(를) 함수 호출 측에 반환해요.
    return float(-np.mean(y_true * np.log(y_pred + eps) + (1 - y_true) * np.log(1 - y_pred + eps)))


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # XOR 데이터
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    X = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [0.0, 0.0],
            # 설명: 이 코드를 실행해요.
            [0.0, 1.0],
            # 설명: 이 코드를 실행해요.
            [1.0, 0.0],
            # 설명: 이 코드를 실행해요.
            [1.0, 1.0],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    y = np.array([[0.0], [1.0], [1.0], [0.0]], dtype=float)

    # 설명: 'rng' 변수에 값을 계산해서 저장해요.
    rng = np.random.default_rng(42)
    # 설명: 'hidden_dim' 변수에 값을 계산해서 저장해요.
    hidden_dim = 3

    # 설명: 'W1' 변수에 값을 계산해서 저장해요.
    W1 = rng.normal(0, 0.5, size=(2, hidden_dim))
    # 설명: 모든 원소가 0인 NumPy 배열을 생성해요.
    b1 = np.zeros((1, hidden_dim), dtype=float)
    # 설명: 'W2' 변수에 값을 계산해서 저장해요.
    W2 = rng.normal(0, 0.5, size=(hidden_dim, 1))
    # 설명: 모든 원소가 0인 NumPy 배열을 생성해요.
    b2 = np.zeros((1, 1), dtype=float)

    # 설명: 'lr' 변수에 값을 계산해서 저장해요.
    lr = 0.8
    # 설명: 'epochs' 변수에 값을 계산해서 저장해요.
    epochs = 800

    # 초기 손실
    # 설명: 'a1_init' 변수에 값을 계산해서 저장해요.
    a1_init = _sigmoid(X @ W1 + b1)
    # 설명: 'y_hat_init' 변수에 값을 계산해서 저장해요.
    y_hat_init = _sigmoid(a1_init @ W2 + b2)
    # 설명: 손실 값을 계산해서 저장해요.
    loss_before = _bce_loss(y, y_hat_init)

    # 설명: 'range(epochs)'의 각 원소를 '_'로 받으며 반복해요.
    for _ in range(epochs):
        # 설명: 'z1' 변수에 값을 계산해서 저장해요.
        z1 = X @ W1 + b1
        # 설명: 'a1' 변수에 값을 계산해서 저장해요.
        a1 = _sigmoid(z1)
        # 설명: 'z2' 변수에 값을 계산해서 저장해요.
        z2 = a1 @ W2 + b2
        # 설명: 'y_hat' 변수에 값을 계산해서 저장해요.
        y_hat = _sigmoid(z2)

        # BCE + sigmoid gradient
        # 설명: 샘플 수(데이터 개수)를 n 변수에 저장해요.
        n = len(X)
        # 설명: 'dz2' 변수에 값을 계산해서 저장해요.
        dz2 = (y_hat - y) / n
        # 설명: 'dW2' 변수에 값을 계산해서 저장해요.
        dW2 = a1.T @ dz2
        # 설명: 'db2' 변수에 값을 계산해서 저장해요.
        db2 = dz2.sum(axis=0, keepdims=True)

        # 설명: 'da1' 변수에 값을 계산해서 저장해요.
        da1 = dz2 @ W2.T
        # 설명: 'dz1' 변수에 값을 계산해서 저장해요.
        dz1 = da1 * a1 * (1.0 - a1)
        # 설명: 'dW1' 변수에 값을 계산해서 저장해요.
        dW1 = X.T @ dz1
        # 설명: 'db1' 변수에 값을 계산해서 저장해요.
        db1 = dz1.sum(axis=0, keepdims=True)

        # 설명: 'W2 -' 변수에 값을 계산해서 저장해요.
        W2 -= lr * dW2
        # 설명: 'b2 -' 변수에 값을 계산해서 저장해요.
        b2 -= lr * db2
        # 설명: 'W1 -' 변수에 값을 계산해서 저장해요.
        W1 -= lr * dW1
        # 설명: 'b1 -' 변수에 값을 계산해서 저장해요.
        b1 -= lr * db1

    # 설명: 'a1_final' 변수에 값을 계산해서 저장해요.
    a1_final = _sigmoid(X @ W1 + b1)
    # 설명: 'y_hat_final' 변수에 값을 계산해서 저장해요.
    y_hat_final = _sigmoid(a1_final @ W2 + b2)
    # 설명: 손실 값을 계산해서 저장해요.
    loss_after = _bce_loss(y, y_hat_final)

    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = (y_hat_final >= 0.5).astype(int)
    # 설명: 평균값을 계산해요.
    acc = float((pred == y).mean())

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter77",
        # 설명: 이 코드를 실행해요.
        "topic": "미니 복습 프로젝트",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "loss_before": round(loss_before, 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "loss_after": round(loss_after, 6),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "predictions": pred.flatten().tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "target": y.astype(int).flatten().tolist(),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "accuracy": round(acc, 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
