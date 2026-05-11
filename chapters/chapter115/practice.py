# [개발자 설명 주석 적용됨]
"""롯데호텔 주가 예측 — 30개 체인 호텔 가상 데이터셋 생성 및 ML 분류 실습"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

LESSON_10MIN = (
    "30개 체인 호텔 객실예약률·계절성·10년 월말 주가를 특성으로 가상 1000행 데이터셋을 생성하고 ML 모델로 상승/하락을 예측한다."
)
PRACTICE_30MIN = (
    "롯데호텔 가상 주가 데이터(1000샘플)를 생성하고 랜덤 포레스트로 다음 달 상승 여부를 예측한다."
)

N_HOTELS = 30
HOTEL_NAMES = [f"hotel_{i:02d}_occ" for i in range(1, N_HOTELS + 1)]


def generate_hotel_dataset(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """롯데호텔 주가 예측을 위한 가상 데이터셋을 생성합니다.

    특성:
        - 30개 체인 호텔 객실 예약률 (%)
        - 계절 특성 (월, 분기, 계절, 성수기 여부)
        - 월말 주가 파생 특성 (전월 종가, 3/6/12개월 수익률, 이동평균, 변동성)
    타겟:
        - 다음 달 종가가 이번 달보다 높으면 1(상승), 아니면 0(하락)
    """
    rng = np.random.default_rng(seed)

    # 월별 날짜 생성
    dates = pd.date_range("2015-01", periods=n, freq="MS")
    months = dates.month.values.astype(int)
    quarters = ((months - 1) // 3 + 1).astype(int)
    seasons = np.where(
        np.isin(months, [12, 1, 2]), 0,
        np.where(np.isin(months, [3, 4, 5]), 1,
                 np.where(np.isin(months, [6, 7, 8]), 2, 3)),
    )  # 0=겨울, 1=봄, 2=여름, 3=가을
    is_peak = np.isin(months, [7, 8, 12, 1]).astype(int)  # 여름·겨울 성수기

    # 계절별 예약률 배율 (겨울<봄<가을<여름)
    season_boost = np.array([0.88, 1.00, 1.18, 0.97])[seasons]

    # 30개 체인 호텔 객실 예약률 생성
    hotel_data: dict[str, np.ndarray] = {}
    for col in HOTEL_NAMES:
        base_occ = rng.uniform(62, 82)            # 호텔별 기준 예약률 (%)
        trend = np.linspace(0, rng.uniform(1, 6), n)  # 장기 완만한 증가 추세
        noise = rng.normal(0, 4, size=n)
        occ = np.clip(base_occ * season_boost + trend + noise, 20.0, 99.0)
        hotel_data[col] = occ

    # 평균 예약률 (주가에 영향)
    mean_occ = np.mean(list(hotel_data.values()), axis=0)

    # 롯데호텔 주가 시뮬레이션 (기준가 10,000원)
    close = np.zeros(n)
    close[0] = 10_000.0
    for i in range(1, n):
        occ_effect = (mean_occ[i] - 72.0) * 18.0   # 예약률이 주가에 미치는 영향
        season_bonus = np.array([100.0, -30.0, 250.0, 80.0])[seasons[i]]
        macro_drift = rng.normal(10.0, 220.0)        # 경기 노이즈
        close[i] = max(close[i - 1] + occ_effect + season_bonus + macro_drift, 2_000.0)

    # DataFrame 구성
    df = pd.DataFrame(hotel_data)
    df["month"] = months
    df["quarter"] = quarters
    df["season"] = seasons
    df["is_peak_season"] = is_peak
    df["close"] = close
    df["date"] = dates.strftime("%Y-%m")

    # 주가 파생 특성
    df["prev_month_close"] = df["close"].shift(1)
    df["prev_3m_return"] = df["close"].pct_change(3) * 100.0
    df["prev_6m_return"] = df["close"].pct_change(6) * 100.0
    df["prev_12m_return"] = df["close"].pct_change(12) * 100.0
    df["price_ma3"] = df["close"].rolling(3).mean()
    df["price_ma6"] = df["close"].rolling(6).mean()
    df["volatility_6m"] = df["close"].pct_change().rolling(6).std() * 100.0

    # 타겟: 다음 달 상승 여부
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)

    return df.dropna().reset_index(drop=True)


def run() -> dict:
    # 데이터셋 생성
    df = generate_hotel_dataset(n=1000, seed=42)

    feature_cols = (
        HOTEL_NAMES
        + ["month", "quarter", "season", "is_peak_season"]
        + [
            "prev_month_close", "prev_3m_return", "prev_6m_return",
            "prev_12m_return", "price_ma3", "price_ma6", "volatility_6m",
        ]
    )

    X = df[feature_cols].values
    y = df["target"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_te_sc = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X_tr_sc, y_train)
    y_pred = model.predict(X_te_sc)
    y_prob = model.predict_proba(X_te_sc)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    try:
        auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        auc = 0.5

    # 상위 5개 특성 중요도
    imp_sorted = sorted(
        zip(feature_cols, model.feature_importances_.tolist()),
        key=lambda x: -x[1],
    )[:5]

    return {
        "chapter": "chapter115",
        "topic": "롯데호텔 주가 예측 (가상 데이터셋)",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "n_samples": int(len(df)),
        "n_features": int(len(feature_cols)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "accuracy": round(acc, 4),
        "auc": round(auc, 4),
        "top5_features": [
            {"feature": k, "importance": round(v, 4)} for k, v in imp_sorted
        ],
    }


if __name__ == "__main__":
    print(run())
