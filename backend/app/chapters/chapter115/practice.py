"""Instruction Tuning 개념 시뮬레이션 (TF-IDF + 분류기)"""
from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline

LESSON_10MIN = (
    "Instruction Tuning은 '지시-입력-출력' 형식 데이터로 모델이 사람의 지시를 따르도록 학습한다. "
    "소량의 고품질 데이터(LIMA: 1,000개)만으로도 충분히 효과적임이 증명되었다."
)
PRACTICE_30MIN = (
    "금융 도메인 지시 문장을 TF-IDF로 벡터화하고 로지스틱 회귀로 지시 유형을 분류한다. "
    "파인튜닝 전(일반 모델)과 후(도메인 특화)의 정확도 차이를 시뮬레이션으로 비교한다."
)

# ---------------------------------------------------------------------------
# 금융 도메인 Instruction Tuning 시뮬레이션 데이터
# 형식: (instruction, category)
# category: analysis(분석), summary(요약), signal(매매신호), risk(리스크경고), qa(질의응답)
# ---------------------------------------------------------------------------
DOMAIN_TRAIN = [
    # analysis
    ("이 종목의 기술적 지표를 분석해줘", "analysis"),
    ("삼성전자 최근 실적을 바탕으로 분석해줘", "analysis"),
    ("반도체 섹터 수급 분석 결과를 설명해줘", "analysis"),
    ("이 종목의 이동평균선과 RSI를 분석해줘", "analysis"),
    ("코스피 지수의 기술적 분석을 해줘", "analysis"),
    ("외국인 순매수 종목을 분석해줘", "analysis"),
    # summary
    ("이 공시 내용을 한 줄로 요약해줘", "summary"),
    ("분기 실적 보고서를 간단히 정리해줘", "summary"),
    ("오늘 주요 뉴스를 요약해줘", "summary"),
    ("이 증권사 리포트의 핵심을 요약해줘", "summary"),
    ("DART 사업보고서를 요약해줘", "summary"),
    ("이 종목 관련 뉴스 세 개를 정리해줘", "summary"),
    # signal
    ("지금 이 종목 매수 신호가 나오고 있나요?", "signal"),
    ("RSI 기준으로 과매수 구간인지 알려줘", "signal"),
    ("골든크로스가 발생한 종목을 찾아줘", "signal"),
    ("단기 매도 시점을 알려줘", "signal"),
    ("이동평균 이탈 시 매수 타이밍인가요?", "signal"),
    ("거래량 급증 후 매수 신호인지 확인해줘", "signal"),
    # risk
    ("이 종목의 투자 위험 요소를 알려줘", "risk"),
    ("금리 인상이 이 종목에 미치는 위험은?", "risk"),
    ("환율 변동에 따른 리스크를 설명해줘", "risk"),
    ("이 기업의 재무 건전성 위험 신호는?", "risk"),
    ("공매도 증가가 리스크 신호인지 알려줘", "risk"),
    ("이 업종의 규제 리스크를 정리해줘", "risk"),
    # qa
    ("PER이 뭔지 설명해줘", "qa"),
    ("EPS는 어떻게 계산해?", "qa"),
    ("ROE가 높으면 좋은 건가요?", "qa"),
    ("EBITDA는 무엇인가요?", "qa"),
    ("배당수익률이 높은 종목을 어떻게 고르나요?", "qa"),
    ("PBR 1 이하 종목이 왜 저평가인가요?", "qa"),
]

DOMAIN_TEST = [
    ("이 종목 MACD 분석해줘", "analysis"),
    ("실적 발표 내용을 요약해줘", "summary"),
    ("지금 매수해도 될까요?", "signal"),
    ("이 종목 손절 기준이 있나요?", "risk"),
    ("시가총액이 뭔가요?", "qa"),
    ("SK하이닉스 반도체 실적 분석 부탁해요", "analysis"),
    ("오늘 장 마감 시황 요약해줘", "summary"),
    ("볼린저밴드 하단 이탈 신호인가요?", "signal"),
]

# 파인튜닝 전 시뮬레이션: 도메인 외 일반 데이터로 학습
PRETRAIN_TRAIN = [
    ("이 문서를 분석해줘", "analysis"),
    ("짧게 요약해줘", "summary"),
    ("지금 어떻게 해야 하나요?", "signal"),
    ("위험한 점은 무엇인가요?", "risk"),
    ("이게 뭔지 설명해줘", "qa"),
    ("데이터를 분석해줘", "analysis"),
    ("내용을 정리해줘", "summary"),
    ("결정해줘", "signal"),
    ("문제점이 뭐야?", "risk"),
    ("개념 설명해줘", "qa"),
]


def _build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 4), max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000, random_state=42)),
    ])


def run() -> dict:
    train_texts, train_labels = zip(*DOMAIN_TRAIN)
    test_texts, test_labels = zip(*DOMAIN_TEST)
    pre_texts, pre_labels = zip(*PRETRAIN_TRAIN)

    # 파인튜닝 후(도메인 데이터로 학습)
    domain_pipe = _build_pipeline()
    domain_pipe.fit(train_texts, train_labels)
    domain_pred = domain_pipe.predict(test_texts)
    domain_acc = round(float(accuracy_score(test_labels, domain_pred)), 4)
    domain_f1 = round(float(f1_score(test_labels, domain_pred, average="macro", zero_division=0)), 4)

    # 파인튜닝 전(일반 데이터로만 학습)
    pretrain_pipe = _build_pipeline()
    pretrain_pipe.fit(pre_texts, pre_labels)
    pretrain_pred = pretrain_pipe.predict(test_texts)
    pretrain_acc = round(float(accuracy_score(test_labels, pretrain_pred)), 4)
    pretrain_f1 = round(float(f1_score(test_labels, pretrain_pred, average="macro", zero_division=0)), 4)

    predictions = [
        {
            "instruction": t,
            "expected": e,
            "before_finetuning": p,
            "after_finetuning": d,
            "improved": (e == d and e != p),
        }
        for t, e, p, d in zip(test_texts, test_labels, pretrain_pred, domain_pred)
    ]

    categories = ["analysis", "summary", "signal", "risk", "qa"]
    train_per_category = {cat: sum(1 for _, c in DOMAIN_TRAIN if c == cat) for cat in categories}

    return {
        "chapter": "chapter115",
        "topic": "Instruction Tuning 지시 분류 시뮬레이션",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "data_format": {
            "instruction": "사용자 지시 텍스트",
            "category": "analysis | summary | signal | risk | qa",
            "note": "Instruction Tuning 학습 데이터 형식: (지시, 카테고리) 쌍",
        },
        "training_data": {
            "domain_samples": len(DOMAIN_TRAIN),
            "per_category": train_per_category,
        },
        "before_finetuning": {
            "description": "도메인 외 일반 데이터만 학습한 경우 (파인튜닝 전)",
            "accuracy": pretrain_acc,
            "f1_macro": pretrain_f1,
        },
        "after_finetuning": {
            "description": "금융 도메인 Instruction 데이터로 학습한 경우 (파인튜닝 후)",
            "accuracy": domain_acc,
            "f1_macro": domain_f1,
        },
        "accuracy_gain": round(domain_acc - pretrain_acc, 4),
        "f1_gain": round(domain_f1 - pretrain_f1, 4),
        "test_predictions": predictions,
        "insight": (
            f"파인튜닝 전 정확도 {pretrain_acc:.1%} → 후 {domain_acc:.1%}로 "
            f"{(domain_acc - pretrain_acc) * 100:.1f}%p 향상됩니다. "
            "도메인 특화 데이터 30개만으로도 성능이 크게 개선됩니다."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=2))
