# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""회귀 지표 비교 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: mean_absolute_error, mean_squared_error, r2_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "회귀 지표는 같은 예측도 다른 시각으로 평가한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "MAE, MSE, RMSE, R2를 두 예측 결과에서 비교한다."


# 설명: '_metrics' 함수를 정의해요.
def _metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    # 설명: 평균 제곱 오차(MSE)를 계산해 저장해요.
    mse = float(mean_squared_error(y_true, y_pred))
    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 예측 오차 절댓값의 평균(MAE)을 계산해요.
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "mse": round(mse, 4),
        # 설명: 제곱근을 원소별로 계산해요.
        "rmse": round(float(np.sqrt(mse)), 4),
        # 설명: 결정계수(R²)로 모델이 분산을 얼마나 설명하는지 측정해요.
        "r2": round(float(r2_score(y_true, y_pred)), 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 실제 정답 레이블 배열을 정의해요.
    y_true = np.array([100, 120, 130, 150, 170, 160, 180], dtype=float)
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    pred_a = np.array([98, 125, 128, 148, 165, 158, 182], dtype=float)
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    pred_b = np.array([90, 135, 120, 155, 178, 150, 190], dtype=float)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter50",
        # 설명: 이 코드를 실행해요.
        "topic": "회귀 지표 비교",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "model_a": _metrics(y_true, pred_a),
        # 설명: 이 코드를 실행해요.
        "model_b": _metrics(y_true, pred_b),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
