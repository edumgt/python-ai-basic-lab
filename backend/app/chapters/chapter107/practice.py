"""주가 예측 전략 백테스트 성과지표"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = "주가 예측 모델은 맞힌 비율뿐 아니라 그 신호로 만든 전략 수익률과 낙폭도 함께 봐야 한다."
PRACTICE_30MIN = "예측 신호로 만든 일간 전략 수익률에서 누적수익률, MDD, Sharpe, Sortino를 계산한다."


def run() -> dict:
    market_returns = np.array([0.012, -0.004, 0.007, 0.006, -0.015, 0.011, 0.009, -0.003, 0.004, 0.008, -0.01, 0.013])
    predicted_up = np.array([1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1])
    strategy_returns = np.where(predicted_up == 1, market_returns, 0.0)
    equity = np.cumprod(1 + strategy_returns)
    running_max = np.maximum.accumulate(equity)
    drawdown = equity / running_max - 1

    mdd = float(np.min(drawdown))
    mean_r = float(np.mean(strategy_returns))
    std_r = float(np.std(strategy_returns, ddof=1))
    downside_std = float(np.std(np.minimum(strategy_returns, 0), ddof=1))
    sharpe = 0.0 if std_r == 0 else (mean_r / std_r) * np.sqrt(252)
    sortino = 0.0 if downside_std == 0 else (mean_r / downside_std) * np.sqrt(252)

    return {
        "chapter": "chapter107",
        "topic": "주가 예측 전략 백테스트 성과지표",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "signal_hit_ratio": round(float((predicted_up[market_returns > 0] == 1).mean()), 4),
        "cumulative_return": round(float(equity[-1] - 1), 6),
        "mdd": round(mdd, 6),
        "sharpe": round(float(sharpe), 6),
        "sortino": round(float(sortino), 6),
        "strategy_returns": np.round(strategy_returns, 6).tolist(),
    }


if __name__ == "__main__":
    print(run())
