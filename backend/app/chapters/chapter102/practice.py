"""LSTM으로 주가 수익률 시계열 예측"""
from __future__ import annotations

import numpy as np

from stock_practice_utils import stock_return_sequence

LESSON_10MIN = "LSTM은 급등락 뒤에도 중요한 수익률 정보를 셀 상태에 더 오래 저장해 다음 날 예측에 활용한다."
PRACTICE_30MIN = "단순화한 LSTM 게이트 계산으로 주가 수익률 패턴을 추적한다."


def _sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + np.exp(-x)))


def run() -> dict:
    seq = stock_return_sequence(seed=51, n=60, noise=0.015)
    h, c = 0.0, 0.0
    preds: list[float] = []

    for value in seq:
        f = _sigmoid(0.9 * h + 12 * value)
        i = _sigmoid(-0.3 * h + 14 * value)
        o = _sigmoid(0.5 * h + 10 * value)
        g = np.tanh(11 * value + 0.3 * h)
        c = f * c + i * g
        h = o * np.tanh(c)
        preds.append(float(h * 0.04))

    target = np.r_[seq[1:], seq[-1]]
    mae = float(np.mean(np.abs(target - np.array(preds))))

    return {
        "chapter": "chapter102",
        "topic": "LSTM으로 주가 수익률 시계열 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "sequence_len": int(len(seq)),
        "mae": round(mae, 6),
        "final_cell_state": round(float(c), 6),
        "final_hidden_state": round(float(h), 6),
    }


if __name__ == "__main__":
    print(run())
