"""주가 예측 손실에서 학습률 실험"""
from __future__ import annotations


def optimize(lr: float, steps: int = 25) -> list[float]:
    weight = 1.8
    history = []
    target_weight = 0.65
    for _ in range(steps):
        grad = 2 * (weight - target_weight)
        weight -= lr * grad
        history.append(weight)
    return history


def run() -> dict:
    h_small = optimize(lr=0.05)
    h_good = optimize(lr=0.2)
    h_big = optimize(lr=1.1)

    return {
        "chapter": "chapter27",
        "topic": "주가 예측 손실에서 학습률 실험",
        "lesson_10min": "학습률은 예측 오차를 줄이는 속도이지만 너무 크면 주가 예측 가중치가 발산할 수 있다.",
        "practice_30min": "다음 날 수익률을 예측하는 단일 가중치를 가정하고 학습률별 수렴/발산을 비교한다.",
        "target_weight": 0.65,
        "final_weight_small_lr": round(h_small[-1], 6),
        "final_weight_good_lr": round(h_good[-1], 6),
        "final_weight_big_lr": round(h_big[-1], 6),
        "big_lr_first_5": [round(v, 4) for v in h_big[:5]],
    }


if __name__ == "__main__":
    print(run())
