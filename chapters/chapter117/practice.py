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

# 계절 위상 상수 (월별 수주/착공 패턴)
HOUSING_PHASE_SHIFT = -2  # 봄철 착공 증가를 반영
ARCH_ORDER_PHASE_SHIFT = -1  # 연초 건축 발주 집중 반영
CIVIL_ORDER_PHASE_SHIFT = -4  # 토목 발주의 상대적 후행 사이클 반영

# 주가 시뮬레이션 계수
BASE_ARCH_ORDERS = 95.0
BASE_CIVIL_ORDERS = 80.0
BASE_CONSTRUCTION_CYCLE = 100.0
BASE_SAFETY_SCORE = 70.0
BASE_INTEREST_RATE = 3.0
BASE_STEEL_INDEX = 110.0
ORDER_ARCH_COEF = 12.0
ORDER_CIVIL_COEF = 8.0
CYCLE_COEF = 35.0
ACCIDENT_COUNT_COEF = -700.0
ACCIDENT_FLAG_COEF = -300.0
SAFETY_COEF = 20.0
RATE_COEF = -400.0
STEEL_COEF = -28.0
NOISE_MEAN = 30.0
NOISE_STD = 450.0


def generate_posco_ac_dataset(seed: int = 42) -> pd.DataFrame:
    """포스코A&C 주가 예측용 월별 가상 데이터셋을 생성합니다."""
    rng = np.random.default_rng(seed)

    dates = pd.date_range("2010-01", "2024-12", freq="MS")
    n_months = len(dates)
    years = dates.year.values.astype(int)
    months = dates.month.values.astype(int)
    quarters = ((months - 1) // 3 + 1).astype(int)

    covid_mask = ((years == 2020) & (months >= 2)) | ((years == 2021) & (months <= 6))
    rate_hike_mask = years >= 2022

    # --- 건설경기/거시 특성 -------------------------------------------------
    construction_cycle = np.clip(
        95
        + 10 * np.sin(2 * np.pi * np.arange(n_months) / 36)
        + np.linspace(-2, 8, n_months)
        + rng.normal(0, 2.5, n_months),
        70,
        130,
    )
    construction_cycle[covid_mask] -= 6

    steel_price_index = np.clip(
        100
        + np.linspace(0, 35, n_months)
        + 6 * np.sin(2 * np.pi * np.arange(n_months) / 24)
        + rng.normal(0, 3.5, n_months),
        80,
        170,
    )
    steel_price_index[rate_hike_mask] += 8

    housing_starts = np.clip(
        35_000
        + np.linspace(2_000, -4_000, n_months)
        + 1_500 * np.sin(2 * np.pi * (months + HOUSING_PHASE_SHIFT) / 12)
        + rng.normal(0, 1_100, n_months),
        20_000,
        50_000,
    )
    housing_starts[covid_mask] *= 0.86

    interest_rate = np.clip(
        np.linspace(2.25, 4.0, n_months) + rng.normal(0, 0.2, n_months),
        1.0,
        6.0,
    )
    interest_rate[rate_hike_mask] += 0.6

    # --- 핵심 요구 특성: 수주·재해 ------------------------------------------
    architecture_orders = np.clip(
        90
        + np.linspace(0, 25, n_months)
        + 15 * np.sin(2 * np.pi * (months + ARCH_ORDER_PHASE_SHIFT) / 12)
        + rng.normal(0, 8, n_months),
        30,
        180,
    )
    architecture_orders[covid_mask] *= 0.78

    civil_orders = np.clip(
        70
        + np.linspace(8, 18, n_months)
        + 9 * np.sin(2 * np.pi * (months + CIVIL_ORDER_PHASE_SHIFT) / 12)
        + rng.normal(0, 6, n_months),
        20,
        150,
    )

    # 안전관리 체계 강화 가정을 반영해 장기적으로 재해 발생 평균(λ)이 완만히 감소하도록 설정
    severe_accident_count = rng.poisson(lam=np.linspace(1.3, 0.7, n_months)).astype(float)
    severe_accident_count[rng.choice(n_months, size=10, replace=False)] += 1.0
    severe_accident_count = np.clip(severe_accident_count, 0, 6)

    safety_score = np.clip(
        65 + np.linspace(0, 18, n_months) - severe_accident_count * 5 + rng.normal(0, 3, n_months),
        40,
        98,
    )
    severe_accident_flag = (severe_accident_count >= 2).astype(int)

    # --- 주가 시뮬레이션 ------------------------------------------------------
    close = np.zeros(n_months)
    close[0] = 14_000.0
    for i in range(1, n_months):
        order_effect = (
            (architecture_orders[i] - BASE_ARCH_ORDERS) * ORDER_ARCH_COEF
            + (civil_orders[i] - BASE_CIVIL_ORDERS) * ORDER_CIVIL_COEF
        )
        cycle_effect = (construction_cycle[i] - BASE_CONSTRUCTION_CYCLE) * CYCLE_COEF
        accident_penalty = (
            severe_accident_count[i] * ACCIDENT_COUNT_COEF
            + severe_accident_flag[i] * ACCIDENT_FLAG_COEF
        )
        safety_effect = (safety_score[i] - BASE_SAFETY_SCORE) * SAFETY_COEF
        rate_drag = (interest_rate[i] - BASE_INTEREST_RATE) * RATE_COEF
        steel_drag = (steel_price_index[i] - BASE_STEEL_INDEX) * STEEL_COEF
        noise = rng.normal(NOISE_MEAN, NOISE_STD)
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
TRAIN_SPLIT = 0.7
MIN_SPLIT_SIZE = 10
RF_PARAMS = {"n_estimators": 220, "max_depth": 6, "min_samples_leaf": 2, "random_state": 42}
GBM_PARAMS = {
    "n_estimators": 220,
    "max_depth": 3,
    "learning_rate": 0.05,
    "subsample": 0.85,
    "random_state": 42,
}
MLP_PARAMS = {
    "hidden_layer_sizes": (64, 32),
    "activation": "relu",
    "solver": "adam",
    "learning_rate_init": 0.001,
    "max_iter": 500,
    "early_stopping": True,
    "validation_fraction": 0.15,
    "random_state": 42,
}


def run() -> dict:
    df = generate_posco_ac_dataset(seed=42)
    x = df[FEATURE_COLS].values
    y = df["target"].values

    split = int(len(x) * TRAIN_SPLIT)
    if split < MIN_SPLIT_SIZE or (len(x) - split) < MIN_SPLIT_SIZE:
        raise ValueError("학습/평가 샘플이 너무 적습니다. 데이터 생성 구간 또는 split 비율을 확인하세요.")
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]

    scaler = StandardScaler()
    x_tr = scaler.fit_transform(x_train)
    x_te = scaler.transform(x_test)

    rf = RandomForestClassifier(**RF_PARAMS)
    gbm = GradientBoostingClassifier(**GBM_PARAMS)
    mlp = MLPClassifier(**MLP_PARAMS)

    results = [
        _evaluate("RandomForest (ML)", rf, x_tr, y_train, x_te, y_test),
        _evaluate("GradientBoosting (ML)", gbm, x_tr, y_train, x_te, y_test),
        _evaluate("MLP Neural Network (DL)", mlp, x_tr, y_train, x_te, y_test),
    ]
    best = max(results, key=lambda r: r["auc"])

    if not hasattr(rf, "feature_importances_"):
        raise ValueError("RandomForest feature_importances_를 계산할 수 없습니다.")
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
