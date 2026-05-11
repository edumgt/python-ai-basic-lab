"""선형회귀로 다음 종가 예측"""
from __future__ import annotations

from typing import Any

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from stock_practice_utils import FEATURE_POOL, make_stock_feature_frame, preview_records, time_split_frame, top_items

LESSON_10MIN = "선형회귀는 최근 가격·거래량 특성을 직선으로 조합해 다음 거래일 종가를 예측하는 가장 기본적인 회귀 모델이다."
PRACTICE_30MIN = "샘플 수, 특성 수, 노이즈, 테스트 비율, 랜덤 시드를 바꿔가며 다음 종가 예측 MSE가 어떻게 달라지는지 실험한다."

DEFAULT_PARAMS: dict[str, Any] = {
    "n_samples": 260,
    "n_features": 5,
    "noise": 0.018,
    "test_size": 0.2,
    "random_state": 42,
}


def _coerce_int(value: Any, default: int, *, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


def _coerce_float(value: Any, default: float, *, minimum: float, maximum: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


def _sanitize_params(params: dict[str, Any] | None = None) -> dict[str, Any]:
    raw = params or {}
    return {
        "n_samples": _coerce_int(raw.get("n_samples"), int(DEFAULT_PARAMS["n_samples"]), minimum=80, maximum=600),
        "n_features": _coerce_int(raw.get("n_features"), int(DEFAULT_PARAMS["n_features"]), minimum=2, maximum=len(FEATURE_POOL)),
        "noise": _coerce_float(raw.get("noise"), float(DEFAULT_PARAMS["noise"]), minimum=0.005, maximum=0.08),
        "test_size": _coerce_float(raw.get("test_size"), float(DEFAULT_PARAMS["test_size"]), minimum=0.1, maximum=0.4),
        "random_state": _coerce_int(raw.get("random_state"), int(DEFAULT_PARAMS["random_state"]), minimum=0, maximum=9999),
    }


def run_with_params(params: dict[str, Any] | None = None) -> dict[str, Any]:
    config = _sanitize_params(params)
    df = make_stock_feature_frame(seed=config["random_state"], n=config["n_samples"], noise=config["noise"])
    features = FEATURE_POOL[: config["n_features"]]
    x_train, x_test, y_train, y_test = time_split_frame(df, features, "target_close_next", test_size=config["test_size"])

    model = LinearRegression()
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    mse = float(mean_squared_error(y_test, pred))

    coef_map = {name: float(value) for name, value in zip(features, model.coef_)}
    preview_df = x_test.copy()
    preview_df["actual_next_close"] = y_test.values
    preview_df["predicted_next_close"] = pred

    return {
        "chapter": "chapter05",
        "topic": "선형회귀로 다음 종가 예측",
        "mse": round(mse, 6),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "noise": float(config["noise"]),
        "n_samples": int(config["n_samples"]),
        "n_features": int(config["n_features"]),
        "test_size": float(config["test_size"]),
        "random_state": int(config["random_state"]),
        "latest_actual_next_close": round(float(y_test.iloc[-1]), 4),
        "latest_predicted_next_close": round(float(pred[-1]), 4),
        "coef_preview": top_items(coef_map, limit=6),
        "prediction_preview": preview_records(
            preview_df.reset_index(drop=True),
            [*features[: min(3, len(features))], "actual_next_close", "predicted_next_close"],
            tail=5,
        ),
        "fixed_demo_reason": (
            "기본 실행은 같은 랜덤 시드와 같은 주가 생성 설정을 쓰기 때문에 "
            "항상 같은 삼성전자 비슷한 연습 차트를 만들고 mse도 같은 값으로 나온다."
        ),
        "change_hint": (
            "샘플 수를 늘리거나, 특성 수를 바꾸거나, 가격 노이즈를 높이면 "
            "다음 종가 예측 난이도와 mse가 함께 달라진다."
        ),
        "mse_reading": (
            "MSE는 예측한 다음 종가와 실제 다음 종가 차이를 제곱해 평균낸 값이다. "
            "작을수록 직선 모델이 주가 흐름을 더 가깝게 설명한 것이다."
        ),
    }


def run() -> dict[str, Any]:
    return run_with_params(DEFAULT_PARAMS)


if __name__ == "__main__":
    print(run())
