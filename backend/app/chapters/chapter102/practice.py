"""LSTM 시계열 예측 기초 실습 파일"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = "LSTM은 입력/망각/출력 게이트로 장기 의존성을 관리한다."
PRACTICE_30MIN = "간단한 LSTM 수식으로 셀 상태와 예측값 변화를 확인한다."


def _sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + np.exp(-x)))


def run() -> dict:
    x = np.linspace(-1.2, 1.2, 40)
    h, c = 0.0, 0.0
    preds: list[float] = []

    for value in x:
        f = _sigmoid(0.9 * h + 0.7 * value)
        i = _sigmoid(-0.4 * h + 0.8 * value)
        o = _sigmoid(0.6 * h + 0.5 * value)
        g = np.tanh(0.7 * value + 0.3 * h)
        c = f * c + i * g
        h = o * np.tanh(c)
        preds.append(float(h))

    target = np.tanh(0.8 * x)
    mae = float(np.mean(np.abs(target - np.array(preds))))

    return {
        "chapter": "chapter102",
        "topic": "LSTM 시계열 예측 기초",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "sequence_len": int(len(x)),
        "mae": round(mae, 6),
        "final_cell_state": round(float(c), 6),
        "final_hidden_state": round(float(h), 6),
    }


if __name__ == "__main__":
    print(run())
