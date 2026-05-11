"""선형회귀 실습 파일"""
from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

LESSON_10MIN = "선형회귀는 입력과 목표값의 직선 관계를 가장 기본적으로 학습하는 회귀 모델이다."
PRACTICE_30MIN = "샘플 수, 특성 수, 노이즈, 테스트 비율, 랜덤 시드를 바꿔가며 MSE가 왜 달라지는지 실험한다."

DEFAULT_PARAMS: dict[str, Any] = {
    "n_samples": 120,
    "n_features": 3,
    "noise": 7.0,
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
        "n_samples": _coerce_int(raw.get("n_samples"), int(DEFAULT_PARAMS["n_samples"]), minimum=30, maximum=1000),
        "n_features": _coerce_int(raw.get("n_features"), int(DEFAULT_PARAMS["n_features"]), minimum=1, maximum=20),
        "noise": _coerce_float(raw.get("noise"), float(DEFAULT_PARAMS["noise"]), minimum=0.0, maximum=80.0),
        "test_size": _coerce_float(raw.get("test_size"), float(DEFAULT_PARAMS["test_size"]), minimum=0.1, maximum=0.5),
        "random_state": _coerce_int(raw.get("random_state"), int(DEFAULT_PARAMS["random_state"]), minimum=0, maximum=9999),
    }


def run_with_params(params: dict[str, Any] | None = None) -> dict[str, Any]:
    config = _sanitize_params(params)
    X, y = make_regression(
        n_samples=config["n_samples"],
        n_features=config["n_features"],
        noise=config["noise"],
        random_state=config["random_state"],
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config["test_size"],
        random_state=config["random_state"],
    )

    model = LinearRegression().fit(X_train, y_train)
    pred = model.predict(X_test)
    mse = float(mean_squared_error(y_test, pred))

    residuals = y_test - pred
    preview = [
        {
            "actual": round(float(actual), 4),
            "predicted": round(float(predicted), 4),
            "error": round(float(actual - predicted), 4),
        }
        for actual, predicted in zip(y_test[:5], pred[:5])
    ]

    return {
        "chapter": "chapter05",
        "topic": "선형회귀",
        "mse": mse,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "noise": float(config["noise"]),
        "n_samples": int(config["n_samples"]),
        "n_features": int(config["n_features"]),
        "test_size": float(config["test_size"]),
        "random_state": int(config["random_state"]),
        "coef_preview": [round(float(v), 4) for v in model.coef_[: min(5, len(model.coef_))]],
        "intercept": round(float(model.intercept_), 4),
        "residual_mean": round(float(np.mean(residuals)), 6),
        "residual_std": round(float(np.std(residuals)), 6),
        "prediction_preview": preview,
        "fixed_demo_reason": (
            "기본 실행은 make_regression과 train_test_split에 같은 random_state=42를 써서 "
            "항상 같은 연습 데이터를 만들기 때문에 mse도 매번 같게 나온다."
        ),
        "change_hint": (
            "샘플 수, 특성 수, 노이즈, 테스트 비율, 랜덤 시드를 바꾸면 데이터와 분할이 달라져 "
            "mse도 함께 바뀐다."
        ),
        "mse_reading": (
            "MSE는 예측값과 실제값 차이를 제곱해 평균낸 값이다. "
            "작을수록 직선이 데이터를 더 가깝게 설명한 것이다."
        ),
    }


def run() -> dict[str, Any]:
    return run_with_params(DEFAULT_PARAMS)


if __name__ == "__main__":
    print(run())
