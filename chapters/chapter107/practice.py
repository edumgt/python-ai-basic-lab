"""백테스트 성과지표 구현 실습 파일"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = "성과평가는 수익률과 위험(MDD·변동성)을 함께 봐야 한다."
PRACTICE_30MIN = "일간 수익률로 누적수익률, MDD, Sharpe, Sortino를 계산한다."


def run() -> dict:
    returns = np.array([0.012, -0.004, 0.007, 0.006, -0.015, 0.011, 0.009, -0.003, 0.004, 0.008, -0.01, 0.013])
    equity = np.cumprod(1 + returns)
    running_max = np.maximum.accumulate(equity)
    drawdown = equity / running_max - 1

    mdd = float(np.min(drawdown))
    mean_r = float(np.mean(returns))
    std_r = float(np.std(returns, ddof=1))
    downside_std = float(np.std(np.minimum(returns, 0), ddof=1))

    sharpe = 0.0 if std_r == 0 else (mean_r / std_r) * np.sqrt(252)
    sortino = 0.0 if downside_std == 0 else (mean_r / downside_std) * np.sqrt(252)

    return {
        "chapter": "chapter107",
        "topic": "백테스트 성과지표 구현",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "cumulative_return": round(float(equity[-1] - 1), 6),
        "mdd": round(mdd, 6),
        "sharpe": round(float(sharpe), 6),
        "sortino": round(float(sortino), 6),
        "returns": np.round(returns, 6).tolist(),
    }


if __name__ == "__main__":
    print(run())
