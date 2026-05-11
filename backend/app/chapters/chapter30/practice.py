"""CNN 핵심 연산 구현"""
from __future__ import annotations

import numpy as np

# 10분 핵심 개념: CNN이 이미지를 처리하는 세 단계
LESSON_10MIN = (
    "CNN은 합성곱(Convolution) 필터로 공간 패턴을 추출하고, "
    "ReLU로 의미 없는 음수를 제거한 뒤, 풀링으로 크기를 줄인다."
)

# 30분 실습 목표: 각 단계를 직접 숫자로 확인
PRACTICE_30MIN = (
    "4×4 이미지에 3×3 에지 검출 커널을 적용해 합성곱 → ReLU → 최대풀링 "
    "세 단계를 손으로 계산하며 특성 맵이 어떻게 변하는지 확인한다."
)


def conv2d_valid(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """합성곱(Convolution) 연산 — 'valid' 패딩: 테두리 밖으로 나가지 않는 위치만 계산.

    커널을 이미지 위에서 한 칸씩 슬라이딩하며,
    겹치는 영역(패치)과 커널을 원소별로 곱한 뒤 합산한다.
    결과 크기 = (이미지 크기 - 커널 크기 + 1).
    """
    h, w = image.shape
    kh, kw = kernel.shape
    out_h, out_w = h - kh + 1, w - kw + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            # 커널 크기만큼 이미지 패치를 잘라내 커널과 원소별 곱 후 합산
            patch = image[i : i + kh, j : j + kw]
            out[i, j] = np.sum(patch * kernel)
    return out


def max_pool2d(feature_map: np.ndarray, size: int = 2, stride: int = 2) -> np.ndarray:
    """최대 풀링(Max Pooling) — 각 구역에서 가장 큰 값(가장 강한 특성)만 남긴다.

    size×size 창을 stride 간격으로 이동하며,
    창 안의 최댓값을 출력에 기록한다.
    특성 맵 크기를 줄여 연산량을 감소시키고 위치 변화에 강인하게 만든다.
    """
    h, w = feature_map.shape
    out_h = (h - size) // stride + 1
    out_w = (w - size) // stride + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            # stride 간격으로 이동한 2×2 블록에서 최댓값 선택
            block = feature_map[i * stride : i * stride + size, j * stride : j * stride + size]
            out[i, j] = np.max(block)
    return out


def run() -> dict:
    # 4×4 입력 이미지 (픽셀 밝기 값, 0~3 범위)
    image = np.array(
        [
            [1, 2, 1, 0],
            [0, 1, 3, 1],
            [2, 1, 0, 2],
            [1, 0, 2, 3],
        ],
        dtype=float,
    )

    # 3×3 수직 에지 검출 커널: 왼쪽이 밝고 오른쪽이 어두우면 양수, 반대면 음수
    kernel = np.array(
        [
            [1, 0, -1],
            [1, 0, -1],
            [1, 0, -1],
        ],
        dtype=float,
    )

    # 1단계: 합성곱 — 커널을 슬라이딩하며 각 위치에서 패턴 강도를 측정
    # 결과: 4×4 → 2×2 (valid 패딩, 커널 3×3)
    conv_out = conv2d_valid(image, kernel)

    # 2단계: ReLU 활성화 — 음수는 0으로 클리핑해 '패턴 없음'을 명확히 표현
    relu_out = np.maximum(0, conv_out)

    # 3단계: 최대 풀링 — 2×2 구역에서 가장 강한 신호만 남겨 공간 크기를 줄임
    pool_out = max_pool2d(relu_out, size=2, stride=1)

    return {
        "chapter": "chapter30",
        "topic": "CNN 핵심 연산",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "input_shape": list(image.shape),
        "kernel_shape": list(kernel.shape),
        "conv_output": conv_out.tolist(),   # 합성곱 결과 (음수 포함)
        "relu_output": relu_out.tolist(),   # ReLU 후 결과 (음수 → 0)
        "pool_output": pool_out.tolist(),   # 최대 풀링 후 결과 (크기 축소)
    }


if __name__ == "__main__":
    print(run())
