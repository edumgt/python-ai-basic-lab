from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import pandas as pd

FRED_SERIES: list[tuple[str, str]] = [
    ("FEDFUNDS", "미국 기준금리"),
    ("CPIAUCSL", "미국 CPI"),
    ("UNRATE", "미국 실업률"),
    ("DGS10", "미국 10년 국채금리"),
    ("VIXCLS", "변동성 지수 VIX"),
    ("DCOILWTICO", "WTI 유가"),
]

WORLD_BANK_INDICATORS: list[tuple[str, str]] = [
    ("NY.GDP.MKTP.KD.ZG", "한국 GDP 성장률"),
    ("FP.CPI.TOTL.ZG", "한국 물가상승률"),
    ("SL.UEM.TOTL.ZS", "한국 실업률"),
    ("NE.EXP.GNFS.ZS", "한국 수출 비중"),
]


@dataclass(frozen=True)
class SourceRecommendation:
    name: str
    kind: str
    note: str
    key_required: bool


SOURCE_RECOMMENDATIONS: list[SourceRecommendation] = [
    SourceRecommendation("DART", "공시/재무", "한국 상장사의 공식 공시와 재무제표 수집", True),
    SourceRecommendation("FRED", "거시경제", "금리, CPI, 실업률, VIX, 유가 같은 글로벌 거시 신호 수집", False),
    SourceRecommendation("World Bank", "국가 구조지표", "한국 GDP 성장률, 수출 비중 같은 장기 구조 데이터 수집", False),
    SourceRecommendation("KOSIS", "국내 통계", "한국 산업생산, 고용, 물가 같은 국내 통계 확장", True),
    SourceRecommendation("Alpha Vantage", "가격/뉴스/기술지표", "해외 주가, 경제지표, 기술적 지표, 뉴스 감성 확장", True),
]


