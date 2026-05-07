# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""경사하강법 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "경사하강법은 기울기를 따라 손실이 줄어드는 방향으로 조금씩 이동한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "2차 함수의 최소점으로 이동하는 과정을 기록한다."


# 설명: '_loss' 함수를 정의해요.
def _loss(x: float) -> float:
    # 설명: '(x - 3.0) ** 2 + 2.0'을(를) 함수 호출 측에 반환해요.
    return (x - 3.0) ** 2 + 2.0


# 설명: '_grad' 함수를 정의해요.
def _grad(x: float) -> float:
    # 설명: '2.0 * (x - 3.0)'을(를) 함수 호출 측에 반환해요.
    return 2.0 * (x - 3.0)


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'lr' 변수에 값을 계산해서 저장해요.
    lr = 0.2
    # 설명: 'steps' 변수에 값을 계산해서 저장해요.
    steps = 15
    # 설명: 'x' 변수에 값을 계산해서 저장해요.
    x = -5.0

    # 설명: 'trajectory' 변수에 값을 계산해서 저장해요.
    trajectory = []
    # 설명: 'range(steps)'의 각 원소를 'step'로 받으며 반복해요.
    for step in range(steps):
        # 설명: 'g' 변수에 값을 계산해서 저장해요.
        g = _grad(x)
        # 설명: 'x' 변수에 값을 계산해서 저장해요.
        x = x - lr * g
        # 설명: 이 코드를 실행해요.
        trajectory.append(
            # 설명: 이 코드를 실행해요.
            {
                # 설명: 이 코드를 실행해요.
                "step": step + 1,
                # 설명: 값을 부동소수점(실수)형으로 변환해요.
                "x": round(float(x), 5),
                # 설명: 값을 부동소수점(실수)형으로 변환해요.
                "loss": round(float(_loss(x)), 5),
            # 설명: 이 코드를 실행해요.
            }
        # 설명: 이 코드를 실행해요.
        )

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter71",
        # 설명: 이 코드를 실행해요.
        "topic": "경사하강법",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "learning_rate": lr,
        # 설명: 이 코드를 실행해요.
        "start_x": -5.0,
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "end_x": round(float(x), 6),
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "end_loss": round(float(_loss(x)), 6),
        # 설명: 이 코드를 실행해요.
        "trajectory": trajectory,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
