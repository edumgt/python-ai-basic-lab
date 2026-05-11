"""로보 어드바이저 미니 프로젝트 실습 파일"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent / "data"

LESSON_10MIN = "로보 어드바이저는 위험성향과 제약조건을 코드로 명시해 의사결정을 자동화한다."
PRACTICE_30MIN = "종목 스크리닝 후 위험성향별 포트폴리오를 구성한다."


def run() -> dict:
    universe = pd.read_csv(DATA_DIR / "stock_universe.csv")

    screened = universe[(universe["momentum"] > 0.08) & (universe["pe"] < 25)].copy()
    conservative = screened.nsmallest(3, "volatility")
    aggressive = screened.nlargest(3, "momentum")

    conservative_w = [0.45, 0.35, 0.20]
    aggressive_w = [0.5, 0.3, 0.2]

    return {
        "chapter": "chapter113",
        "topic": "로보 어드바이저 미니 프로젝트",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "screened_universe": screened[["ticker", "momentum", "volatility", "pe"]].round(4).to_dict(orient="records"),
        "conservative_portfolio": [
            {"ticker": t, "weight": w}
            for t, w in zip(conservative["ticker"].tolist(), conservative_w)
        ],
        "aggressive_portfolio": [
            {"ticker": t, "weight": w}
            for t, w in zip(aggressive["ticker"].tolist(), aggressive_w)
        ],
        "rebalance_rule": "매월 말 momentum, volatility를 재계산해 비중을 재할당한다.",
    }


if __name__ == "__main__":
    print(run())
