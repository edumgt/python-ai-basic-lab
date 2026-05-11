# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""학습률의 영향 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations


# 설명: '_loss' 함수를 정의해요.
def _loss(x: float) -> float:
    # 설명: '(x - 2.0) ** 2'을(를) 함수 호출 측에 반환해요.
    return (x - 2.0) ** 2


# 설명: '_grad' 함수를 정의해요.
def _grad(x: float) -> float:
    # 설명: '2.0 * (x - 2.0)'을(를) 함수 호출 측에 반환해요.
    return 2.0 * (x - 2.0)


# 설명: '_optimize' 함수를 정의해요.
def _optimize(lr: float, steps: int = 25) -> dict:
    # 설명: 'x' 변수에 값을 계산해서 저장해요.
    x = -6.0
    # 설명: 손실 값을 계산해서 저장해요.
    losses = []
    # 설명: 'diverged' 변수에 값을 계산해서 저장해요.
    diverged = False

    # 설명: 'range(steps)'의 각 원소를 '_'로 받으며 반복해요.
    for _ in range(steps):
        # 설명: 'x -' 변수에 값을 계산해서 저장해요.
        x -= lr * _grad(x)
        # 설명: 'current_loss' 변수에 값을 계산해서 저장해요.
        current_loss = _loss(x)
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        losses.append(round(float(current_loss), 6))

        # 설명: 조건 (abs(x) > 1e6 or current_loss > 1e12)이 참인지 확인해요.
        if abs(x) > 1e6 or current_loss > 1e12:
            # 설명: 'diverged' 변수에 값을 계산해서 저장해요.
            diverged = True
            # 설명: 현재 반복문을 즉시 탈출해요.
            break

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "learning_rate": lr,
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "end_x": round(float(x), 6),
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "end_loss": round(float(_loss(x)), 6),
        # 설명: 시퀀스의 원소 개수를 반환해요.
        "steps_ran": len(losses),
        # 설명: 이 코드를 실행해요.
        "diverged": diverged,
        # 설명: 이 코드를 실행해요.
        "first_5_losses": losses[:5],
        # 설명: 이 코드를 실행해요.
        "last_5_losses": losses[-5:],
    # 설명: 이 코드를 실행해요.
    }


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'results' 변수에 값을 계산해서 저장해요.
    results = [_optimize(0.02), _optimize(0.2), _optimize(1.1)]

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter73",
        # 설명: 이 코드를 실행해요.
        "topic": "학습률의 영향",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": "학습률이 너무 작으면 느리고, 너무 크면 발산할 수 있다.",
        # 설명: 이 코드를 실행해요.
        "practice_30min": "세 가지 learning rate를 비교해 수렴/발산을 확인한다.",
        # 설명: 이 코드를 실행해요.
        "results": results,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