def _fetch_fred_series(client: httpx.Client, series_id: str, title: str) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    resp = client.get(url, timeout=45.0)
    resp.raise_for_status()
    df = pd.read_csv(pd.io.common.StringIO(resp.text))
    value_col = series_id
    df = df.rename(columns={"observation_date": "date", value_col: "value"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")
    df["series_id"] = series_id
    df["title"] = title
    return df[["date", "series_id", "title", "value"]]


def build_fred_dataset(client: httpx.Client) -> pd.DataFrame:
    frames = [_fetch_fred_series(client, series_id, title) for series_id, title in FRED_SERIES]
    df = pd.concat(frames, ignore_index=True)
    return df.sort_values(["series_id", "date"]).reset_index(drop=True)


def build_fred_monthly_features(fred_df: pd.DataFrame) -> pd.DataFrame:
    if fred_df.empty:
        return pd.DataFrame()

    wide = (
        fred_df.pivot_table(index="date", columns="series_id", values="value", aggfunc="last")
        .sort_index()
        .resample("MS")
        .mean()
    )
    wide["fred_cpi_yoy"] = wide["CPIAUCSL"].pct_change(12) * 100
    wide = wide.rename(
        columns={
            "FEDFUNDS": "fred_fedfunds",
            "UNRATE": "fred_unrate",
            "DGS10": "fred_dgs10",
            "VIXCLS": "fred_vix",
            "DCOILWTICO": "fred_oil_wti",
        }
    )
    wide = wide.reset_index().rename(columns={"date": "month"})
    wide["year"] = pd.to_datetime(wide["month"]).dt.year
    return wide


def _pick_first_non_null(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    for item in items:
        if item.get("value") is not None:
            return item
    return items[0] if items else None


def _fetch_world_bank_indicator(client: httpx.Client, indicator_id: str, title: str) -> pd.DataFrame:
    url = f"https://api.worldbank.org/v2/country/KOR/indicator/{indicator_id}"
    resp = client.get(url, params={"format": "json", "per_page": "200"}, timeout=45.0)
    resp.raise_for_status()
    payload = resp.json()
    rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
    clean_rows: list[dict[str, Any]] = []
    for row in rows:
        year = row.get("date")
        value = row.get("value")
        if year is None:
            continue
        clean_rows.append({
            "year": int(year),
            "indicator_id": indicator_id,
            "title": title,
            "value": None if value is None else float(value),
        })
    return pd.DataFrame(clean_rows).sort_values("year")


def build_world_bank_dataset(client: httpx.Client) -> pd.DataFrame:
    frames = [_fetch_world_bank_indicator(client, indicator_id, title) for indicator_id, title in WORLD_BANK_INDICATORS]
    df = pd.concat(frames, ignore_index=True)
    return df.sort_values(["indicator_id", "year"]).reset_index(drop=True)


def build_world_bank_wide(world_bank_df: pd.DataFrame) -> pd.DataFrame:
    if world_bank_df.empty:
        return pd.DataFrame()
    wide = world_bank_df.pivot_table(index="year", columns="indicator_id", values="value", aggfunc="last").reset_index()
    return wide.rename(
        columns={
            "NY.GDP.MKTP.KD.ZG": "wb_gdp_growth",
            "FP.CPI.TOTL.ZG": "wb_cpi_inflation",
            "SL.UEM.TOTL.ZS": "wb_unemployment",
            "NE.EXP.GNFS.ZS": "wb_exports_gdp",
        }
    )


def build_external_macro_pipeline(
    fred_monthly_df: pd.DataFrame,
    world_bank_wide_df: pd.DataFrame,
) -> pd.DataFrame:
    if fred_monthly_df.empty:
        return pd.DataFrame()
    annual = (
        fred_monthly_df.groupby("year")[
            ["fred_fedfunds", "fred_cpi_yoy", "fred_unrate", "fred_dgs10", "fred_vix", "fred_oil_wti"]
        ]
        .mean()
        .reset_index()
    )
    if not world_bank_wide_df.empty:
        annual = annual.merge(world_bank_wide_df, on="year", how="left")
    return annual.sort_values("year").reset_index(drop=True)


def build_external_invest_ml_dataset(data_dir: Path, macro_pipeline_df: pd.DataFrame | None = None) -> pd.DataFrame:
    fundamentals_path = data_dir / "dart_fundamentals.csv"
    if not fundamentals_path.exists():
        return pd.DataFrame()

    fundamentals = pd.read_csv(fundamentals_path, dtype={"stock_code": str, "corp_code": str})
    fundamentals["stock_code"] = fundamentals["stock_code"].astype(str).str.zfill(6)
    fundamentals = fundamentals.sort_values(["stock_code", "year"]).reset_index(drop=True)
    if macro_pipeline_df is None:
        macro_path = data_dir / "external_macro_pipeline.csv"
        if not macro_path.exists():
            return pd.DataFrame()
        macro_df = pd.read_csv(macro_path)
    else:
        macro_df = macro_pipeline_df.copy()
    macro_df["year"] = pd.to_numeric(macro_df["year"], errors="coerce").astype("Int64")
    panel = fundamentals.merge(macro_df, on="year", how="left")

    panel["next_revenue_yoy"] = panel.groupby("stock_code")["revenue_yoy"].shift(-1)
    panel["next_operating_income_yoy"] = panel.groupby("stock_code")["operating_income_yoy"].shift(-1)
    panel["label_next_revenue_up"] = pd.Series(
        [pd.NA if pd.isna(value) else int(value > 0) for value in panel["next_revenue_yoy"]],
        dtype="Int64",
    )
    panel["label_next_income_up"] = pd.Series(
        [pd.NA if pd.isna(value) else int(value > 0) for value in panel["next_operating_income_yoy"]],
        dtype="Int64",
    )
    panel = panel.dropna(subset=["label_next_revenue_up", "label_next_income_up"])
    panel["label_next_revenue_up"] = panel["label_next_revenue_up"].astype(int)
    panel["label_next_income_up"] = panel["label_next_income_up"].astype(int)
    panel["macro_story"] = panel.apply(
        lambda row: (
            f"금리 {row.get('fred_fedfunds', float('nan')):.2f}, "
            f"물가 {row.get('fred_cpi_yoy', float('nan')):.2f}, "
            f"VIX {row.get('fred_vix', float('nan')):.2f}"
        ),
        axis=1,
    )
    return panel.reset_index(drop=True)


def build_external_datasets(data_dir: Path) -> dict[str, Any]:
    with httpx.Client() as client:
        fred_df = build_fred_dataset(client)
        fred_monthly = build_fred_monthly_features(fred_df)
        world_bank_df = build_world_bank_dataset(client)
        world_bank_wide = build_world_bank_wide(world_bank_df)

    macro_pipeline = build_external_macro_pipeline(fred_monthly, world_bank_wide)
    ml_dataset = build_external_invest_ml_dataset(data_dir, macro_pipeline_df=macro_pipeline)

    fred_df.to_csv(data_dir / "macro_fred_signals.csv", index=False)
    world_bank_df.to_csv(data_dir / "world_bank_korea_indicators.csv", index=False)
    macro_pipeline.to_csv(data_dir / "external_macro_pipeline.csv", index=False)
    ml_dataset.to_csv(data_dir / "external_invest_ml_dataset.csv", index=False)

    return {
        "fred_rows": int(len(fred_df)),
        "world_bank_rows": int(len(world_bank_df)),
        "macro_rows": int(len(macro_pipeline)),
        "ml_rows": int(len(ml_dataset)),
        "sources": [item.__dict__ for item in SOURCE_RECOMMENDATIONS],
    }
