# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""학습률에 따른 경사하강법 비교"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations


# 설명: 'optimize' 함수를 정의해요.
def optimize(lr: float, steps: int = 25) -> list[float]:
    # 설명: 'x' 변수에 값을 계산해서 저장해요.
    x = 8.0
    # 설명: 'history' 변수에 값을 계산해서 저장해요.
    history = []
    # 설명: 'range(steps)'의 각 원소를 '_'로 받으며 반복해요.
    for _ in range(steps):
        # 설명: 'grad' 변수에 값을 계산해서 저장해요.
        grad = 2 * (x - 3)
        # 설명: 'x -' 변수에 값을 계산해서 저장해요.
        x -= lr * grad
        # 설명: 이 코드를 실행해요.
        history.append(x)
    # 설명: 'history'을(를) 함수 호출 측에 반환해요.
    return history


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'h_small' 변수에 값을 계산해서 저장해요.
    h_small = optimize(lr=0.05)
    # 설명: 'h_good' 변수에 값을 계산해서 저장해요.
    h_good = optimize(lr=0.2)
    # 설명: 'h_big' 변수에 값을 계산해서 저장해요.
    h_big = optimize(lr=1.1)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter27",
        # 설명: 이 코드를 실행해요.
        "topic": "학습률 실험",
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "final_x_small_lr": round(h_small[-1], 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "final_x_good_lr": round(h_good[-1], 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "final_x_big_lr": round(h_big[-1], 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "big_lr_first_5": [round(v, 4) for v in h_big[:5]],
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
