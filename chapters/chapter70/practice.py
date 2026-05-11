# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""손실함수 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "손실함수는 예측이 얼마나 틀렸는지 숫자로 알려준다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "MSE와 Cross-Entropy를 직접 계산한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 회귀 예시
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true_reg = np.array([3.0, 5.0, 2.5, 7.0], dtype=float)
    # 설명: 모델이 예측한 레이블 배열을 정의해요.
    y_pred_reg = np.array([2.8, 4.6, 3.1, 6.2], dtype=float)
    # 설명: 평균 제곱 오차(MSE)를 계산해 저장해요.
    mse = float(np.mean((y_true_reg - y_pred_reg) ** 2))

    # 분류 예시(3클래스)
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true_cls = np.array([0, 2, 1], dtype=int)
    # 설명: 모델이 각 클래스에 대해 예측한 확률 배열을 정의해요.
    y_prob = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [0.80, 0.15, 0.05],
            # 설명: 이 코드를 실행해요.
            [0.10, 0.20, 0.70],
            # 설명: 이 코드를 실행해요.
            [0.25, 0.60, 0.15],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )
    # 설명: log(0) 방지를 위한 아주 작은 값(epsilon)을 정의해요.
    eps = 1e-9
    # 설명: 각 샘플에서 정답 클래스에 해당하는 예측 확률을 추출해요.
    chosen_prob = y_prob[np.arange(len(y_true_cls)), y_true_cls]
    # 설명: 크로스 엔트로피 손실(분류 오차 척도)을 계산해요.
    cross_entropy = float(-np.mean(np.log(chosen_prob + eps)))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter70",
        # 설명: 이 코드를 실행해요.
        "topic": "손실함수",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "mse": round(mse, 6),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "cross_entropy": round(cross_entropy, 6),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "chosen_probabilities": chosen_prob.round(4).tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
