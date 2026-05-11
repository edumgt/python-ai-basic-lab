"""포스코A&C 주가 예측 — 건설경기·중대재해·건축수주 특성 결합 ML/DL 실습"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

LESSON_10MIN = (
    "포스코A&C 주가를 건설경기 사이클, E&C 중대재해 리스크, 건축 관련 수주 건수와 "
    "기술적 지표를 결합해 예측하는 다중 요인 데이터셋 설계를 학습한다."
)
PRACTICE_30MIN = (
    "월별 가상 데이터(2010–2024)를 생성하고 RandomForest·GradientBoosting·MLP로 "
    "다음 달 주가 상승 여부를 비교 예측한다."
)


def generate_posco_ac_dataset(seed: int = 42) -> pd.DataFrame:
    """포스코A&C 주가 예측용 월별 가상 데이터셋을 생성합니다."""
    rng = np.random.default_rng(seed)

    dates = pd.date_range("2010-01", "2024-12", freq="MS")
    n = len(dates)
    years = dates.year.values.astype(int)
    months = dates.month.values.astype(int)
    quarters = ((months - 1) // 3 + 1).astype(int)

    covid_mask = ((years == 2020) & (months >= 2)) | ((years == 2021) & (months <= 6))
    rate_hike_mask = years >= 2022

    # --- 건설경기/거시 특성 -------------------------------------------------
    construction_cycle = np.clip(
        95 + 10 * np.sin(2 * np.pi * np.arange(n) / 36) + np.linspace(-2, 8, n) + rng.normal(0, 2.5, n),
        70,
        130,
    )
    construction_cycle[covid_mask] -= 6

    steel_price_index = np.clip(
        100 + np.linspace(0, 35, n) + 6 * np.sin(2 * np.pi * np.arange(n) / 24) + rng.normal(0, 3.5, n),
        80,
        170,
    )
    steel_price_index[rate_hike_mask] += 8

    housing_starts = np.clip(
        35_000 + np.linspace(2_000, -4_000, n) + 1_500 * np.sin(2 * np.pi * (months - 2) / 12) + rng.normal(0, 1_100, n),
        20_000,
        50_000,
    )
    housing_starts[covid_mask] *= 0.86

    interest_rate = np.clip(
        np.linspace(2.25, 4.0, n) + rng.normal(0, 0.2, n),
        1.0,
        6.0,
    )
    interest_rate[rate_hike_mask] += 0.6

    # --- 핵심 요구 특성: 수주·재해 ------------------------------------------
    architecture_orders = np.clip(
        90 + np.linspace(0, 25, n) + 15 * np.sin(2 * np.pi * (months - 1) / 12) + rng.normal(0, 8, n),
        30,
        180,
    )
    architecture_orders[covid_mask] *= 0.78

    civil_orders = np.clip(
        70 + np.linspace(8, 18, n) + 9 * np.sin(2 * np.pi * (months - 4) / 12) + rng.normal(0, 6, n),
        20,
        150,
    )

    severe_accident_count = np.clip(
        rng.poisson(lam=np.linspace(1.3, 0.7, n)),
        0,
        5,
    ).astype(float)
    severe_accident_count[rng.choice(n, size=10, replace=False)] += 1.0
    severe_accident_count = np.clip(severe_accident_count, 0, 6)

    safety_score = np.clip(
        65 + np.linspace(0, 18, n) - severe_accident_count * 5 + rng.normal(0, 3, n),
        40,
        98,
    )
    severe_accident_flag = (severe_accident_count >= 2).astype(int)

    # --- 주가 시뮬레이션 ------------------------------------------------------
    close = np.zeros(n)
    close[0] = 14_000.0
    for i in range(1, n):
        order_effect = (
            (architecture_orders[i] - 95) * 12
            + (civil_orders[i] - 80) * 8
        )
        cycle_effect = (construction_cycle[i] - 100) * 35
        accident_penalty = severe_accident_count[i] * -700 + severe_accident_flag[i] * -300
        safety_effect = (safety_score[i] - 70) * 20
        rate_drag = (interest_rate[i] - 3.0) * -400
        steel_drag = (steel_price_index[i] - 110) * -28
        noise = rng.normal(30, 450)
        delta = order_effect + cycle_effect + accident_penalty + safety_effect + rate_drag + steel_drag + noise
        close[i] = max(close[i - 1] + delta, 5_000.0)

    # --- DataFrame -----------------------------------------------------------
    df = pd.DataFrame(
        {
            "year": years,
            "month": months,
            "quarter": quarters,
            "construction_cycle": construction_cycle,
            "architecture_orders": architecture_orders,
            "civil_orders": civil_orders,
            "severe_accident_count": severe_accident_count,
            "severe_accident_flag": severe_accident_flag,
            "safety_score": safety_score,
            "steel_price_index": steel_price_index,
            "housing_starts": housing_starts,
            "interest_rate": interest_rate,
            "close": close,
        }
    )

    # --- 파생 특성 -----------------------------------------------------------
    df["orders_total"] = df["architecture_orders"] + df["civil_orders"]
    df["orders_yoy_pct"] = df["orders_total"].pct_change(12) * 100.0
    df["construction_cycle_3m_avg"] = df["construction_cycle"].rolling(3).mean()
    df["prev_m_close"] = df["close"].shift(1)
    df["ret_1m"] = df["close"].pct_change(1) * 100.0
    df["ret_3m"] = df["close"].pct_change(3) * 100.0
    df["ret_6m"] = df["close"].pct_change(6) * 100.0
    df["ma_3m"] = df["close"].rolling(3).mean()
    df["ma_6m"] = df["close"].rolling(6).mean()
    df["ma_gap_3_6"] = (df["ma_3m"] / df["ma_6m"] - 1) * 100.0
    df["volatility_6m"] = df["close"].pct_change().rolling(6).std() * 100.0
    df["accident_3m_sum"] = df["severe_accident_count"].rolling(3).sum()

    # 타겟: 다음 달 주가 상승 여부
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)
    return df.dropna().reset_index(drop=True)


def _evaluate(name: str, model, x_train, y_train, x_test, y_test) -> dict:
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]
    acc = float(accuracy_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    try:
        auc = float(roc_auc_score(y_test, y_prob))
    except ValueError:
        auc = 0.5
    return {"model": name, "accuracy": round(acc, 4), "f1": round(f1, 4), "auc": round(auc, 4)}


FEATURE_COLS = [
    "construction_cycle",
    "construction_cycle_3m_avg",
    "architecture_orders",
    "civil_orders",
    "orders_total",
    "orders_yoy_pct",
    "severe_accident_count",
    "severe_accident_flag",
    "accident_3m_sum",
    "safety_score",
    "steel_price_index",
    "housing_starts",
    "interest_rate",
    "month",
    "quarter",
    "prev_m_close",
    "ret_1m",
    "ret_3m",
    "ret_6m",
    "ma_3m",
    "ma_6m",
    "ma_gap_3_6",
    "volatility_6m",
]


def run() -> dict:
    df = generate_posco_ac_dataset(seed=42)
    x = df[FEATURE_COLS].values
    y = df["target"].values

    split = int(len(x) * 0.7)
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]

    scaler = StandardScaler()
    x_tr = scaler.fit_transform(x_train)
    x_te = scaler.transform(x_test)

    rf = RandomForestClassifier(n_estimators=220, max_depth=6, min_samples_leaf=2, random_state=42)
    gbm = GradientBoostingClassifier(
        n_estimators=220, max_depth=3, learning_rate=0.05, subsample=0.85, random_state=42
    )
    mlp = MLPClassifier(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        solver="adam",
        learning_rate_init=0.001,
        max_iter=500,
        early_stopping=True,
        validation_fraction=0.15,
        random_state=42,
    )

    results = [
        _evaluate("RandomForest (ML)", rf, x_tr, y_train, x_te, y_test),
        _evaluate("GradientBoosting (ML)", gbm, x_tr, y_train, x_te, y_test),
        _evaluate("MLP Neural Network (DL)", mlp, x_tr, y_train, x_te, y_test),
    ]
    best = max(results, key=lambda r: r["auc"])

    top_features = sorted(zip(FEATURE_COLS, rf.feature_importances_), key=lambda item: -item[1])[:5]
    latest = df.iloc[-1]

    return {
        "chapter": "chapter117",
        "topic": "포스코A&C 주가 예측 (건설경기·중대재해·건축수주 특성 결합)",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "n_samples": int(len(df)),
        "n_features": int(len(FEATURE_COLS)),
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
        "model_comparison": results,
        "best_model": best,
        "top5_features_rf": [{"feature": k, "importance": round(float(v), 4)} for k, v in top_features],
        "latest_month_summary": {
            "year": int(latest["year"]),
            "month": int(latest["month"]),
            "construction_cycle": round(float(latest["construction_cycle"]), 2),
            "architecture_orders": int(latest["architecture_orders"]),
            "severe_accident_count": int(latest["severe_accident_count"]),
            "close": round(float(latest["close"]), 2),
        },
        "insight": (
            "건축 수주 건수와 건설경기 지수가 상승할수록 주가 예측 확률이 개선되고, "
            "중대재해 발생 건수는 하방 리스크로 반영됩니다."
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), ensure_ascii=False, indent=2))
