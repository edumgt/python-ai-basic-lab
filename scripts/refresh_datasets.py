#!/usr/bin/env python3
"""
데이터셋 새로고침 스크립트

FinanceDataReader로 실제 KRX 시장 데이터를 가져와 data/ 아래 CSV 파일 4개를 갱신합니다.
네트워크 접속이 불가능하면 --use-fallback 플래그로 시드 기반 현실적 폴백 데이터를 사용합니다.

사용법:
    python scripts/refresh_datasets.py                    # 실데이터 (네트워크 필요)
    python scripts/refresh_datasets.py --use-fallback     # 폴백 데이터로 강제 실행
    python scripts/refresh_datasets.py --start 2024-01-01 --end 2025-01-01
    python scripts/refresh_datasets.py --dart-key YOUR_DART_KEY  # 재무제표도 갱신

갱신 파일:
    data/stock_ohlcv.csv          삼성전자(005930) 최근 1년 OHLCV
    data/stocks_features.csv      8개 종목 연간수익률·변동성·베타·PER·ROE
    data/stock_universe.csv       8개 종목 모멘텀·변동성·밸류에이션·시총
    data/financial_statements.csv 삼성·SK하이닉스 연간 재무제표
                                  (DART 키 없으면 기존 데이터에 누락 컬럼만 보완)

의존성: finance-datareader>=0.9.50 (requirements.txt에 포함)
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.dart_utils import build_dart_datasets
from backend.app.external_market_utils import build_external_datasets

# ── 대상 종목 ──────────────────────────────────────────────────────────
# (KRX 코드, 회사명, 섹터)
TICKERS: list[tuple[str, str, str]] = [
    ("005930", "삼성전자",          "semiconductor"),
    ("000660", "SK하이닉스",        "semiconductor"),
    ("035420", "NAVER",             "internet"),
    ("035720", "카카오",            "internet"),
    ("051910", "LG화학",            "battery"),
    ("373220", "LG에너지솔루션",    "battery"),
    ("105560", "KB금융",            "banking"),
    ("207940", "삼성바이오로직스",  "bio"),
]
KOSPI_TICKER = "KS11"  # FinanceDataReader KOSPI 지수 코드


def _csv_ticker(krx_code: str) -> str:
    """KRX 6자리 코드 → CSV 내 표시 형식 (기존 파일 호환)"""
    return f"{krx_code}.KS"


# ── 폴백 기초 데이터 (PER·PBR·시총·ROE, 2025년 초 추정치) ──────────
# 네트워크 없이도 stocks_features / stock_universe 를 채우기 위한 정적 값
# 시총 단위: 십억원
FALLBACK_FUNDAMENTALS: dict[str, dict] = {
    "005930": {"per": 12.5, "pbr": 1.15, "market_cap_b": 350_000, "roe": 0.095},
    "000660": {"per": 14.8, "pbr": 1.62, "market_cap_b": 120_000, "roe": 0.118},
    "035420": {"per": 22.3, "pbr": 1.18, "market_cap_b":  27_000, "roe": 0.054},
    "035720": {"per": 28.1, "pbr": 1.54, "market_cap_b":  18_000, "roe": 0.044},
    "051910": {"per": 16.2, "pbr": 0.98, "market_cap_b":  20_000, "roe": 0.062},
    "373220": {"per": 38.5, "pbr": 3.12, "market_cap_b":  72_000, "roe": 0.075},
    "105560": {"per":  6.8, "pbr": 0.52, "market_cap_b":  25_000, "roe": 0.121},
    "207940": {"per": 32.6, "pbr": 5.43, "market_cap_b":  55_000, "roe": 0.168},
}

# 폴백 가격 시계열 기준 종가 (원화, 2025년 초 기준 추정)
FALLBACK_BASE_PRICE: dict[str, float] = {
    "005930":  58_800,
    "000660": 195_000,
    "035420": 172_000,
    "035720":  38_500,
    "051910": 252_000,
    "373220": 340_000,
    "105560":  74_200,
    "207940": 710_000,
}

# ── CLI ────────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="주식 데이터셋 새로고침")
    p.add_argument("--start", default=None,
                   help="시작일 YYYY-MM-DD (기본: 종료일 -365일)")
    p.add_argument("--end", default=None,
                   help="종료일 YYYY-MM-DD (기본: 어제)")
    p.add_argument("--dart-key", default=None, metavar="KEY",
                   help="DART OpenAPI 키 (없으면 DART_API_KEY 환경변수 사용)")
    p.add_argument("--use-fallback", action="store_true",
                   help="네트워크 없이 폴백 데이터로 강제 실행")
    return p.parse_args()


# ── 데이터 취득 ────────────────────────────────────────────────────────

def _fetch_prices(ticker: str, start: str, end: str) -> pd.DataFrame | None:
    """FinanceDataReader로 가격 데이터 취득. 실패 시 None 반환."""
    try:
        import FinanceDataReader as fdr  # noqa: PLC0415

        df = fdr.DataReader(ticker, start=start, end=end)
        if df is None or df.empty:
            return None
        df = df.reset_index()
        df.columns = [str(c).lower() for c in df.columns]
        # 날짜 컬럼 정규화
        date_col = next(
            (c for c in df.columns if c in ("date", "datetime")),
            df.columns[0],
        )
        if date_col != "date":
            df = df.rename(columns={date_col: "date"})
        df["date"] = pd.to_datetime(df["date"]).dt.normalize()
        return df
    except (ImportError, OSError, ValueError, KeyError, AttributeError) as exc:
        print(f"  [WARN] {ticker} 가격 취득 실패: {exc}", file=sys.stderr)
        return None


def _generate_ohlcv_fallback(ticker: str, start: str, end: str) -> pd.DataFrame:
    """시드 난수 랜덤워크로 현실적인 OHLCV 데이터 생성.

    종목별 시드가 고정되어 있어 동일 날짜 범위에서 항상 같은 결과를 반환합니다.
    """
    base = FALLBACK_BASE_PRICE[ticker]
    dates = pd.bdate_range(start=start, end=end)
    n = len(dates)
    rng = np.random.default_rng(int(ticker) % 100_000)

    daily_ret = rng.normal(0.0003, 0.016, n)
    closes = base * np.cumprod(1 + daily_ret)
    opens = closes * (1 + rng.normal(0, 0.004, n))
    highs = np.maximum(closes, opens) * (1 + np.abs(rng.normal(0, 0.006, n)))
    lows = np.minimum(closes, opens) * (1 - np.abs(rng.normal(0, 0.006, n)))
    volumes = rng.integers(3_000_000, 18_000_000, n).astype(int)

    return pd.DataFrame({
        "date":   [d.strftime("%Y-%m-%d") for d in dates],
        "open":   opens.round(0).astype(int),
        "high":   highs.round(0).astype(int),
        "low":    lows.round(0).astype(int),
        "close":  closes.round(0).astype(int),
        "volume": volumes,
    })


# ── 지표 계산 ──────────────────────────────────────────────────────────

def _compute_beta(
    stock_closes: pd.Series,
    kospi_closes: pd.Series | None,
) -> float:
    """베타(시장 민감도) 계산. KOSPI 데이터 없으면 1.0 반환."""
    if kospi_closes is None or len(kospi_closes) < 10:
        return 1.0
    s_rets = stock_closes.pct_change().dropna().values
    k_rets = kospi_closes.pct_change().dropna().values
    n = min(len(s_rets), len(k_rets))
    if n < 10:
        return 1.0
    cov_mat = np.cov(s_rets[-n:], k_rets[-n:])
    var_k = cov_mat[1, 1]
    return round(float(cov_mat[0, 1] / var_k), 3) if var_k > 0 else 1.0


def _compute_metrics(
    df: pd.DataFrame,
    kospi_df: pd.DataFrame | None,
) -> dict:
    """price DataFrame → 지표 딕셔너리 반환."""
    close = pd.to_numeric(df["close"], errors="coerce").dropna()
    if len(close) < 2:
        return {
            "annual_return":  0.0,
            "volatility":     0.0,
            "beta":           1.0,
            "momentum_3m":    0.0,
            "volatility_20d": 0.0,
        }

    rets = close.pct_change().dropna()
    annual_return = round(float(close.iloc[-1] / close.iloc[0] - 1), 4)
    volatility = round(float(rets.std() * (252 ** 0.5)), 4)

    kospi_close = (
        pd.to_numeric(kospi_df["close"], errors="coerce").dropna()
        if kospi_df is not None and not kospi_df.empty
        else None
    )
    beta = _compute_beta(close, kospi_close)

    m3_window = min(63, len(close) - 1)
    momentum_3m = round(
        float(close.iloc[-1] / close.iloc[-(m3_window + 1)] - 1), 4
    ) if m3_window > 0 else 0.0

    v20_window = min(20, len(rets))
    volatility_20d = round(
        float(rets.iloc[-v20_window:].std() * (252 ** 0.5)), 4
    ) if v20_window > 1 else volatility

    return {
        "annual_return":  annual_return,
        "volatility":     volatility,
        "beta":           beta,
        "momentum_3m":    momentum_3m,
        "volatility_20d": volatility_20d,
    }


# ── CSV 갱신 함수 ──────────────────────────────────────────────────────

def _write_stock_ohlcv(df: pd.DataFrame, path: Path) -> None:
    """삼성전자(005930) OHLCV → data/stock_ohlcv.csv

    date/open/high/low/close/volume 컬럼만 저장합니다.
    """
    wanted = ["date", "open", "high", "low", "close", "volume"]
    cols = [c for c in wanted if c in df.columns]
    df[cols].to_csv(path, index=False)
    print(f"  ✓ {path.name} 갱신 ({len(df)}행, 삼성전자 005930)")


def _write_stocks_features(
    price_data: dict[str, pd.DataFrame],
    kospi_df: pd.DataFrame | None,
    path: Path,
) -> None:
    """종목별 수익률·변동성·베타·PER·ROE → data/stocks_features.csv"""
    rows = []
    for ticker, _name, _sector in TICKERS:
        m = _compute_metrics(price_data[ticker], kospi_df)
        fund = FALLBACK_FUNDAMENTALS[ticker]
        rows.append({
            "ticker":        _csv_ticker(ticker),
            "annual_return": m["annual_return"],
            "volatility":    m["volatility"],
            "beta":          m["beta"],
            "per":           fund["per"],
            "roe":           fund["roe"],
        })
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"  ✓ {path.name} 갱신 ({len(rows)}행)")


def _write_stock_universe(
    price_data: dict[str, pd.DataFrame],
    kospi_df: pd.DataFrame | None,
    path: Path,
) -> None:
    """종목 팩터 데이터 → data/stock_universe.csv"""
    rows = []
    for ticker, _name, sector in TICKERS:
        m = _compute_metrics(price_data[ticker], kospi_df)
        fund = FALLBACK_FUNDAMENTALS[ticker]
        rows.append({
            "ticker":         _csv_ticker(ticker),
            "sector":         sector,
            "momentum_3m":    m["momentum_3m"],
            "volatility_20d": m["volatility_20d"],
            "per":            fund["per"],
            "pbr":            fund["pbr"],
            "market_cap_b":   fund["market_cap_b"],
        })
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"  ✓ {path.name} 갱신 ({len(rows)}행)")


def _ensure_financial_statements_columns(path: Path) -> None:
    """financial_statements.csv 에 누락된 tax_rate, working_capital_change 컬럼 보완.

    chapter105 DCF 계산에 필요한 컬럼이 없으면 합리적 기본값으로 추가합니다.
    기존 컬럼과 데이터는 그대로 유지합니다.
    """
    if not path.exists():
        print(f"  [WARN] {path.name} 없음 — 건너뜀", file=sys.stderr)
        return

    df = pd.read_csv(path)
    changed = False

    if "tax_rate" not in df.columns:
        # 한국 법인세 실효세율 근사치 (약 22%)
        df["tax_rate"] = 0.22
        changed = True

    if "working_capital_change" not in df.columns:
        # 운전자본 변동 추정: 매출의 약 1~2%  (DCF 연습용 소규모 값)
        df["working_capital_change"] = (
            pd.to_numeric(df.get("revenue", pd.Series(dtype=float)), errors="coerce")
            .fillna(0) * 0.012
        ).round(0)
        changed = True

    if changed:
        df.to_csv(path, index=False)
        print(f"  ✓ {path.name} 누락 컬럼 추가 (tax_rate, working_capital_change)")
    else:
        print(f"  - {path.name} 변경 없음 (이미 최신)")


def _write_financial_statements_dart(dart_key: str, path: Path) -> None:
    """DART OpenAPI로 투자용 공시 데이터셋과 실습 재무제표를 함께 갱신합니다."""
    info = build_dart_datasets(dart_key, DATA_DIR)
    print(
        "  ✓ DART 데이터셋 갱신 "
        f"(기업 {info['company_count']}개, 재무 {info['fundamental_rows']}행, "
        f"공시 {info['disclosure_rows']}행, 투자파이프라인 {info['pipeline_rows']}행)"
    )

    fundamentals_path = DATA_DIR / "dart_fundamentals.csv"
    if not fundamentals_path.exists():
        print("  [WARN] dart_fundamentals.csv 생성 실패 — 기존 financial_statements.csv 유지", file=sys.stderr)
        _ensure_financial_statements_columns(path)
        return

    dart_df = pd.read_csv(fundamentals_path, dtype={"stock_code": str})
    dart_df["stock_code"] = dart_df["stock_code"].astype(str).str.zfill(6)
    dart_df = dart_df[dart_df["stock_code"].isin(["005930", "000660"])].copy()
    dart_df["year"] = pd.to_numeric(dart_df["year"], errors="coerce").astype("Int64")
    dart_df = dart_df[dart_df["year"].isin([2023, 2024, 2025])]
    if dart_df.empty:
        print("  [WARN] DART 재무 데이터가 비어 있어 기존 financial_statements.csv 유지", file=sys.stderr)
        _ensure_financial_statements_columns(path)
        return

    base_cols = [
        "ticker", "year", "revenue", "operating_income", "depreciation",
        "capex", "free_cash_flow", "eps", "tax_rate", "working_capital_change",
    ]
    if path.exists():
        current_df = pd.read_csv(path)
        for col in base_cols:
            if col not in current_df.columns:
                current_df[col] = np.nan
    else:
        current_df = pd.DataFrame(columns=base_cols)

    dart_view = pd.DataFrame({
        "ticker": dart_df["stock_code"].astype(str) + ".KS",
        "year": dart_df["year"].astype(int),
        "revenue": (pd.to_numeric(dart_df["revenue"], errors="coerce") / 1_000_000_000).round(0),
        "operating_income": (pd.to_numeric(dart_df["operating_income"], errors="coerce") / 1_000_000_000).round(0),
        "capex": (pd.to_numeric(dart_df["capex"], errors="coerce") / 1_000_000_000).round(0),
        "free_cash_flow": (pd.to_numeric(dart_df["free_cash_flow"], errors="coerce") / 1_000_000_000).round(0),
    })

    merged = current_df.merge(
        dart_view,
        on=["ticker", "year"],
        how="outer",
        suffixes=("", "_dart"),
    )
    for col in ["revenue", "operating_income", "capex", "free_cash_flow"]:
        merged[col] = merged[f"{col}_dart"].combine_first(merged[col])
        merged = merged.drop(columns=[f"{col}_dart"])

    merged["depreciation"] = pd.to_numeric(merged["depreciation"], errors="coerce")
    merged["depreciation"] = merged["depreciation"].fillna((pd.to_numeric(merged["capex"], errors="coerce") * 0.62).round(0))
    merged["tax_rate"] = pd.to_numeric(merged["tax_rate"], errors="coerce").fillna(0.22)
    merged["working_capital_change"] = pd.to_numeric(
        merged["working_capital_change"], errors="coerce"
    ).fillna((pd.to_numeric(merged["revenue"], errors="coerce") * 0.012).round(0))
    merged = merged[base_cols].sort_values(["ticker", "year"]).reset_index(drop=True)
    merged.to_csv(path, index=False)
    print(f"  ✓ {path.name} DART 기반 갱신 ({len(merged)}행)")


def _write_external_macro_datasets() -> None:
    """FRED + World Bank 기반 외부 거시 데이터셋 갱신."""
    info = build_external_datasets(DATA_DIR)
    print(
        "  ✓ 외부 거시 데이터셋 갱신 "
        f"(FRED {info['fred_rows']}행, World Bank {info['world_bank_rows']}행, "
        f"거시 파이프라인 {info['macro_rows']}행, ML 학습셋 {info['ml_rows']}행)"
    )


# ── 진입점 ─────────────────────────────────────────────────────────────

def main() -> None:
    args = _parse_args()
    dart_key = args.dart_key or os.getenv("DART_API_KEY")

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    end_str = args.end or yesterday
    start_str = args.start or (
        date.fromisoformat(end_str) - timedelta(days=365)
    ).isoformat()

    print(f"[refresh_datasets] 기간: {start_str} ~ {end_str}")
    print(f"  폴백 강제: {'예' if args.use_fallback else '아니오'}\n")

    # ── 가격 데이터 수집 ──────────────────────────────────────────────
    price_data: dict[str, pd.DataFrame] = {}

    for ticker, name, _sector in TICKERS:
        df: pd.DataFrame | None = None
        if not args.use_fallback:
            df = _fetch_prices(ticker, start_str, end_str)
            if df is not None:
                print(f"  ✓ {name}({ticker}) {len(df)}행 취득 [실데이터]")

        if df is None:
            if not args.use_fallback:
                print(f"  → {name}({ticker}) 폴백 데이터 사용")
            df = _generate_ohlcv_fallback(ticker, start_str, end_str)
            if args.use_fallback:
                print(f"  ✓ {name}({ticker}) {len(df)}행 생성 [폴백]")

        price_data[ticker] = df

    # KOSPI 지수 (베타 계산용)
    kospi_df: pd.DataFrame | None = None
    if not args.use_fallback:
        kospi_df = _fetch_prices(KOSPI_TICKER, start_str, end_str)
        if kospi_df is not None:
            print(f"  ✓ KOSPI({KOSPI_TICKER}) {len(kospi_df)}행 취득 [실데이터]")
        else:
            print("  → KOSPI 취득 실패 — 베타는 1.0으로 대체")

    # ── CSV 파일 갱신 ─────────────────────────────────────────────────
    print("\n[데이터셋 파일 갱신]")
    _write_stock_ohlcv(price_data["005930"], DATA_DIR / "stock_ohlcv.csv")
    _write_stocks_features(price_data, kospi_df, DATA_DIR / "stocks_features.csv")
    _write_stock_universe(price_data, kospi_df, DATA_DIR / "stock_universe.csv")

    if dart_key:
        _write_financial_statements_dart(
            dart_key, DATA_DIR / "financial_statements.csv"
        )
    else:
        _ensure_financial_statements_columns(DATA_DIR / "financial_statements.csv")

    try:
        _write_external_macro_datasets()
    except Exception as exc:  # noqa: BLE001
        print(f"  [WARN] 외부 거시 데이터셋 갱신 실패: {exc}", file=sys.stderr)

    print("\n완료.")


if __name__ == "__main__":
    main()
