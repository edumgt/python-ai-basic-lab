# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""크로스 엔트로피 손실 계산"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 'cross_entropy' 함수를 정의해요.
def cross_entropy(probs: np.ndarray, y_true: np.ndarray) -> float:
    # 설명: 샘플 수(데이터 개수)를 n 변수에 저장해요.
    n = len(y_true)
    # 설명: 각 샘플에서 정답 클래스에 해당하는 예측 확률을 추출해요.
    chosen = probs[np.arange(n), y_true]
    # 설명: 'float(-np.mean(np.log(chosen + 1e-12)))'을(를) 함수 호출 측에 반환해요.
    return float(-np.mean(np.log(chosen + 1e-12)))


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 소프트맥스 출력 등 각 클래스의 확률 배열을 정의해요.
    probs = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [0.70, 0.20, 0.10],
            # 설명: 이 코드를 실행해요.
            [0.05, 0.90, 0.05],
            # 설명: 이 코드를 실행해요.
            [0.15, 0.35, 0.50],
            # 설명: 이 코드를 실행해요.
            [0.60, 0.25, 0.15],
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true = np.array([0, 1, 2, 1])
    # 설명: 손실 값을 계산해서 저장해요.
    loss = cross_entropy(probs, y_true)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter25",
        # 설명: 이 코드를 실행해요.
        "topic": "크로스 엔트로피",
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "probs": probs.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "labels": y_true.tolist(),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "loss": round(loss, 6),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
