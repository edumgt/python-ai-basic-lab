"""RNN 시계열 예측 기초 실습 파일"""
from __future__ import annotations

import math
import numpy as np

LESSON_10MIN = "RNN은 hidden state를 통해 시간 의존성을 누적한다."
PRACTICE_30MIN = "단순 RNN 셀 계산으로 다음 시점 값을 예측한다."


def _series(n: int = 60) -> np.ndarray:
    x = np.arange(n)
    return np.sin(x * 0.2) + 0.1 * np.cos(x * 0.07)


def run() -> dict:
    ts = _series()
    w_x, w_h, w_y = 0.7, 0.25, 0.9
    h = 0.0
    preds = []

    for t in range(len(ts) - 1):
        h = math.tanh(w_x * ts[t] + w_h * h)
        y_hat = w_y * h
        preds.append(y_hat)

    target = ts[1:]
    pred_arr = np.array(preds)
    mae = float(np.mean(np.abs(target - pred_arr)))

    return {
        "chapter": "chapter101",
        "topic": "RNN 시계열 예측 기초",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "timesteps": int(len(ts)),
        "mae": round(mae, 6),
        "last_actual": round(float(target[-1]), 6),
        "last_pred": round(float(pred_arr[-1]), 6),
    }


if __name__ == "__main__":
    print(run())
