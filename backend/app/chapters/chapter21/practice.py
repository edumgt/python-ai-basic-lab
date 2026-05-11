"""신경망으로 주가 방향성 예측"""
from __future__ import annotations

import numpy as np

from stock_practice_utils import make_stock_feature_frame

LESSON_10MIN = "신경망은 주가 수익률·이동평균 괴리·거래량 같은 힌트를 여러 층에서 조합해 상승 확률을 만든다."
PRACTICE_30MIN = "작은 2층 신경망으로 다음 날 상승 여부를 학습하며 손실 감소와 정확도 향상을 확인한다."


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def run() -> dict:
    df = make_stock_feature_frame(seed=48, n=260, noise=0.019)
    features = ["ret_1d", "ret_5d", "ma_gap", "vol_ratio"]
    x = df[features].to_numpy()
    x = (x - x.mean(axis=0)) / (x.std(axis=0) + 1e-9)
    y = df["target_up"].to_numpy().reshape(-1, 1)

    np.random.seed(42)
    w1 = np.random.randn(x.shape[1], 6) * 0.15
    b1 = np.zeros((1, 6))
    w2 = np.random.randn(6, 1) * 0.15
    b2 = np.zeros((1, 1))

    lr = 0.18
    epochs = 400
    losses = []

    for _ in range(epochs):
        z1 = x @ w1 + b1
        a1 = np.maximum(0, z1)
        z2 = a1 @ w2 + b2
        probs = _sigmoid(z2)
        loss = -np.mean(y * np.log(probs + 1e-12) + (1 - y) * np.log(1 - probs + 1e-12))
        losses.append(float(loss))

        dz2 = probs - y
        dw2 = (a1.T @ dz2) / len(x)
        db2 = np.mean(dz2, axis=0, keepdims=True)
        da1 = dz2 @ w2.T
        dz1 = da1 * (z1 > 0)
        dw1 = (x.T @ dz1) / len(x)
        db1 = np.mean(dz1, axis=0, keepdims=True)

        w2 -= lr * dw2
        b2 -= lr * db2
        w1 -= lr * dw1
        b1 -= lr * db1

    final_probs = _sigmoid(np.maximum(0, x @ w1 + b1) @ w2 + b2).ravel()
    pred = (final_probs >= 0.5).astype(int)
    accuracy = float((pred == y.ravel()).mean())

    return {
        "chapter": "chapter21",
        "topic": "신경망으로 주가 방향성 예측",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "initial_loss": round(losses[0], 6),
        "final_loss": round(losses[-1], 6),
        "train_accuracy": round(accuracy, 4),
        "weight_shapes": {"w1": list(w1.shape), "w2": list(w2.shape)},
        "latest_up_probability": round(float(final_probs[-1]), 4),
    }


if __name__ == "__main__":
    print(run())
