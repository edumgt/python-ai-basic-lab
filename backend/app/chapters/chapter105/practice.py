"""기업가치와 주가 예측 업사이드"""
from __future__ import annotations

import pandas as pd

LESSON_10MIN = "재무제표로 계산한 적정가치와 현재 주가 차이는 중장기 주가 예측 업사이드 신호가 될 수 있다."
PRACTICE_30MIN = "DCF로 기업가치를 계산하고 현재 가격 대비 예상 상승 여력을 구한다."


def run() -> dict:
    statement = pd.read_csv("data/financial_statements.csv")
    latest = statement.iloc[-1]
    nopat = latest["operating_income"] * (1.0 - latest["tax_rate"])
    fcf0 = nopat + latest["depreciation"] - latest["capex"] - latest["working_capital_change"]

    growth = 0.05
    discount_rate = 0.1
    terminal_growth = 0.02
    projected = [fcf0 * ((1 + growth) ** i) for i in range(1, 6)]
    pv = [cf / ((1 + discount_rate) ** i) for i, cf in enumerate(projected, start=1)]
    terminal = projected[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    enterprise_value = sum(pv) + terminal / ((1 + discount_rate) ** 5)

    shares_outstanding = 12_000_000
    fair_price = enterprise_value / shares_outstanding

    # stock_ohlcv.csv 최신 종가를 현재 주가로 사용 (파일 없으면 기본값)
    try:
        ohlcv = pd.read_csv("data/stock_ohlcv.csv")
        current_price = float(pd.to_numeric(ohlcv["close"], errors="coerce").dropna().iloc[-1])
    except (FileNotFoundError, KeyError, IndexError, ValueError):
        current_price = 71_500.0

    expected_upside = fair_price / current_price - 1

    return {
        "chapter": "chapter105",
        "topic": "기업가치와 주가 예측 업사이드",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "latest_fcf": round(float(fcf0), 4),
        "fair_price_estimate": round(float(fair_price), 4),
        "current_price_assumption": current_price,
        "expected_upside_pct": round(float(expected_upside), 6),
        "valuation_signal": "undervalued" if expected_upside > 0 else "overvalued",
    }


if __name__ == "__main__":
    print(run())
