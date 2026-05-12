"""로봇주 vs 반도체주 텍스트 분류 (TF-IDF + 다중 분류기 비교)"""
from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

LESSON_10MIN = (
    "종목 설명 텍스트를 TF-IDF로 숫자로 바꾼 뒤 로지스틱 회귀·랜덤 포레스트·SVM으로 "
    "로봇주(0)와 반도체주(1)를 분류한다. BERT와 같은 목적을 경량 모델로 체험한다."
)
PRACTICE_30MIN = (
    "TF-IDF 벡터화 + 세 가지 분류기 성능을 비교하고 "
    "어떤 키워드가 분류에 중요한지 확인한다."
)

TRAIN_TEXTS = [
    "산업용 로봇 완성품과 감속기를 생산하는 기업입니다.",
    "협동 로봇과 로봇 제어기 전문 제조사입니다.",
    "서비스 로봇과 자율주행 로봇 센서 핵심 부품 업체입니다.",
    "로봇 관절용 감속기와 액추에이터를 공급합니다.",
    "물류 자동화 로봇과 AGV를 개발합니다.",
    "의료용 로봇 팔과 정밀 제어 시스템을 만듭니다.",
    "교육용 및 엔터테인먼트 로봇 플랫폼 전문 기업입니다.",
    "드론과 무인 이동체 소프트웨어를 개발합니다.",
    "GPU와 AI 반도체 칩을 설계·생산합니다.",
    "메모리 반도체와 낸드 플래시를 대량 생산합니다.",
    "NPU 기반 엣지 AI 칩을 공급하는 팹리스입니다.",
    "전력 반도체 MOSFET과 IGBT를 제조합니다.",
    "시스템 반도체와 파운드리 서비스를 제공합니다.",
    "고대역폭 메모리 HBM과 D램 모듈을 생산합니다.",
    "자율주행용 레이더 및 라이다 반도체를 개발합니다.",
    "5G 통신용 RF 반도체와 안테나 모듈을 공급합니다.",
]
TRAIN_LABELS = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]

TEST_TEXTS = [
    "산업 자동화 로봇과 스마트 팩토리 솔루션 기업입니다.",
    "차량용 반도체와 MCU를 공급하는 팹리스 회사입니다.",
    "웨어러블 로봇 외골격 장치를 연구 개발합니다.",
    "DDR5 메모리와 SSD 컨트롤러 반도체를 만듭니다.",
]
TEST_LABELS = [0, 1, 0, 1]

LABEL_NAMES = {0: "로봇주", 1: "반도체주"}


def _build_pipeline(clf) -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), max_features=300)),
        ("clf", clf),
    ])


def run() -> dict:
    pipelines = {
        "logistic": _build_pipeline(LogisticRegression(max_iter=1000, random_state=42)),
        "random_forest": _build_pipeline(
            RandomForestClassifier(n_estimators=100, random_state=42)
        ),
        "svm": _build_pipeline(LinearSVC(max_iter=2000, random_state=42)),
    }

    results: dict[str, dict] = {}
    for name, pipe in pipelines.items():
        pipe.fit(TRAIN_TEXTS, TRAIN_LABELS)
        pred = pipe.predict(TEST_TEXTS)
        results[name] = {
            "accuracy": round(float(accuracy_score(TEST_LABELS, pred)), 4),
            "f1": round(float(f1_score(TEST_LABELS, pred, zero_division=0)), 4),
            "predictions": [LABEL_NAMES[int(p)] for p in pred],
        }

    best_model = max(results, key=lambda k: results[k]["accuracy"])

    return {
        "chapter": "chapter113",
        "topic": "로봇주 vs 반도체주 텍스트 분류",
        "lesson_10min": LESSON_10MIN,
        "practice_30min": PRACTICE_30MIN,
        "train_samples": len(TRAIN_TEXTS),
        "test_samples": len(TEST_TEXTS),
        "test_texts": TEST_TEXTS,
        "model_comparison": results,
        "best_model": best_model,
        "note": (
            "TF-IDF는 문자 n-gram을 사용합니다. "
            "더 정확한 분류가 필요하면 BERT(transformers+torch)를 사용하세요."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=2))
