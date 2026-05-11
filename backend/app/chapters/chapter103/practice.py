"""Transformer 시계열 기초 실습 파일"""
from __future__ import annotations

import numpy as np

# 10분 핵심 개념: Transformer의 핵심 아이디어
LESSON_10MIN = (
    "Transformer는 순차 반복(RNN) 없이 Self-Attention으로 "
    "모든 시점 간 관계를 한 번에 계산한다. "
    "Q(Query)·K(Key)·V(Value) 세 행렬이 '무엇을 찾는가·어디에 있는가·무엇을 꺼낼까'를 담당한다."
)

# 30분 실습 목표: Self-Attention을 숫자로 직접 확인
PRACTICE_30MIN = (
    "7개 시점의 수익률 시퀀스에 단일 헤드 Self-Attention을 적용해 "
    "어떤 과거 시점이 가장 높은 가중치를 받는지 확인하고, "
    "context 벡터로 다음 수익률을 예측한다."
)


def _softmax(x: np.ndarray) -> np.ndarray:
    """수치 안정 소프트맥스: 최댓값을 빼 오버플로를 방지한 뒤 확률로 변환."""
    z = x - np.max(x)
    e = np.exp(z)
    return e / e.sum()


def run() -> dict:
    # 7개 시점의 일별 주가 수익률 시퀀스 (예시 데이터)
    seq = np.array([0.01, 0.02, -0.01, 0.015, 0.03, -0.005, 0.018], dtype=float)

    # ── Self-Attention: Q · K · V 계산 ──────────────────────────────────────
    # Q (Query): 가장 최근 시점(t=-1)을 2차원 특성 공간으로 투영
    #            "지금 이 시점이 어떤 정보를 원하는가?"
    q = seq[-1] * np.array([1.2, 0.6])                          # shape: (2,)

    # K (Key): 모든 시점을 2차원 특성 공간으로 투영
    #          "각 시점이 어떤 특성을 가지고 있는가?"
    keys = np.stack([seq * 0.8, seq * 1.1], axis=1)             # shape: (T, 2)

    # V (Value): 각 시점에서 실제로 꺼낼 정보 (수익률 + 수익률²)
    #            "그 시점의 정보를 어떻게 표현할 것인가?"
    values = np.stack([seq, np.square(seq)], axis=1)            # shape: (T, 2)

    # Attention 점수: Q와 K의 내적 → 스케일 조정 (차원 수의 제곱근으로 나눔)
    # 스케일 조정 이유: 차원이 클수록 내적 값이 커져 소프트맥스가 포화되는 문제를 방지
    scores = (keys @ q) / np.sqrt(len(q))                       # shape: (T,)

    # 소프트맥스로 점수를 확률 가중치로 변환 — 합이 1이 되어 비중을 표현
    weights = _softmax(scores)                                   # shape: (T,)

    # Context 벡터: 가중치로 V를 가중합 — 중요한 시점의 정보가 더 많이 반영됨
    context = weights @ values                                   # shape: (2,)

    # 예측: context의 두 요소를 선형 결합해 다음 시점 수익률 점수 생성
    next_score = float(0.7 * context[0] + 0.3 * context[1])

    return {
        "chapter": "chapter103",
        "topic": "Transformer 시계열 기초 (Self-Attention)",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "sequence": seq.tolist(),                                 # 입력 수익률 시퀀스
        "attention_weights": np.round(weights, 4).tolist(),       # 각 시점의 주목 비중
        "most_attended_timestep": int(np.argmax(weights)),        # 가장 많이 주목된 시점 인덱스
        "context_vector": np.round(context, 6).tolist(),          # 가중합 결과 벡터
        "predicted_next_return_score": round(next_score, 6),      # 다음 수익률 예측 점수
    }


if __name__ == "__main__":
    print(run())
