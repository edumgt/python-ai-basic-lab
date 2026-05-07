# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""초기화 스케일과 L2 정규화 영향"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 'run_once' 함수를 정의해요.
def run_once(scale: float, l2: float) -> tuple[float, float]:
    # 설명: 난수 생성 시드를 고정해요 — 같은 시드이면 항상 같은 결과가 나와요.
    np.random.seed(0)
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    X = np.array([[1.0, 0.2], [0.3, 1.2], [1.3, 0.7], [0.4, 0.4]])
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    y = np.array([1, 0, 1, 0])

    # 설명: 표준 정규분포(평균 0, 표준편차 1) 난수 배열을 생성해요.
    W = np.random.randn(2, 2) * scale
    # 설명: 모든 원소가 0인 NumPy 배열을 생성해요.
    b = np.zeros((1, 2))

    # 설명: 'softmax' 함수를 정의해요.
    def softmax(logits: np.ndarray) -> np.ndarray:
        # 설명: 배열에서 가장 큰 값을 찾아요.
        s = logits - np.max(logits, axis=1, keepdims=True)
        # 설명: e의 거듭제곱(지수 함수)을 원소별로 계산해요.
        e = np.exp(s)
        # 설명: 'e / np.sum(e, axis=1, keepdims=True)'을(를) 함수 호출 측에 반환해요.
        return e / np.sum(e, axis=1, keepdims=True)

    # 설명: 'range(120)'의 각 원소를 '_'로 받으며 반복해요.
    for _ in range(120):
        # 설명: 'logits' 변수에 값을 계산해서 저장해요.
        logits = X @ W + b
        # 설명: 소프트맥스 출력 등 각 클래스의 확률 배열을 정의해요.
        probs = softmax(logits)
        # 설명: 대각선이 1이고 나머지가 0인 단위 행렬을 생성해요.
        y_oh = np.eye(2)[y]

        # 설명: 샘플 수(데이터 개수)를 n 변수에 저장해요.
        n = len(y)
        # 설명: 'dlogits' 변수에 값을 계산해서 저장해요.
        dlogits = (probs - y_oh) / n
        # 설명: 'dW' 변수에 값을 계산해서 저장해요.
        dW = X.T @ dlogits + l2 * W
        # 설명: 배열 원소의 합계를 계산해요.
        db = np.sum(dlogits, axis=0, keepdims=True)

        # 설명: 'W -' 변수에 값을 계산해서 저장해요.
        W -= 0.3 * dW
        # 설명: 'b -' 변수에 값을 계산해서 저장해요.
        b -= 0.3 * db

    # 설명: 지정 범위의 연속 정수·간격 배열을 생성해요.
    ce = -np.mean(np.log(probs[np.arange(len(y)), y] + 1e-12))
    # 설명: 배열 원소의 합계를 계산해요.
    reg = 0.5 * l2 * float(np.sum(W * W))
    # 설명: 'float(ce + reg), float(np.linalg.norm(W))'을(를) 함수 호출 측에 반환해요.
    return float(ce + reg), float(np.linalg.norm(W))


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'weak_init' 변수에 값을 계산해서 저장해요.
    weak_init = run_once(scale=0.01, l2=0.0)
    # 설명: 'strong_init' 변수에 값을 계산해서 저장해요.
    strong_init = run_once(scale=1.0, l2=0.0)
    # 설명: 'with_l2' 변수에 값을 계산해서 저장해요.
    with_l2 = run_once(scale=1.0, l2=0.1)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter29",
        # 설명: 이 코드를 실행해요.
        "topic": "초기화/정규화",
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "weak_init_loss": round(weak_init[0], 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "strong_init_loss": round(strong_init[0], 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "strong_init_weight_norm": round(strong_init[1], 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "l2_weight_norm": round(with_l2[1], 6),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
