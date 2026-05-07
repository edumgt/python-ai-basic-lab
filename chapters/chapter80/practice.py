# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""풀링 직관 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "풀링은 특징맵을 작게 줄여 중요한 값만 남긴다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "max pooling을 직접 구현해 요약 결과를 확인한다."


# 설명: 'max_pool2d' 함수를 정의해요.
def max_pool2d(feature_map: np.ndarray, size: int = 2, stride: int = 2) -> np.ndarray:
    # 설명: 배열의 높이(h)와 너비(w)를 한 번에 꺼내요.
    h, w = feature_map.shape
    # 설명: 출력 높이를 계산해요 — (입력 크기 - 커널 크기) / 스트라이드 + 1.
    out_h = (h - size) // stride + 1
    # 설명: 출력 너비를 계산해요 — (입력 크기 - 커널 크기) / 스트라이드 + 1.
    out_w = (w - size) // stride + 1
    # 설명: 출력 결과를 저장할 배열을 초기화해요.
    out = np.zeros((out_h, out_w), dtype=float)

    # 설명: 'range(out_h)'의 각 원소를 'i'로 받으며 반복해요.
    for i in range(out_h):
        # 설명: 'range(out_w)'의 각 원소를 'j'로 받으며 반복해요.
        for j in range(out_w):
            # 설명: 현재 위치에서 풀링 크기만큼 특성 맵 블록을 잘라내요.
            block = feature_map[i * stride : i * stride + size, j * stride : j * stride + size]
            # 설명: 배열에서 가장 큰 값을 찾아요.
            out[i, j] = np.max(block)

    # 설명: 'out'을(를) 함수 호출 측에 반환해요.
    return out


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    feature_map = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [1, 2, 0, 1],
            # 설명: 이 코드를 실행해요.
            [3, 4, 1, 0],
            # 설명: 이 코드를 실행해요.
            [0, 2, 5, 6],
            # 설명: 이 코드를 실행해요.
            [1, 1, 2, 8],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'pooled' 변수에 값을 계산해서 저장해요.
    pooled = max_pool2d(feature_map, size=2, stride=2)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter80",
        # 설명: 이 코드를 실행해요.
        "topic": "풀링 직관",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 파이썬 리스트로 변환해요.
        "input_shape": list(feature_map.shape),
        # 설명: 값을 파이썬 리스트로 변환해요.
        "output_shape": list(pooled.shape),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "feature_map": feature_map.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "pooled": pooled.tolist(),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
