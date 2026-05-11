"""RNN으로 주가 수익률 시계열 예측"""
from __future__ import annotations

import math
import numpy as np

from stock_practice_utils import stock_return_sequence

LESSON_10MIN = "RNN은 이전 거래일 수익률 정보를 hidden state에 저장해 다음 날 수익률 예측에 반영한다."
PRACTICE_30MIN = "단순 RNN 셀 계산으로 최근 수익률 흐름에서 다음 시점 값을 예측한다."


def run() -> dict:
    seq = stock_return_sequence(seed=50, n=70, noise=0.014)
    w_x, w_h, w_y = 0.75, 0.28, 0.92
    h = 0.0
    preds = []

    for t in range(len(seq) - 1):
        h = math.tanh(w_x * seq[t] + w_h * h)
        preds.append(w_y * h)

    target = seq[1:]
    pred_arr = np.array(preds)
    mae = float(np.mean(np.abs(target - pred_arr)))

    return {
        "chapter": "chapter101",
        "topic": "RNN으로 주가 수익률 시계열 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "timesteps": int(len(seq)),
        "mae": round(mae, 6),
        "last_actual_return": round(float(target[-1]), 6),
        "last_pred_return": round(float(pred_arr[-1]), 6),
    }


if __name__ == "__main__":
    print(run())
