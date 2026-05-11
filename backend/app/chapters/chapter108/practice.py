"""예측 수익률 기반 포트폴리오 구성"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = "여러 종목의 예측 수익률이 있을 때는 어떤 종목을 얼마나 담을지까지 정해야 실제 주가 예측 전략이 된다."
PRACTICE_30MIN = "예측 수익률과 공분산으로 평균분산·리스크 패리티 가중치를 비교한다."


def _normalize(weights: np.ndarray) -> np.ndarray:
    weights = np.maximum(weights, 0)
    total = float(weights.sum())
    return weights / total if total > 0 else np.ones_like(weights) / len(weights)


def run() -> dict:
    predicted_returns = np.array([0.11, 0.082, 0.064], dtype=float)
    cov = np.array(
        [
            [0.042, 0.014, 0.009],
            [0.014, 0.025, 0.010],
            [0.009, 0.010, 0.018],
        ],
        dtype=float,
    )
    tickers = ["005930", "000660", "035420"]

    inv_cov = np.linalg.inv(cov)
    mv_weights = _normalize(inv_cov @ predicted_returns)
    vol = np.sqrt(np.diag(cov))
    rp_weights = _normalize(1.0 / vol)

    return {
        "chapter": "chapter108",
        "topic": "예측 수익률 기반 포트폴리오 구성",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "tickers": tickers,
        "predicted_returns": np.round(predicted_returns, 4).tolist(),
        "mean_variance_weights": np.round(mv_weights, 4).tolist(),
        "risk_parity_weights": np.round(rp_weights, 4).tolist(),
        "mean_variance_expected_return": round(float(mv_weights @ predicted_returns), 6),
        "risk_parity_expected_return": round(float(rp_weights @ predicted_returns), 6),
    }


if __name__ == "__main__":
    print(run())
