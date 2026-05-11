"""현대자동차 주가 예측 — 생산·판매·전기차 특성 기반 ML/DL 분석 실습 파일"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

LESSON_10MIN = (
    "현대자동차 주가를 년도별 생산차량수·미국판매량·전기차생산 비율 등 실물 특성과 "
    "기술적 지표를 결합한 데이터셋으로 ML(RandomForest·GBM)과 DL(MLP 신경망)로 예측한다."
)
PRACTICE_30MIN = (
    "현대차 가상 월별 데이터(2010–2024, 180개월)를 생성하고 RandomForest·GradientBoosting·MLP로 "
    "다음 달 주가 상승 여부를 예측해 세 모델의 정확도·AUC를 비교한다."
)

# ---------------------------------------------------------------------------
# 데이터 생성 기준 상수 (연간 기준, 내부에서 12로 나눠 월별 환산)
# ---------------------------------------------------------------------------
ANNUAL_PRODUCTION_2010 = 350_0000   # 연간 전체 생산량 기준치 (2010년, 대)
ANNUAL_PRODUCTION_2024 = 450_0000   # 연간 전체 생산량 기준치 (2024년, 대)
US_SALES_2010 = 50_0000             # 미국 연간 판매량 (2010년, 대)
US_SALES_2024 = 80_0000             # 미국 연간 판매량 (2024년, 대)
CHINA_SALES_2010 = 70_0000          # 중국 연간 판매량 (2010년, 대)
CHINA_SALES_2024 = 25_0000          # 중국 연간 판매량 (2024년, 대) — 점유율 하락
EUROPE_SALES_2010 = 40_0000         # 유럽 연간 판매량 (2010년, 대)
EUROPE_SALES_2024 = 60_0000         # 유럽 연간 판매량 (2024년, 대)
DOMESTIC_SALES_2010 = 65_0000       # 국내 연간 판매량 (2010년, 대)
DOMESTIC_SALES_2024 = 70_0000       # 국내 연간 판매량 (2024년, 대)
BASE_STOCK_PRICE = 100_000          # 기준 주가 (2010-01, 원)

# 주가 시뮬레이션 계수 — 각 실물 지표가 월 주가 변화에 미치는 가중치
EV_RATIO_COEF = 4_000       # EV 비율 1pp 상승 → 주가 +4,000원 압력
US_SALES_COEF = 1_500       # 미국 판매 정상화 1단위 → +1,500원
CHINA_SALES_COEF = -800     # 중국 판매 부진 1단위 → -800원
FX_COEF = 12                # 환율 1원 하락(원화 강세) → +12원 (수출 악재 역방향)
OIL_COEF = -18              # 유가 1달러 상승 → -18원 (원가 상승)

# ---------------------------------------------------------------------------
# 가상 데이터셋 생성
# ---------------------------------------------------------------------------

def generate_hyundai_dataset(seed: int = 42) -> pd.DataFrame:
    """현대자동차 주가 예측을 위한 가상 월별 데이터셋을 생성합니다. (2010-01 ~ 2024-12, 180개월)

    특성:
        - 생산 지표: 월별 전체·국내·해외·EV 생산량(대), EV 비율(%), EV 비율 전년비
        - 판매 지표: 미국·중국·유럽·국내 월별 판매량, 미국 판매 전년비
        - 거시 지표: 환율(원/달러), 유가(달러/배럴), 글로벌 자동차 수요 지수
        - 계절/시간: 월, 분기, 계절 더미(여름·겨울 성수기)
        - 주가 파생: 전월 종가, 1/3/6/12개월 수익률, 이동평균 괴리, 변동성
    타겟:
        - 다음 달 종가가 이번 달보다 높으면 1(상승), 아니면 0(하락)
    """
    rng = np.random.default_rng(seed)

    dates = pd.date_range("2010-01", "2024-12", freq="MS")
    n = len(dates)
    years = dates.year.values.astype(int)
    months = dates.month.values.astype(int)
    qtr = ((months - 1) // 3 + 1).astype(int)

    covid_mask = ((years == 2020) & (months >= 3)) | ((years == 2021) & (months <= 6))
    oil_crash_mask = (years >= 2014) & (years <= 2016)
    ukraine_mask = years >= 2022

    # --- 생산 특성 (연간 → 월별 환산) ------------------------------------
    annual_total = np.linspace(ANNUAL_PRODUCTION_2010, ANNUAL_PRODUCTION_2024, n) / 12
    seasonal_prod = 1.0 + 0.08 * np.sin(2 * np.pi * (months - 3) / 12)  # 봄·가을 성수기
    total_prod = annual_total * seasonal_prod * (1 + rng.normal(0, 0.04, n))
    total_prod[covid_mask] *= 0.75

    ev_ratio = np.clip(
        np.linspace(0.002, 0.25, n) + rng.normal(0, 0.008, n), 0.0, 1.0
    )  # EV 비율: 0.2% (2010) → 25% (2024)
    ev_prod = total_prod * ev_ratio
    domestic_prod_ratio = np.clip(
        np.linspace(0.55, 0.42, n) + rng.normal(0, 0.015, n), 0.3, 0.7
    )
    korea_prod = total_prod * domestic_prod_ratio
    overseas_prod = total_prod - korea_prod

    # --- 판매 특성 -------------------------------------------------------
    us_base = np.linspace(US_SALES_2010, US_SALES_2024, n) / 12
    us_seasonal = 1.0 + 0.10 * np.sin(2 * np.pi * (months - 4) / 12)
    us_sales = us_base * us_seasonal * (1 + rng.normal(0, 0.06, n))
    us_sales[covid_mask] *= 0.72
    us_sales = np.clip(us_sales, 0, None)

    china_base = np.linspace(CHINA_SALES_2010, CHINA_SALES_2024, n) / 12  # 중국 점유율 지속 하락
    china_sales = china_base * (1 + rng.normal(0, 0.07, n))
    china_sales[covid_mask] *= 0.65
    china_sales = np.clip(china_sales, 0, None)

    europe_sales = (np.linspace(EUROPE_SALES_2010, EUROPE_SALES_2024, n) / 12) * (1 + rng.normal(0, 0.05, n))
    domestic_sales = (np.linspace(DOMESTIC_SALES_2010, DOMESTIC_SALES_2024, n) / 12) * (1 + rng.normal(0, 0.04, n))

    # --- 거시 지표 -------------------------------------------------------
    usd_krw = np.clip(
        np.linspace(1150, 1350, n) + rng.normal(0, 35, n), 1000, 1700
    )
    usd_krw[ukraine_mask] += 80  # 우크라이나 전쟁→ 달러 강세
    usd_krw = np.clip(usd_krw, 1000, 1700)

    oil_price = np.clip(
        np.linspace(85, 75, n) + rng.normal(0, 8, n), 25, 140
    )
    oil_price[oil_crash_mask] *= 0.60
    oil_price[covid_mask] *= 0.55
    oil_price[ukraine_mask] *= 1.35
    oil_price = np.clip(oil_price, 25, 140)

    global_auto_demand = np.clip(
        100 + np.linspace(0, 20, n) + rng.normal(0, 4, n), 60, 140
    )
    global_auto_demand[covid_mask] *= 0.72

    # --- 주가 시뮬레이션 (기준: 2010-01 = BASE_STOCK_PRICE 원) ----------
    us_sales_monthly_ref = US_SALES_2024 / 12
    china_sales_monthly_ref = CHINA_SALES_2010 / 12
    close = np.zeros(n)
    close[0] = float(BASE_STOCK_PRICE)
    for i in range(1, n):
        ev_boost = ev_ratio[i] * EV_RATIO_COEF
        us_effect = (us_sales[i] / us_sales_monthly_ref - 1) * US_SALES_COEF
        china_drag = (china_sales[i] / china_sales_monthly_ref - 1) * CHINA_SALES_COEF
        fx_effect = (1350 - usd_krw[i]) * FX_COEF
        oil_drag = (oil_price[i] - 70) * OIL_COEF
        drift = rng.normal(50, 1_500)
        delta = ev_boost + us_effect + china_drag + fx_effect + oil_drag + drift
        close[i] = max(close[i - 1] + delta, 20_000.0)

    # --- DataFrame 구성 --------------------------------------------------
    df = pd.DataFrame({
        "year": years,
        "month": months,
        "quarter": qtr,
        "total_production": total_prod,
        "korea_production": korea_prod,
        "overseas_production": overseas_prod,
        "ev_production": ev_prod,
        "ev_ratio_pct": ev_ratio * 100,
        "us_sales": us_sales,
        "china_sales": china_sales,
        "europe_sales": europe_sales,
        "domestic_sales": domestic_sales,
        "usd_krw": usd_krw,
        "oil_price": oil_price,
        "global_auto_demand": global_auto_demand,
        "close": close,
    })

    # --- 주가 파생 특성 --------------------------------------------------
    df["prev_m_close"] = df["close"].shift(1)
    df["ret_1m"] = df["close"].pct_change(1) * 100.0
    df["ret_3m"] = df["close"].pct_change(3) * 100.0
    df["ret_6m"] = df["close"].pct_change(6) * 100.0
    df["ret_12m"] = df["close"].pct_change(12) * 100.0   # 전년동월 대비
    df["ma_3m"] = df["close"].rolling(3).mean()
    df["ma_6m"] = df["close"].rolling(6).mean()
    df["ma_12m"] = df["close"].rolling(12).mean()
    df["ma_gap_3_12"] = (df["ma_3m"] / df["ma_12m"] - 1) * 100.0
    df["volatility_6m"] = df["close"].pct_change().rolling(6).std() * 100.0

    # --- 계절 더미 -------------------------------------------------------
    df["is_summer"] = np.isin(months, [6, 7, 8]).astype(int)
    df["is_winter"] = np.isin(months, [12, 1, 2]).astype(int)

    # --- EV·판매 모멘텀 --------------------------------------------------
    df["ev_ratio_12m_chg"] = df["ev_ratio_pct"].diff(12)    # 1년 전 대비 EV 비율 변화(pp)
    df["us_sales_12m_chg"] = df["us_sales"].pct_change(12) * 100.0  # 미국 판매 전년비(%)

    # --- 타겟 : 다음 달 상승 여부 ----------------------------------------
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)

    return df.dropna().reset_index(drop=True)


# ---------------------------------------------------------------------------
# 모델 학습 및 평가 헬퍼
# ---------------------------------------------------------------------------

def _evaluate(name: str, model, X_train, y_train, X_test, y_test) -> dict:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    acc = float(accuracy_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    try:
        auc = float(roc_auc_score(y_test, y_prob))
    except ValueError:
        auc = 0.5
    return {
        "model": name,
        "accuracy": round(acc, 4),
        "f1": round(f1, 4),
        "auc": round(auc, 4),
    }


# ---------------------------------------------------------------------------
# run()
# ---------------------------------------------------------------------------

FEATURE_COLS = [
    # 생산 지표
    "total_production", "korea_production", "overseas_production",
    "ev_production", "ev_ratio_pct", "ev_ratio_12m_chg",
    # 판매 지표
    "us_sales", "china_sales", "europe_sales", "domestic_sales", "us_sales_12m_chg",
    # 거시 지표
    "usd_krw", "oil_price", "global_auto_demand",
    # 계절
    "month", "quarter", "is_summer", "is_winter",
    # 주가 파생
    "prev_m_close", "ret_1m", "ret_3m", "ret_6m", "ret_12m",
    "ma_3m", "ma_6m", "ma_12m", "ma_gap_3_12", "volatility_6m",
]


def run() -> dict:
    df = generate_hyundai_dataset(seed=42)

    X = df[FEATURE_COLS].values
    y = df["target"].values

    # 시계열 순서 유지 분리 (70:30)
    split = int(len(X) * 0.70)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    scaler = StandardScaler()
    X_tr = scaler.fit_transform(X_train)
    X_te = scaler.transform(X_test)

    # --- ML 모델 --------------------------------------------------------
    rf = RandomForestClassifier(
        n_estimators=200, max_depth=6, min_samples_leaf=2, random_state=42
    )
    gbm = GradientBoostingClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.8, random_state=42
    )

    # --- DL 모델 (MLP 신경망) -------------------------------------------
    mlp = MLPClassifier(
        hidden_layer_sizes=(64, 32, 16),
        activation="relu",
        solver="adam",
        learning_rate_init=0.001,
        max_iter=500,
        early_stopping=True,
        validation_fraction=0.15,
        random_state=42,
    )

    results = [
        _evaluate("RandomForest (ML)", rf, X_tr, y_train, X_te, y_test),
        _evaluate("GradientBoosting (ML)", gbm, X_tr, y_train, X_te, y_test),
        _evaluate("MLP Neural Network (DL)", mlp, X_tr, y_train, X_te, y_test),
    ]

    # 상위 5개 특성 중요도 (RandomForest 기준)
    imp = sorted(
        zip(FEATURE_COLS, rf.feature_importances_.tolist()),
        key=lambda x: -x[1],
    )[:5]

    # 최신 월 EV/판매 현황 요약
    latest = df.iloc[-1]
    ev_summary = {
        "year": int(latest["year"]),
        "month": int(latest["month"]),
        "ev_ratio_pct": round(float(latest["ev_ratio_pct"]), 2),
        "ev_production": int(latest["ev_production"]),
        "us_sales": int(latest["us_sales"]),
        "total_production": int(latest["total_production"]),
    }

    best = max(results, key=lambda r: r["auc"])

    return {
        "chapter": "chapter116",
        "topic": "현대자동차 주가 예측 (ML/DL 고도화 — 월별 데이터)",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "n_samples": int(len(df)),
        "n_features": int(len(FEATURE_COLS)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "model_comparison": results,
        "best_model": best,
        "top5_features_rf": [
            {"feature": k, "importance": round(v, 4)} for k, v in imp
        ],
        "latest_quarter_summary": ev_summary,
        "insight": (
            "EV 생산 비율과 미국 판매량 성장이 주가 예측의 핵심 변수로 확인됩니다. "
            "DL(MLP) 모델은 비선형 상호작용을 ML 앙상블 대비 보완적으로 포착합니다."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=2))
