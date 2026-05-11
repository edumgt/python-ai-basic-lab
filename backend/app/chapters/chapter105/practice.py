"""재무제표 분석과 DCF 기초 실습 파일"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent / "data"

LESSON_10MIN = "재무제표는 기업의 수익성·안정성·현금창출력을 동시에 보여준다."
PRACTICE_30MIN = "FCF를 추정해 할인율로 현재가치를 계산하는 DCF를 구현한다."


def run() -> dict:
    statement = pd.read_csv(DATA_DIR / "financial_statements.csv")

    latest = statement.iloc[-1]
    nopat = latest["operating_income"] * (1.0 - latest["tax_rate"])
    fcf0 = nopat + latest["depreciation"] - latest["capex"] - latest["working_capital_change"]

    growth = 0.05
    discount_rate = 0.1
    terminal_growth = 0.02

    projected = [fcf0 * ((1 + growth) ** i) for i in range(1, 6)]
    pv = [cf / ((1 + discount_rate) ** i) for i, cf in enumerate(projected, start=1)]
    terminal = projected[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    terminal_pv = terminal / ((1 + discount_rate) ** 5)
    enterprise_value = sum(pv) + terminal_pv

    return {
        "chapter": "chapter105",
        "topic": "재무제표 분석과 DCF 기초",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "latest_fcf": round(float(fcf0), 4),
        "discount_rate": discount_rate,
        "terminal_growth": terminal_growth,
        "enterprise_value": round(float(enterprise_value), 4),
        "statement_preview": statement.to_dict(orient="records"),
    }


if __name__ == "__main__":
    print(run())
