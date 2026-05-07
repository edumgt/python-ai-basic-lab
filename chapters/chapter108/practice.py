"""포트폴리오 최적화 기초 실습 파일"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = "포트폴리오 최적화는 기대수익과 공분산을 함께 고려하는 문제다."
PRACTICE_30MIN = "평균분산/리스크 패리티 가중치를 계산해 비교한다."


def _normalize(w: np.ndarray) -> np.ndarray:
    w = np.maximum(w, 0)
    s = float(w.sum())
    return w / s if s > 0 else np.ones_like(w) / len(w)


def run() -> dict:
    expected = np.array([0.10, 0.075, 0.055], dtype=float)
    cov = np.array(
        [
            [0.040, 0.012, 0.006],
            [0.012, 0.022, 0.008],
            [0.006, 0.008, 0.015],
        ],
        dtype=float,
    )

    inv_cov = np.linalg.inv(cov)
    mv_raw = inv_cov @ expected
    mv_w = _normalize(mv_raw)

    vol = np.sqrt(np.diag(cov))
    rp_w = _normalize(1.0 / vol)

    mv_ret = float(mv_w @ expected)
    mv_vol = float(np.sqrt(mv_w @ cov @ mv_w))
    rp_ret = float(rp_w @ expected)
    rp_vol = float(np.sqrt(rp_w @ cov @ rp_w))

    return {
        "chapter": "chapter108",
        "topic": "포트폴리오 최적화 기초",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "assets": ["equity", "bond", "commodity"],
        "mean_variance_weights": np.round(mv_w, 4).tolist(),
        "risk_parity_weights": np.round(rp_w, 4).tolist(),
        "mean_variance_expected_return": round(mv_ret, 6),
        "mean_variance_volatility": round(mv_vol, 6),
        "risk_parity_expected_return": round(rp_ret, 6),
        "risk_parity_volatility": round(rp_vol, 6),
    }


if __name__ == "__main__":
    print(run())
