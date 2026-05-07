# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""이상탐지 입문 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "정상 패턴에서 많이 벗어난 값을 이상치로 볼 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "z-score를 계산해 이상치를 탐지한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    values = np.array([10, 11, 10, 12, 11, 10, 9, 10, 11, 45, 10, 9], dtype=float)

    # 설명: 데이터의 평균값을 계산해 저장해요.
    mean = float(values.mean())
    # 설명: 데이터의 표준편차를 계산해 저장해요.
    std = float(values.std())
    # 설명: z-점수(표준 정규 점수)를 계산해요 — (값 - 평균) / 표준편차.
    z = (values - mean) / (std + 1e-9)

    # 설명: 이상치 판별 기준값(임계값)을 설정해요.
    threshold = 2.0
    # 설명: 임계값을 초과한 이상치의 인덱스를 찾아요.
    outlier_idx = np.where(np.abs(z) > threshold)[0]

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter85",
        # 설명: 이 코드를 실행해요.
        "topic": "이상탐지 입문",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "mean": round(mean, 4),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "std": round(std, 4),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "z_scores": np.round(z, 4).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "outlier_indices": outlier_idx.astype(int).tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "outlier_values": values[outlier_idx].tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
