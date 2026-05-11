# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""역전파 감각 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "복잡한 식도 체인룰로 쪼개면 각 변수의 기여도를 계산할 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "간단한 식에서 미분값을 손계산과 수치미분으로 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # y = (a*b + c)^2
    # 설명: 'a' 변수에 값을 계산해서 저장해요.
    a = 1.5
    # 설명: 'b' 변수에 값을 계산해서 저장해요.
    b = -2.0
    # 설명: 'c' 변수에 값을 계산해서 저장해요.
    c = 0.7

    # 설명: z-점수(표준 정규 점수)를 계산해요 — (값 - 평균) / 표준편차.
    z = a * b + c
    # 설명: 'y' 변수에 값을 계산해서 저장해요.
    y = z**2

    # chain rule
    # 설명: 'dy_dz' 변수에 값을 계산해서 저장해요.
    dy_dz = 2.0 * z
    # 설명: 'dy_da' 변수에 값을 계산해서 저장해요.
    dy_da = dy_dz * b
    # 설명: 'dy_db' 변수에 값을 계산해서 저장해요.
    dy_db = dy_dz * a
    # 설명: 'dy_dc' 변수에 값을 계산해서 저장해요.
    dy_dc = dy_dz

    # 설명: log(0) 방지를 위한 아주 작은 값(epsilon)을 정의해요.
    eps = 1e-6

    # 설명: 'f' 함수를 정의해요.
    def f(aa: float, bb: float, cc: float) -> float:
        # 설명: '(aa * bb + cc) ** 2'을(를) 함수 호출 측에 반환해요.
        return (aa * bb + cc) ** 2

    # 설명: 'num_da' 변수에 값을 계산해서 저장해요.
    num_da = (f(a + eps, b, c) - f(a - eps, b, c)) / (2 * eps)
    # 설명: 'num_db' 변수에 값을 계산해서 저장해요.
    num_db = (f(a, b + eps, c) - f(a, b - eps, c)) / (2 * eps)
    # 설명: 'num_dc' 변수에 값을 계산해서 저장해요.
    num_dc = (f(a, b, c + eps) - f(a, b, c - eps)) / (2 * eps)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter72",
        # 설명: 이 코드를 실행해요.
        "topic": "역전파 감각",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "z": round(float(z), 6),
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "y": round(float(y), 6),
        # 설명: 이 코드를 실행해요.
        "analytic_grad": {
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "dy_da": round(float(dy_da), 6),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "dy_db": round(float(dy_db), 6),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "dy_dc": round(float(dy_dc), 6),
        # 설명: 이 코드를 실행해요.
        },
        # 설명: 이 코드를 실행해요.
        "numeric_grad": {
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "dy_da": round(float(num_da), 6),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "dy_db": round(float(num_db), 6),
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "dy_dc": round(float(num_dc), 6),
        # 설명: 이 코드를 실행해요.
        },
        # 설명: 값을 불리언(True/False)형으로 변환해요.
        "grad_close": bool(
            # 설명: 두 배열의 모든 원소가 허용 오차 내에서 같은지 확인해요.
            np.allclose([dy_da, dy_db, dy_dc], [num_da, num_db, num_dc], atol=1e-5)
        # 설명: 이 코드를 실행해요.
        ),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
