from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import httpx
import pandas as pd

DART_API_BASE = "https://opendart.fss.or.kr/api"
DART_TARGETS: list[tuple[str, str, str]] = [
    ("005930", "삼성전자", "semiconductor"),
    ("000660", "SK하이닉스", "semiconductor"),
    ("035420", "NAVER", "internet"),
    ("035720", "카카오", "internet"),
    ("051910", "LG화학", "battery"),
    ("373220", "LG에너지솔루션", "battery"),
    ("105560", "KB금융", "banking"),
    ("207940", "삼성바이오로직스", "bio"),
]


@dataclass(frozen=True)
class DartTarget:
    stock_code: str
    corp_name: str
    sector: str
    corp_code: str


def default_dart_years(today: date | None = None, num_years: int = 4) -> list[int]:
    anchor = today or date.today()
    latest_year = anchor.year - 1
    return list(range(latest_year - num_years + 1, latest_year + 1))


def _clean_amount(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text in {"-", "None", "nan"}:
        return None
    text = text.replace(",", "")
    if text.startswith("(") and text.endswith(")"):
        text = f"-{text[1:-1]}"
    try:
        return float(text)
    except ValueError:
        return None


def _safe_ratio(numerator: float | None, denominator: float | None, scale: float = 100.0) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return round(float(numerator / denominator * scale), 4)


def _api_get_json(client: httpx.Client, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    resp = client.get(f"{DART_API_BASE}/{endpoint}", params=params, timeout=45.0)
    resp.raise_for_status()
    data = resp.json()
    status = data.get("status")
    if status not in {None, "000", "013"}:
        message = data.get("message", "알 수 없는 DART 오류")
        raise RuntimeError(f"DART API 오류 ({endpoint}): {status} {message}")
    return data


def _download_corp_codes(client: httpx.Client, api_key: str) -> dict[str, str]:
    resp = client.get(f"{DART_API_BASE}/corpCode.xml", params={"crtfc_key": api_key}, timeout=60.0)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        xml_name = zf.namelist()[0]
        xml_bytes = zf.read(xml_name)
    root = ET.fromstring(xml_bytes)
    mapping: dict[str, str] = {}
    for node in root.findall(".//list"):
        stock_code = (node.findtext("stock_code") or "").strip()
        corp_code = (node.findtext("corp_code") or "").strip()
        if stock_code and corp_code:
            mapping[stock_code] = corp_code
    return mapping


def resolve_dart_targets(client: httpx.Client, api_key: str) -> list[DartTarget]:
    corp_map = _download_corp_codes(client, api_key)
    results: list[DartTarget] = []
    for stock_code, corp_name, sector in DART_TARGETS:
        corp_code = corp_map.get(stock_code)
        if not corp_code:
            continue
        results.append(DartTarget(stock_code=stock_code, corp_name=corp_name, sector=sector, corp_code=corp_code))
    return results


def _fetch_company_profile(client: httpx.Client, api_key: str, target: DartTarget) -> dict[str, Any]:
    data = _api_get_json(
        client,
        "company.json",
        {"crtfc_key": api_key, "corp_code": target.corp_code},
    )
    return {
        "stock_code": target.stock_code,
        "corp_code": target.corp_code,
        "corp_name": data.get("corp_name") or target.corp_name,
        "corp_name_eng": data.get("corp_name_eng", ""),
        "sector": target.sector,
        "corp_cls": data.get("corp_cls", ""),
        "ceo_name": data.get("ceo_nm", ""),
        "industry_code": data.get("induty_code", ""),
        "established_date": data.get("est_dt", ""),
        "homepage": data.get("hm_url", ""),
        "address": data.get("adres", ""),
    }


def _match_rows(
    rows: list[dict[str, Any]],
    *,
    ids: set[str] | None = None,
    exact_names: set[str] | None = None,
    contains: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    ids = ids or set()
    exact_names = exact_names or set()
    matched: list[dict[str, Any]] = []
    for row in rows:
        account_id = str(row.get("account_id", "")).strip()
        account_nm = str(row.get("account_nm", "")).strip()
        if account_id in ids or account_nm in exact_names:
            matched.append(row)
            continue
        if contains and any(token in account_nm for token in contains):
            matched.append(row)
    return matched


def _pick_amount(
    rows: list[dict[str, Any]],
    *,
    ids: set[str] | None = None,
    exact_names: set[str] | None = None,
    contains: tuple[str, ...] = (),
) -> float | None:
    matched = _match_rows(rows, ids=ids, exact_names=exact_names, contains=contains)
    for row in matched:
        amount = _clean_amount(row.get("thstrm_amount"))
        if amount is not None:
            return amount
    return None


def _sum_abs_amounts(
    rows: list[dict[str, Any]],
    *,
    ids: set[str] | None = None,
    exact_names: set[str] | None = None,
    contains: tuple[str, ...] = (),
) -> float | None:
    matched = _match_rows(rows, ids=ids, exact_names=exact_names, contains=contains)
    values = [abs(value) for value in (_clean_amount(row.get("thstrm_amount")) for row in matched) if value is not None]
    if not values:
        return None
    return float(sum(values))


def _fetch_financial_rows(
    client: httpx.Client,
    api_key: str,
    target: DartTarget,
    year: int,
    fs_div: str = "CFS",
) -> list[dict[str, Any]]:
    payload = _api_get_json(
        client,
        "fnlttSinglAcntAll.json",
        {
            "crtfc_key": api_key,
            "corp_code": target.corp_code,
            "bsns_year": str(year),
            "reprt_code": "11011",
            "fs_div": fs_div,
        },
    )
    return payload.get("list", []) or []


def _summarize_financials(target: DartTarget, year: int, rows: list[dict[str, Any]]) -> dict[str, Any]:
    revenue = _pick_amount(
        rows,
        ids={"ifrs-full_Revenue", "ifrs_Revenue", "dart_Revenue"},
        exact_names={"매출액", "영업수익"},
    )
    operating_income = _pick_amount(
        rows,
        ids={"dart_OperatingIncomeLoss"},
        exact_names={"영업이익"},
    )
    net_income = _pick_amount(
        rows,
        ids={"ifrs-full_ProfitLoss", "ifrs_ProfitLoss"},
        exact_names={"당기순이익(손실)", "당기순이익"},
    )
    assets = _pick_amount(rows, ids={"ifrs-full_Assets"}, exact_names={"자산총계"})
    liabilities = _pick_amount(rows, ids={"ifrs-full_Liabilities"}, exact_names={"부채총계"})
    equity = _pick_amount(rows, ids={"ifrs-full_Equity"}, exact_names={"자본총계"})
    current_assets = _pick_amount(rows, ids={"ifrs-full_CurrentAssets"}, exact_names={"유동자산"})
    current_liabilities = _pick_amount(rows, ids={"ifrs-full_CurrentLiabilities"}, exact_names={"유동부채"})
    cash_and_equivalents = _pick_amount(
        rows,
        ids={"ifrs-full_CashAndCashEquivalents"},
        exact_names={"현금및현금성자산"},
    )
    inventories = _pick_amount(rows, ids={"ifrs-full_Inventories"}, exact_names={"재고자산"})
    operating_cash_flow = _pick_amount(rows, exact_names={"영업활동현금흐름"})
    investing_cash_flow = _pick_amount(rows, exact_names={"투자활동현금흐름"})
    financing_cash_flow = _pick_amount(rows, exact_names={"재무활동현금흐름"})
    capex = _sum_abs_amounts(rows, exact_names={"유형자산의 취득", "무형자산의 취득"})
    free_cash_flow = (
        float(operating_cash_flow - capex)
        if operating_cash_flow is not None and capex is not None
        else None
    )
    return {
        "stock_code": target.stock_code,
        "ticker": f"{target.stock_code}.KS",
        "corp_code": target.corp_code,
        "corp_name": target.corp_name,
        "sector": target.sector,
        "year": int(year),
        "revenue": revenue,
        "operating_income": operating_income,
        "net_income": net_income,
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "cash_and_equivalents": cash_and_equivalents,
        "inventories": inventories,
        "operating_cash_flow": operating_cash_flow,
        "investing_cash_flow": investing_cash_flow,
        "financing_cash_flow": financing_cash_flow,
        "capex": capex,
        "free_cash_flow": free_cash_flow,
        "debt_ratio": _safe_ratio(liabilities, equity),
        "current_ratio": _safe_ratio(current_assets, current_liabilities),
        "operating_margin": _safe_ratio(operating_income, revenue),
        "net_margin": _safe_ratio(net_income, revenue),
        "roe": _safe_ratio(net_income, equity),
    }


def build_dart_fundamentals(client: httpx.Client, api_key: str, years: list[int] | None = None) -> pd.DataFrame:
    years = years or default_dart_years()
    targets = resolve_dart_targets(client, api_key)
    rows: list[dict[str, Any]] = []
    for target in targets:
        for year in years:
            financial_rows = _fetch_financial_rows(client, api_key, target, year, fs_div="CFS")
            fs_div = "CFS"
            if not financial_rows:
                financial_rows = _fetch_financial_rows(client, api_key, target, year, fs_div="OFS")
                fs_div = "OFS"
            if not financial_rows:
                continue
            summary = _summarize_financials(target, year, financial_rows)
            summary["fs_div"] = fs_div
            rows.append(summary)

    df = pd.DataFrame(rows).sort_values(["stock_code", "year"]).reset_index(drop=True)
    if df.empty:
        return df

    for metric in ["revenue", "operating_income", "net_income", "free_cash_flow"]:
        prev = df.groupby("stock_code")[metric].shift(1)
        df[f"{metric}_yoy"] = ((df[metric] - prev) / prev.replace(0, pd.NA) * 100).round(4)
    for metric in ["revenue", "operating_income", "net_income", "assets", "equity", "capex", "free_cash_flow"]:
        df[f"{metric}_tn_krw"] = (df[metric] / 1_000_000_000_000).round(4)
    return df


def _categorize_report(report_name: str) -> str:
    if any(token in report_name for token in ("사업보고서", "반기보고서", "분기보고서")):
        return "earnings"
    if any(token in report_name for token in ("임원", "주요주주", "최대주주")):
        return "insider"
    if any(token in report_name for token in ("유상증자", "무상증자", "전환사채", "신주인수권")):
        return "capital"
    if "정정" in report_name:
        return "correction"
    if any(token in report_name for token in ("합병", "분할", "영업양수도", "소송")):
        return "corporate_action"
    return "general"


def build_dart_disclosures(
    client: httpx.Client,
    api_key: str,
    window_days: int = 120,
    page_count: int = 8,
) -> pd.DataFrame:
    end_dt = date.today()
    start_dt = end_dt - timedelta(days=window_days)
    targets = resolve_dart_targets(client, api_key)
    rows: list[dict[str, Any]] = []
    for target in targets:
        payload = _api_get_json(
            client,
            "list.json",
            {
                "crtfc_key": api_key,
                "corp_code": target.corp_code,
                "bgn_de": start_dt.strftime("%Y%m%d"),
                "end_de": end_dt.strftime("%Y%m%d"),
                "page_count": str(page_count),
            },
        )
        for item in payload.get("list", []) or []:
            report_name = str(item.get("report_nm", "")).strip()
            rows.append({
                "stock_code": target.stock_code,
                "ticker": f"{target.stock_code}.KS",
                "corp_code": target.corp_code,
                "corp_name": target.corp_name,
                "sector": target.sector,
                "receipt_date": item.get("rcept_dt", ""),
                "report_name": report_name,
                "report_category": _categorize_report(report_name),
                "receipt_no": item.get("rcept_no", ""),
                "filer_name": item.get("flr_nm", ""),
                "remark": item.get("rm", ""),
            })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values(["stock_code", "receipt_date"], ascending=[True, False]).reset_index(drop=True)


def _build_investment_reason(row: pd.Series) -> str:
    reasons: list[str] = []
    if pd.notna(row.get("revenue_yoy")) and row["revenue_yoy"] > 5:
        reasons.append("매출이 전년보다 커졌어요")
    if pd.notna(row.get("operating_income_yoy")) and row["operating_income_yoy"] > 5:
        reasons.append("영업이익이 더 잘 남고 있어요")
    if pd.notna(row.get("debt_ratio")) and row["debt_ratio"] < 120:
        reasons.append("빚 부담이 비교적 낮아요")
    if pd.notna(row.get("current_ratio")) and row["current_ratio"] > 100:
        reasons.append("당장 쓸 수 있는 돈이 단기 빚보다 많아요")
    if pd.notna(row.get("momentum_3m")) and row["momentum_3m"] > 0:
        reasons.append("최근 3개월 주가 흐름도 나쁘지 않아요")
    if not reasons and pd.notna(row.get("recent_disclosure_count")) and row["recent_disclosure_count"] > 0:
        reasons.append("최근 공시가 이어져서 체크할 재료가 있어요")
    if not reasons:
        reasons.append("공시 숫자를 더 지켜보며 천천히 판단하는 편이 좋아요")
    return " / ".join(reasons[:3])


def build_dart_invest_pipeline(
    fundamentals_df: pd.DataFrame,
    disclosures_df: pd.DataFrame,
    data_dir: Path,
) -> pd.DataFrame:
    if fundamentals_df.empty:
        return pd.DataFrame()

    latest = fundamentals_df.sort_values(["stock_code", "year"]).groupby("stock_code").tail(1).copy()
    latest = latest.rename(
        columns={
            "revenue_yoy": "revenue_yoy",
            "operating_income_yoy": "operating_income_yoy",
            "net_income_yoy": "net_income_yoy",
            "free_cash_flow_yoy": "free_cash_flow_yoy",
        }
    )

    universe_path = data_dir / "stock_universe.csv"
    feature_path = data_dir / "stocks_features.csv"
    if universe_path.exists():
        universe_df = pd.read_csv(universe_path)
        universe_df["stock_code"] = universe_df["ticker"].astype(str).str.replace(".KS", "", regex=False)
        latest = latest.merge(
            universe_df[["stock_code", "momentum_3m", "volatility_20d", "per", "pbr", "market_cap_b", "sector"]],
            on="stock_code",
            how="left",
            suffixes=("", "_market"),
        )
    if feature_path.exists():
        feature_df = pd.read_csv(feature_path)
        feature_df["stock_code"] = feature_df["ticker"].astype(str).str.replace(".KS", "", regex=False)
        latest = latest.merge(
            feature_df[["stock_code", "annual_return", "volatility", "beta", "roe"]],
            on="stock_code",
            how="left",
            suffixes=("", "_feature"),
        )
        latest["roe"] = latest["roe"].fillna(latest.get("roe_feature"))
        if "roe_feature" in latest.columns:
            latest = latest.drop(columns=["roe_feature"])

    if disclosures_df.empty:
        disclosure_agg = pd.DataFrame(columns=["stock_code", "recent_disclosure_count", "latest_report_name", "latest_receipt_date"])
    else:
        disclosure_agg = (
            disclosures_df.sort_values(["stock_code", "receipt_date"], ascending=[True, False])
            .groupby("stock_code")
            .agg(
                recent_disclosure_count=("receipt_no", "count"),
                latest_report_name=("report_name", "first"),
                latest_receipt_date=("receipt_date", "first"),
                latest_report_category=("report_category", "first"),
            )
            .reset_index()
        )
    latest = latest.merge(disclosure_agg, on="stock_code", how="left")

    score = pd.Series(50.0, index=latest.index)
    score += latest["revenue_yoy"].fillna(0).clip(lower=-20, upper=20).div(2)
    score += latest["operating_income_yoy"].fillna(0).clip(lower=-30, upper=30).div(2)
    score += latest["operating_margin"].fillna(0).clip(lower=0, upper=20)
    score += latest["roe"].fillna(0).clip(lower=0, upper=15)
    score += latest["momentum_3m"].fillna(0).clip(lower=-0.2, upper=0.2).mul(60)
    score -= latest["debt_ratio"].fillna(150).clip(lower=0, upper=250).sub(100).clip(lower=0).div(6)
    score -= latest["volatility"].fillna(0.3).clip(lower=0, upper=0.8).mul(18)
    score -= latest["latest_report_category"].eq("correction").fillna(False).astype(int).mul(8)
    latest["signal_score"] = score.round(1).clip(lower=0, upper=100)

    latest["investment_view"] = "중립"
    latest.loc[latest["signal_score"] >= 78, "investment_view"] = "공시상 우호적"
    latest.loc[(latest["signal_score"] >= 62) & (latest["signal_score"] < 78), "investment_view"] = "관심 관찰"
    latest.loc[latest["signal_score"] < 45, "investment_view"] = "보수 점검"
    latest["investment_reason"] = latest.apply(_build_investment_reason, axis=1)
    latest["revenue_tn_krw"] = (latest["revenue"] / 1_000_000_000_000).round(2)
    latest["operating_income_tn_krw"] = (latest["operating_income"] / 1_000_000_000_000).round(2)
    latest["net_income_tn_krw"] = (latest["net_income"] / 1_000_000_000_000).round(2)
    latest["free_cash_flow_tn_krw"] = (latest["free_cash_flow"] / 1_000_000_000_000).round(2)
    return latest.sort_values("signal_score", ascending=False).reset_index(drop=True)


def build_dart_datasets(api_key: str, data_dir: Path, years: list[int] | None = None) -> dict[str, Any]:
    with httpx.Client() as client:
        profiles = pd.DataFrame([_fetch_company_profile(client, api_key, target) for target in resolve_dart_targets(client, api_key)])
        fundamentals = build_dart_fundamentals(client, api_key, years=years)
        disclosures = build_dart_disclosures(client, api_key)

    pipeline = build_dart_invest_pipeline(fundamentals, disclosures, data_dir)
    outputs: dict[str, Any] = {
        "profiles": profiles,
        "fundamentals": fundamentals,
        "disclosures": disclosures,
        "pipeline": pipeline,
    }
    if not profiles.empty:
        profiles.to_csv(data_dir / "dart_company_profiles.csv", index=False)
    if not fundamentals.empty:
        fundamentals.to_csv(data_dir / "dart_fundamentals.csv", index=False)
    if not disclosures.empty:
        disclosures.to_csv(data_dir / "dart_disclosures.csv", index=False)
    if not pipeline.empty:
        pipeline.to_csv(data_dir / "dart_invest_pipeline.csv", index=False)
    return {
        "company_count": int(len(profiles)),
        "fundamental_rows": int(len(fundamentals)),
        "disclosure_rows": int(len(disclosures)),
        "pipeline_rows": int(len(pipeline)),
        "years": years or default_dart_years(),
    }
