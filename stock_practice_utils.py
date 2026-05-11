from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

FEATURE_POOL = [
    "close",
    "volume",
    "ret_1d",
    "ret_5d",
    "ma_5",
    "ma_20",
    "ma_gap",
    "vol_10",
    "vol_ratio",
    "range_pct",
]


def generate_stock_frame(
    seed: int = 42,
    n: int = 260,
    *,
    base_price: float = 70000.0,
    drift: float = 0.0007,
    noise: float = 0.018,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", periods=n, freq="B")
    regime = np.sin(np.linspace(0, 4 * np.pi, n)) * (noise * 0.35)
    shocks = rng.normal(drift, noise, n) + regime
    close = base_price * np.exp(np.cumsum(shocks))

    open_px = np.r_[close[0], close[:-1]] * (1 + rng.normal(0, noise * 0.18, n))
    high = np.maximum(open_px, close) * (1 + np.abs(rng.normal(noise * 0.28, noise * 0.08, n)))
    low = np.minimum(open_px, close) * (1 - np.abs(rng.normal(noise * 0.28, noise * 0.08, n)))
    volume = (
        4_500_000
        + np.abs(np.r_[0.0, np.diff(close)]) * 45
        + np.abs(shocks) * 18_000_000
        + rng.normal(0, 350_000, n)
    ).clip(900_000, None)

    return pd.DataFrame(
        {
            "date": dates,
            "open": open_px,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )


def build_stock_features(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    frame["ret_1d"] = frame["close"].pct_change()
    frame["ret_5d"] = frame["close"].pct_change(5)
    frame["ma_5"] = frame["close"].rolling(5).mean()
    frame["ma_20"] = frame["close"].rolling(20).mean()
    frame["ma_gap"] = frame["ma_5"] / frame["ma_20"] - 1
    frame["vol_10"] = frame["ret_1d"].rolling(10).std()
    frame["vol_ratio"] = frame["volume"] / frame["volume"].rolling(10).mean()
    frame["range_pct"] = (frame["high"] - frame["low"]) / frame["close"]
    frame["target_up"] = (frame["close"].shift(-1) > frame["close"]).astype(int)
    frame["target_close_next"] = frame["close"].shift(-1)
    frame["target_return_next"] = frame["close"].pct_change().shift(-1)
    return frame.dropna().reset_index(drop=True)


def make_stock_feature_frame(seed: int = 42, n: int = 260, *, noise: float = 0.018) -> pd.DataFrame:
    return build_stock_features(generate_stock_frame(seed=seed, n=n, noise=noise))


def time_split_frame(
    df: pd.DataFrame,
    features: list[str],
    target_col: str,
    *,
    test_size: float = 0.25,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    n_test = max(20, int(len(df) * test_size))
    n_test = min(n_test, len(df) - 10)
    split = len(df) - n_test
    x_train = df.iloc[:split][features]
    x_test = df.iloc[split:][features]
    y_train = df.iloc[:split][target_col]
    y_test = df.iloc[split:][target_col]
    return x_train, x_test, y_train, y_test


def top_items(values: dict[str, float], limit: int = 5) -> dict[str, float]:
    items = sorted(values.items(), key=lambda item: -abs(item[1]))[:limit]
    return {key: round(float(value), 6) for key, value in items}


def preview_records(df: pd.DataFrame, cols: list[str], tail: int = 5, digits: int = 4) -> list[dict[str, Any]]:
    preview = df[cols].tail(tail).copy()
    if "date" in preview.columns:
        preview["date"] = preview["date"].astype(str)
    numeric_cols = preview.select_dtypes(include=["number"]).columns
    preview[numeric_cols] = preview[numeric_cols].round(digits)
    return preview.to_dict(orient="records")


def stock_return_sequence(seed: int = 42, n: int = 80, *, noise: float = 0.016) -> np.ndarray:
    frame = make_stock_feature_frame(seed=seed, n=n + 25, noise=noise)
    return frame["ret_1d"].to_numpy()[:n]
