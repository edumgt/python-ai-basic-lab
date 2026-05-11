# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""초기화와 학습 안정성 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "초기 파라미터에 따라 같은 모델도 학습 속도와 안정성이 달라질 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "서로 다른 초기값으로 선형회귀를 학습해 손실 추세를 비교한다."


# 설명: '_train_linear' 함수를 정의해요.
def _train_linear(init_w: float, init_b: float, lr: float = 0.01, epochs: int = 200) -> dict:
    # 설명: 지정 범위의 연속 정수·간격 배열을 생성해요.
    x = np.arange(1, 9, dtype=float)
    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = 2.0 * x + 1.0

    # 설명: 'w' 변수에 값을 계산해서 저장해요.
    w = init_w
    # 설명: 'b' 변수에 값을 계산해서 저장해요.
    b = init_b
    # 설명: 손실 값을 계산해서 저장해요.
    losses = []

    # 설명: 샘플 수(데이터 개수)를 n 변수에 저장해요.
    n = len(x)
    # 설명: 'range(epochs)'의 각 원소를 'epoch'로 받으며 반복해요.
    for epoch in range(epochs):
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = w * x + b
        # 설명: 'err' 변수에 값을 계산해서 저장해요.
        err = pred - y
        # 설명: 손실 값을 계산해서 저장해요.
        loss = float(np.mean(err**2))

        # 설명: 배열 원소의 합계를 계산해요.
        dw = float((2.0 / n) * np.sum(err * x))
        # 설명: 배열 원소의 합계를 계산해요.
        db = float((2.0 / n) * np.sum(err))

        # 설명: 'w -' 변수에 값을 계산해서 저장해요.
        w -= lr * dw
        # 설명: 'b -' 변수에 값을 계산해서 저장해요.
        b -= lr * db

        # 설명: 조건 (epoch < 5 or epoch >= epochs - 5)이 참인지 확인해요.
        if epoch < 5 or epoch >= epochs - 5:
            # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
            losses.append(round(loss, 6))

    # 설명: 배열 원소의 평균값을 계산해요.
    final_loss = float(np.mean((w * x + b - y) ** 2))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "init": {"w": init_w, "b": init_b},
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "final": {"w": round(float(w), 5), "b": round(float(b), 5)},
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "final_loss": round(final_loss, 8),
        # 설명: 이 코드를 실행해요.
        "sampled_losses": losses,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'near_init' 변수에 값을 계산해서 저장해요.
    near_init = _train_linear(init_w=1.8, init_b=0.6)
    # 설명: 'far_init' 변수에 값을 계산해서 저장해요.
    far_init = _train_linear(init_w=-8.0, init_b=10.0)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter74",
        # 설명: 이 코드를 실행해요.
        "topic": "초기화와 학습 안정성",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "near_init_result": near_init,
        # 설명: 이 코드를 실행해요.
        "far_init_result": far_init,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
