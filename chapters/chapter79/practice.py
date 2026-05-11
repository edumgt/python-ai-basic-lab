# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""합성곱 직관 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "필터(커널)를 슬라이딩하면 경계 같은 특징을 강조할 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "간단한 edge filter를 이미지에 적용한다."


# 설명: 'conv2d_valid' 함수를 정의해요.
def conv2d_valid(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # 설명: 배열의 높이(h)와 너비(w)를 한 번에 꺼내요.
    h, w = image.shape
    # 설명: 커널의 높이(kh)와 너비(kw)를 한 번에 꺼내요.
    kh, kw = kernel.shape
    # 설명: 출력 결과를 저장할 배열을 초기화해요.
    out = np.zeros((h - kh + 1, w - kw + 1), dtype=float)

    # 설명: 'range(out.shape[0])'의 각 원소를 'i'로 받으며 반복해요.
    for i in range(out.shape[0]):
        # 설명: 'range(out.shape[1])'의 각 원소를 'j'로 받으며 반복해요.
        for j in range(out.shape[1]):
            # 설명: 현재 위치에서 커널 크기만큼 이미지 일부분(패치)을 잘라내요.
            patch = image[i : i + kh, j : j + kw]
            # 설명: 배열 원소의 합계를 계산해요.
            out[i, j] = np.sum(patch * kernel)

    # 설명: 'out'을(를) 함수 호출 측에 반환해요.
    return out


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 입력 이미지 픽셀 값을 2D 배열로 정의해요.
    image = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [10, 10, 10, 10, 10],
            # 설명: 이 코드를 실행해요.
            [10, 10, 20, 20, 20],
            # 설명: 이 코드를 실행해요.
            [10, 10, 20, 80, 80],
            # 설명: 이 코드를 실행해요.
            [10, 10, 20, 80, 80],
            # 설명: 이 코드를 실행해요.
            [10, 10, 20, 80, 80],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    edge_kernel = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [-1, -1, -1],
            # 설명: 이 코드를 실행해요.
            [0, 0, 0],
            # 설명: 이 코드를 실행해요.
            [1, 1, 1],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 합성곱(Convolution) 연산 결과를 저장해요.
    conv_out = conv2d_valid(image, edge_kernel)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter79",
        # 설명: 이 코드를 실행해요.
        "topic": "합성곱 직관",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "kernel": edge_kernel.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "conv_output": conv_out.round(2).tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
