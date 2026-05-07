# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""2층 신경망 fitting 루프"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 'softmax' 함수를 정의해요.
def softmax(logits: np.ndarray) -> np.ndarray:
    # 설명: 배열에서 가장 큰 값을 찾아요.
    s = logits - np.max(logits, axis=1, keepdims=True)
    # 설명: e의 거듭제곱(지수 함수)을 원소별로 계산해요.
    e = np.exp(s)
    # 설명: 'e / np.sum(e, axis=1, keepdims=True)'을(를) 함수 호출 측에 반환해요.
    return e / np.sum(e, axis=1, keepdims=True)


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
    # 설명: 난수 생성 시드를 고정해요 — 같은 시드이면 항상 같은 결과가 나와요.
    np.random.seed(7)

    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    X = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [0.2, 0.1, 0.7, 0.0],
            # 설명: 이 코드를 실행해요.
            [0.9, 0.1, 0.0, 0.3],
            # 설명: 이 코드를 실행해요.
            [0.3, 0.8, 0.2, 0.1],
            # 설명: 이 코드를 실행해요.
            [0.8, 0.2, 0.1, 0.4],
            # 설명: 이 코드를 실행해요.
            [0.1, 0.7, 0.4, 0.2],
            # 설명: 이 코드를 실행해요.
            [0.9, 0.2, 0.2, 0.8],
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    y = np.array([2, 0, 1, 0, 1, 0])
    # 설명: 'y_oh' 변수에 값을 계산해서 저장해요.
    y_oh = one_hot(y, 3)

    # 설명: 표준 정규분포(평균 0, 표준편차 1) 난수 배열을 생성해요.
    W1 = np.random.randn(4, 6) * 0.1
    # 설명: 모든 원소가 0인 NumPy 배열을 생성해요.
    b1 = np.zeros((1, 6))
    # 설명: 표준 정규분포(평균 0, 표준편차 1) 난수 배열을 생성해요.
    W2 = np.random.randn(6, 3) * 0.1
    # 설명: 모든 원소가 0인 NumPy 배열을 생성해요.
    b2 = np.zeros((1, 3))

    # 설명: 'lr' 변수에 값을 계산해서 저장해요.
    lr = 0.4
    # 설명: 손실 값을 계산해서 저장해요.
    losses = []
    # 설명: 'range(250)'의 각 원소를 '_'로 받으며 반복해요.
    for _ in range(250):
        # 설명: 'z1' 변수에 값을 계산해서 저장해요.
        z1 = X @ W1 + b1
        # 설명: 음수는 0으로, 양수는 그대로 유지하는 ReLU 활성화 함수예요.
        a1 = np.maximum(0, z1)
        # 설명: 'logits' 변수에 값을 계산해서 저장해요.
        logits = a1 @ W2 + b2
        # 설명: 소프트맥스 출력 등 각 클래스의 확률 배열을 정의해요.
        probs = softmax(logits)

        # 설명: 손실 값을 계산해서 저장해요.
        loss = -np.mean(np.sum(y_oh * np.log(probs + 1e-12), axis=1))
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        losses.append(float(loss))

        # 설명: 'n' 변수에 값을 계산해서 저장해요.
        n = X.shape[0]
        # 설명: 'dlogits' 변수에 값을 계산해서 저장해요.
        dlogits = (probs - y_oh) / n
        # 설명: 'dW2' 변수에 값을 계산해서 저장해요.
        dW2 = a1.T @ dlogits
        # 설명: 배열 원소의 합계를 계산해요.
        db2 = np.sum(dlogits, axis=0, keepdims=True)

        # 설명: 'da1' 변수에 값을 계산해서 저장해요.
        da1 = dlogits @ W2.T
        # 설명: 'dz1' 변수에 값을 계산해서 저장해요.
        dz1 = da1 * (z1 > 0)
        # 설명: 'dW1' 변수에 값을 계산해서 저장해요.
        dW1 = X.T @ dz1
        # 설명: 배열 원소의 합계를 계산해요.
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # 설명: 'W1 -' 변수에 값을 계산해서 저장해요.
        W1 -= lr * dW1
        # 설명: 'b1 -' 변수에 값을 계산해서 저장해요.
        b1 -= lr * db1
        # 설명: 'W2 -' 변수에 값을 계산해서 저장해요.
        W2 -= lr * dW2
        # 설명: 'b2 -' 변수에 값을 계산해서 저장해요.
        b2 -= lr * db2

    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = np.argmax(probs, axis=1)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter28",
        # 설명: 이 코드를 실행해요.
        "topic": "2층 신경망 fitting",
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "initial_loss": round(losses[0], 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "final_loss": round(losses[-1], 6),
        # 설명: 배열 원소의 평균값을 계산해요.
        "train_accuracy": round(float(np.mean(pred == y)), 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
