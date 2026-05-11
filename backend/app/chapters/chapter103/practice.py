"""Transformer로 주가 수익률 attention 예측"""
from __future__ import annotations

import numpy as np

from stock_practice_utils import stock_return_sequence

LESSON_10MIN = "Transformer는 최근 수익률 전 구간을 한 번에 보고 다음 거래일 예측에 중요한 날짜를 attention으로 고른다."
PRACTICE_30MIN = "7개 시점의 주가 수익률 시퀀스에 self-attention을 적용해 다음 수익률 점수를 계산한다."


def _softmax(x: np.ndarray) -> np.ndarray:
    z = x - np.max(x)
    e = np.exp(z)
    return e / e.sum()


def run() -> dict:
    seq = stock_return_sequence(seed=52, n=20, noise=0.013)[-7:]
    q = seq[-1] * np.array([1.2, 0.6])
    keys = np.stack([seq * 0.8, seq * 1.1], axis=1)
    values = np.stack([seq, np.square(seq)], axis=1)
    scores = (keys @ q) / np.sqrt(len(q))
    weights = _softmax(scores)
    context = weights @ values
    next_score = float(0.7 * context[0] + 0.3 * context[1])

    return {
        "chapter": "chapter103",
        "topic": "Transformer로 주가 수익률 attention 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "sequence": np.round(seq, 6).tolist(),
        "attention_weights": np.round(weights, 4).tolist(),
        "most_attended_timestep": int(np.argmax(weights)),
        "context_vector": np.round(context, 6).tolist(),
        "predicted_next_return_score": round(next_score, 6),
    }


if __name__ == "__main__":
    print(run())
