"""CNN으로 주가 패턴 필터링"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = "CNN은 최근 주가 패턴을 작은 필터로 훑으며 돌파 직전 모양 같은 국소 구조를 잡아낼 수 있다."
PRACTICE_30MIN = "5일 가격/거래량 변화를 4x4 패턴 맵으로 만들고 합성곱, ReLU, 풀링이 어떤 신호를 남기는지 확인한다."


def conv2d_valid(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    h, w = image.shape
    kh, kw = kernel.shape
    out = np.zeros((h - kh + 1, w - kw + 1))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            patch = image[i : i + kh, j : j + kw]
            out[i, j] = np.sum(patch * kernel)
    return out


def max_pool2d(feature_map: np.ndarray, size: int = 2, stride: int = 1) -> np.ndarray:
    h, w = feature_map.shape
    out = np.zeros(((h - size) // stride + 1, (w - size) // stride + 1))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            block = feature_map[i * stride : i * stride + size, j * stride : j * stride + size]
            out[i, j] = np.max(block)
    return out


def run() -> dict:
    pattern_map = np.array(
        [
            [0.012, 0.018, 0.011, 0.026],
            [0.004, 0.015, 0.021, 0.019],
            [-0.003, 0.009, 0.017, 0.022],
            [0.006, 0.014, 0.024, 0.028],
        ],
        dtype=float,
    )
    kernel = np.array(
        [
            [-1.0, 0.0, 1.0],
            [-0.5, 0.0, 0.5],
            [-1.0, 0.0, 1.0],
        ],
        dtype=float,
    )

    conv_out = conv2d_valid(pattern_map, kernel)
    relu_out = np.maximum(0, conv_out)
    pool_out = max_pool2d(relu_out, size=2, stride=1)

    return {
        "chapter": "chapter30",
        "topic": "CNN으로 주가 패턴 필터링",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "input_shape": list(pattern_map.shape),
        "kernel_shape": list(kernel.shape),
        "conv_output": np.round(conv_out, 6).tolist(),
        "relu_output": np.round(relu_out, 6).tolist(),
        "pool_output": np.round(pool_out, 6).tolist(),
    }


if __name__ == "__main__":
    print(run())
