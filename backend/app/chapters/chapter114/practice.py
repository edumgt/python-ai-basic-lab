"""LoRA(Low-Rank Adaptation) 개념 numpy 시뮬레이션"""
from __future__ import annotations

import numpy as np

LESSON_10MIN = (
    "LoRA는 사전학습 가중치 W₀를 동결하고 ΔW = B×A(저랭크 행렬)만 학습한다. "
    "랭크 r이 작을수록 파라미터 수가 급감하며, 추론 시 W₀ + BA로 병합 가능하다."
)
PRACTICE_30MIN = (
    "numpy로 가중치 행렬을 시뮬레이션하고 Full/LoRA 파라미터 수를 비교한다. "
    "랭크별 근사 오차와 압축률을 계산해 LoRA의 효율성을 수치로 확인한다."
)


def _param_count(rows: int, cols: int, rank: int) -> dict[str, int]:
    full = rows * cols
    lora = rows * rank + rank * cols
    return {"full": full, "lora": lora, "saved": full - lora, "rank": rank}


def _simulate_lora(rows: int, cols: int, rank: int, seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    W0 = rng.normal(0, 0.02, (rows, cols))
    A = rng.normal(0, 0.02, (rank, cols))
    B = np.zeros((rows, rank))
    delta_W = B @ A
    W_with_lora = W0 + delta_W

    x = rng.normal(0, 1, (cols,))
    out_full = W0 @ x
    out_lora = W_with_lora @ x
    diff = float(np.mean(np.abs(out_full - out_lora)))

    params = _param_count(rows, cols, rank)
    compression_ratio = round(params["saved"] / params["full"] * 100, 2)
    return {
        "rows": rows,
        "cols": cols,
        "rank": rank,
        "full_params": params["full"],
        "lora_params": params["lora"],
        "saved_params": params["saved"],
        "compression_pct": compression_ratio,
        "output_diff_mean_abs": round(diff, 6),
        "note": "초기 ΔW=0이므로 차이는 0에 가깝습니다. 학습 후 B가 업데이트되며 차이가 생깁니다.",
    }


def run() -> dict:
    configs = [
        {"rows": 768, "cols": 768, "rank": 4},
        {"rows": 768, "cols": 768, "rank": 8},
        {"rows": 768, "cols": 768, "rank": 16},
        {"rows": 1024, "cols": 1024, "rank": 4},
        {"rows": 1024, "cols": 1024, "rank": 16},
    ]

    results = [_simulate_lora(**c) for c in configs]

    best = min(results, key=lambda r: r["lora_params"])
    summary_rows = [
        {
            "설정": f"{r['rows']}×{r['cols']} r={r['rank']}",
            "Full 파라미터": f"{r['full_params']:,}",
            "LoRA 파라미터": f"{r['lora_params']:,}",
            "압축률": f"{r['compression_pct']}%",
        }
        for r in results
    ]

    return {
        "chapter": "chapter114",
        "topic": "LoRA 저랭크 적응 파라미터 시뮬레이션",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "key_formula": "ΔW = B × A  (B: d×r, A: r×k, r << min(d,k))",
        "simulation_results": results,
        "summary_table": summary_rows,
        "most_efficient": {
            "설정": f"{best['rows']}×{best['cols']} r={best['rank']}",
            "LoRA 파라미터": best["lora_params"],
            "압축률": f"{best['compression_pct']}%",
        },
        "insight": (
            "랭크 r=4로 768×768 행렬을 근사하면 파라미터를 96% 절감할 수 있습니다. "
            "초기화 직후 ΔW=0이므로 원본 출력과 동일하며, 학습을 통해 B 행렬이 업데이트됩니다."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=2))
