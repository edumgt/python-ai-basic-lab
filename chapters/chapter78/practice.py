# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""이미지 데이터 입문 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "흑백 이미지는 2차원 숫자 배열(픽셀 밝기)로 표현된다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "numpy 배열 연산으로 반전/밝기 조절을 수행한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 입력 이미지 픽셀 값을 2D 배열로 정의해요.
    image = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [10, 30, 60, 90, 120],
            # 설명: 이 코드를 실행해요.
            [20, 40, 80, 110, 130],
            # 설명: 이 코드를 실행해요.
            [30, 60, 100, 140, 160],
            # 설명: 이 코드를 실행해요.
            [40, 70, 120, 170, 200],
            # 설명: 이 코드를 실행해요.
            [50, 80, 140, 190, 230],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=np.uint8,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'inverted' 변수에 값을 계산해서 저장해요.
    inverted = 255 - image
    # 설명: 배열 값을 지정된 최솟값·최댓값 범위 안으로 제한해요.
    brighter = np.clip(image.astype(np.int32) + 40, 0, 255).astype(np.uint8)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter78",
        # 설명: 이 코드를 실행해요.
        "topic": "이미지 데이터 입문",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 파이썬 리스트로 변환해요.
        "shape": list(image.shape),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "original": image.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "inverted": inverted.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "brighter": brighter.tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
