"""Transformer 시계열 기초 실습 파일"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = "Transformer는 순차 반복 대신 attention으로 시점 간 관계를 계산한다."
PRACTICE_30MIN = "단일 헤드 self-attention으로 최근 구간의 중요도를 계산한다."


def _softmax(x: np.ndarray) -> np.ndarray:
    z = x - np.max(x)
    e = np.exp(z)
    return e / e.sum()


def run() -> dict:
    seq = np.array([0.01, 0.02, -0.01, 0.015, 0.03, -0.005, 0.018], dtype=float)
    q = seq[-1] * np.array([1.2, 0.6])
    keys = np.stack([seq * 0.8, seq * 1.1], axis=1)
    values = np.stack([seq, np.square(seq)], axis=1)

    scores = (keys @ q) / np.sqrt(len(q))
    weights = _softmax(scores)
    context = weights @ values
    next_score = float(0.7 * context[0] + 0.3 * context[1])

    return {
        "chapter": "chapter103",
        "topic": "Transformer 시계열 기초",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "attention_weights": np.round(weights, 4).tolist(),
        "context_vector": np.round(context, 6).tolist(),
        "predicted_next_return_score": round(next_score, 6),
    }


if __name__ == "__main__":
    print(run())
