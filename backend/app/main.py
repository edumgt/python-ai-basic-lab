"""AI/ML Basic Class FastAPI 백엔드 — 문서 연계 실습 + 퀀트 ML/DL 학습 문서 API 서버."""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import time
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import httpx
import numpy as np
import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 앱 초기화 및 경로 설정
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI/ML Basic Class API",
    version="2.0.0",
    description="문서와 연결된 AI/ML 실습 코드를 웹에서 실행·조회하는 API 서버입니다.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parent
CHAPTERS_DIR = APP_DIR / "chapters"
CHAPTERS_ROOT = CHAPTERS_DIR.resolve()
FRONTEND_DIR = BASE_DIR / "frontend"
DOCS_DIR = BASE_DIR / "docs"
DATA_DIR = BASE_DIR / "data"

OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
NEWS_THEME_BACKEND = os.getenv("NEWS_THEME_BACKEND", "tfidf")
NEWS_THEME_EMBED_MODEL = os.getenv("NEWS_THEME_EMBED_MODEL", "jhgan/ko-sroberta-multitask")


# ---------------------------------------------------------------------------
# Pydantic 스키마 정의
# ---------------------------------------------------------------------------

class ChapterSummary(BaseModel):
    id: str
    title: str
    topic: str
    lesson_10min: str
    practice_30min: str
    has_run: bool


class ChapterDetail(ChapterSummary):
    readme: str


class ChapterSourceResponse(BaseModel):
    chapter: str
    source: str


class ChapterRunResponse(BaseModel):
    chapter: str
    topic: str
    result: dict[str, Any]
    elapsed_ms: float
    stdout: str = ""


class ChapterRunRequest(BaseModel):
    params: dict[str, Any] = {}


class DocSummary(BaseModel):
    id: str
    title: str
    filename: str


class DocDetail(DocSummary):
    content: str


class StockRow(BaseModel):
    date: str
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float
    volume: float


class StockAnalyzeRequest(BaseModel):
    rows: list[StockRow]
    model: str = "rf"   # logistic | rf | nn | gbm


class ChatRequest(BaseModel):
    message: str
    context: dict[str, Any] = {}


class AssistantRouteRequest(BaseModel):
    message: str


class NewsConsultRequest(BaseModel):
    message: str
    market_scope: str = "krx"
    horizon: str = "1m"
    risk_profile: str = "neutral"
    holdings: list[str] = []


class DatasetSummary(BaseModel):
    id: str
    filename: str
    title: str
    description: str
    rows: int
    n_columns: int
    recommended_webapp: str
    practice_label: str


class DatasetDetail(DatasetSummary):
    columns: list[str]
    preview: list[dict[str, Any]]
    numeric_columns: list[str]
    recommended_path: str
    chart_hint: str


# ---------------------------------------------------------------------------
# 내부 유틸리티 함수
# ---------------------------------------------------------------------------

def _parse_practice_meta(py_path: Path) -> dict[str, str]:
    meta: dict[str, str] = {"topic": "", "lesson_10min": "", "practice_30min": ""}
    if not py_path.exists():
        return meta
    text = py_path.read_text(encoding="utf-8")
    for pattern, field in [
        (r'LESSON_10MIN\s*=\s*["\'](.+?)["\']', "lesson_10min"),
        (r'PRACTICE_30MIN\s*=\s*["\'](.+?)["\']', "practice_30min"),
        (r'"topic"\s*:\s*"([^"]+)"', "topic"),
        (r"'topic'\s*:\s*'([^']+)'", "topic"),
    ]:
        m = re.search(pattern, text)
        if m and not meta[field]:
            meta[field] = m.group(1).strip()
    return meta


def _chapter_title(chapter_dir: Path) -> str:
    readme = chapter_dir / "README.md"
    if readme.exists():
        first = readme.read_text(encoding="utf-8").splitlines()[0]
        return re.sub(r"^#+\s*", "", first).strip()
    return chapter_dir.name


def _build_summary(chapter_dir: Path) -> ChapterSummary:
    py_path = chapter_dir / "practice.py"
    meta = _parse_practice_meta(py_path)
    has_run = py_path.exists() and "def run(" in py_path.read_text(encoding="utf-8")
    return ChapterSummary(
        id=chapter_dir.name,
        title=_chapter_title(chapter_dir),
        topic=meta["topic"],
        lesson_10min=meta["lesson_10min"],
        practice_30min=meta["practice_30min"],
        has_run=has_run,
    )


_DATASET_META: dict[str, dict[str, str]] = {
    "dart_disclosures": {
        "title": "DART 최근 공시 타임라인",
        "description": "사업보고서, 임원지분 변동, 정정공시 같은 최근 DART 공시 흐름을 모아 투자자가 체크할 재료를 보여주는 데이터입니다.",
        "recommended_webapp": "DART 공시 투자 파이프라인",
        "practice_label": "공시 이벤트 타임라인 읽기",
        "recommended_path": "/dart",
    },
    "dart_fundamentals": {
        "title": "DART 재무제표 팩터",
        "description": "매출, 영업이익, 순이익, 부채비율, 유동비율 같은 DART 실공시 재무 데이터를 투자 팩터로 정리한 데이터입니다.",
        "recommended_webapp": "DART 공시 투자 파이프라인",
        "practice_label": "연도별 재무 체력 비교",
        "recommended_path": "/dart",
    },
    "dart_invest_pipeline": {
        "title": "DART 기반 투자 파이프라인",
        "description": "DART 재무 + 최근 공시 + 가격 팩터를 합쳐서 종목별 투자 관찰 점수를 만든 통합 데이터입니다.",
        "recommended_webapp": "DART 공시 투자 파이프라인",
        "practice_label": "공시 기반 투자 컨설팅 보기",
        "recommended_path": "/dart",
    },
    "external_invest_ml_dataset": {
        "title": "외부 데이터 기반 투자 학습셋",
        "description": "DART 재무제표에 FRED 거시신호와 World Bank 한국 구조지표를 붙여 다음 해 실적 개선 여부를 학습하는 데이터입니다.",
        "recommended_webapp": "거시경제 투자 파이프라인",
        "practice_label": "외부 데이터 ML/DL 비교",
        "recommended_path": "/macro",
    },
    "external_macro_pipeline": {
        "title": "외부 거시경제 파이프라인",
        "description": "FRED와 World Bank 데이터를 연도별 특징으로 정리해 금리, 물가, 실업률, VIX 같은 시장 환경을 읽는 데이터입니다.",
        "recommended_webapp": "거시경제 투자 파이프라인",
        "practice_label": "거시 레짐 읽기",
        "recommended_path": "/macro",
    },
    "experiment_log": {
        "title": "주식 모델 실험 로그",
        "description": "종목별 예측 모델과 파라미터, AUC, 샤프 비율을 비교하는 주식 AI 실험 로그입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "모델 성능 비교 시각화",
        "recommended_path": "/datasets?dataset=experiment_log",
    },
    "financial_statements": {
        "title": "상장사 재무제표 샘플",
        "description": "매출, 영업이익, 감가상각, CAPEX, 잉여현금흐름으로 기업가치와 적정주가를 연습하는 데이터입니다.",
        "recommended_webapp": "학습 허브",
        "practice_label": "chapter105 재무제표 실습",
        "recommended_path": "/?chapter=chapter105",
    },
    "macro_fred_signals": {
        "title": "FRED 거시 신호 모음",
        "description": "미국 기준금리, CPI, 실업률, 10년물 금리, VIX, 유가를 시계열로 모은 외부 매크로 데이터입니다.",
        "recommended_webapp": "거시경제 투자 파이프라인",
        "practice_label": "거시 시계열 미리보기",
        "recommended_path": "/macro",
    },
    "gender_approval": {
        "title": "상승 여부 분류 샘플",
        "description": "거래량 급증, 실적 서프라이즈, 신호 강도로 다음 거래일 상승 여부를 분류하는 데이터입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "상승/하락 분류 미리보기",
        "recommended_path": "/datasets?dataset=gender_approval",
    },
    "personal_info": {
        "title": "종목 기본 정보 스냅샷",
        "description": "티커, 시가총액, PER, PBR, 배당수익률로 멀티팩터 종목 선정을 연습하는 데이터입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "종목 기본 정보 비교",
        "recommended_path": "/datasets?dataset=personal_info",
    },
    "stock_ohlcv": {
        "title": "대표 종목 OHLCV 시계열",
        "description": "일별 시가·고가·저가·종가·거래량이 담긴 대표 주식 시계열입니다. 가격 예측과 기술적 지표 실습에 맞습니다.",
        "recommended_webapp": "주식 AI 실험실",
        "practice_label": "대표 종목 예측 바로 실행",
        "recommended_path": "/lab?dataset=stock_ohlcv",
    },
    "world_bank_korea_indicators": {
        "title": "World Bank 한국 구조지표",
        "description": "한국 GDP 성장률, 물가상승률, 실업률, 수출 비중 같은 국가 단위 장기 구조지표입니다.",
        "recommended_webapp": "거시경제 투자 파이프라인",
        "practice_label": "한국 장기 구조지표 읽기",
        "recommended_path": "/macro",
    },
    "stock_universe": {
        "title": "종목 유니버스 팩터",
        "description": "섹터별 종목의 모멘텀, 변동성, 밸류에이션, 시가총액을 비교하는 팩터 데이터입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "유니버스 팩터 비교",
        "recommended_path": "/datasets?dataset=stock_universe",
    },
    "stocks_features": {
        "title": "주식 클러스터링 특성",
        "description": "수익률, 변동성, 베타, PER, ROE로 종목 군집과 스타일 분류를 연습하는 데이터입니다.",
        "recommended_webapp": "학습 허브",
        "practice_label": "chapter109 군집 실습",
        "recommended_path": "/?chapter=chapter109",
    },
    "student_performance": {
        "title": "알파 팩터 학습 데이터",
        "description": "품질 점수, 모멘텀 점수, 이익 추정치 변화로 초과수익 발생 여부를 학습하는 데이터입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "알파 분류 연습",
        "recommended_path": "/datasets?dataset=student_performance",
    },
    "traffic_timeseries": {
        "title": "섹터 ETF 시계열",
        "description": "섹터 ETF의 종가와 거래량을 담은 짧은 시계열입니다. 레짐 전환과 시계열 예측 연습용입니다.",
        "recommended_webapp": "주식 AI 실험실",
        "practice_label": "섹터 시계열 분석",
        "recommended_path": "/lab?dataset=traffic_timeseries",
    },
}


def _mask_preview(df: pd.DataFrame, dataset_id: str) -> pd.DataFrame:
    return df.copy()


def _load_dataset_df(dataset_id: str) -> pd.DataFrame:
    csv_path = DATA_DIR / f"{dataset_id}.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail=f"데이터셋 '{dataset_id}'를 찾을 수 없어요.")
    return pd.read_csv(csv_path)


def _chart_hint(df: pd.DataFrame) -> str:
    cols = set(df.columns)
    if "date" in cols:
        return "timeseries"
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    object_cols = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
    if len(numeric_cols) >= 2:
        return "scatter"
    if len(numeric_cols) >= 1 and len(object_cols) >= 1:
        return "bar"
    return "table"


def _build_dataset_detail(dataset_id: str) -> DatasetDetail:
    meta = _DATASET_META.get(dataset_id)
    if not meta:
        raise HTTPException(status_code=404, detail=f"데이터셋 메타정보가 없는 id='{dataset_id}' 입니다.")
    df = _load_dataset_df(dataset_id)
    preview_df = _mask_preview(df.head(12), dataset_id).copy()
    if "date" in preview_df.columns:
        preview_df["date"] = preview_df["date"].astype(str)
    return DatasetDetail(
        id=dataset_id,
        filename=f"{dataset_id}.csv",
        title=meta["title"],
        description=meta["description"],
        rows=int(len(df)),
        n_columns=int(len(df.columns)),
        recommended_webapp=meta["recommended_webapp"],
        practice_label=meta["practice_label"],
        columns=[str(c) for c in df.columns.tolist()],
        preview=preview_df.to_dict(orient="records"),
        numeric_columns=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])],
        recommended_path=meta["recommended_path"],
        chart_hint=_chart_hint(df),
    )


def _ensure_ohlcv_frame(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    if "date" in frame.columns:
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")

    for col in ["open", "high", "low", "close", "volume"]:
        if col not in frame.columns:
            frame[col] = np.nan
        frame[col] = pd.to_numeric(frame[col], errors="coerce")

    frame["close"] = frame["close"].ffill()
    frame["open"] = frame["open"].fillna(frame["close"])
    frame["high"] = frame["high"].fillna(frame[["open", "close"]].max(axis=1))
    frame["low"] = frame["low"].fillna(frame[["open", "close"]].min(axis=1))
    frame["high"] = frame[["high", "open", "close"]].max(axis=1)
    frame["low"] = frame[["low", "open", "close"]].min(axis=1)

    if frame["volume"].notna().any():
        frame["volume"] = frame["volume"].ffill().bfill()
    else:
        synthetic = frame["close"].pct_change().abs().fillna(0).mul(7_500_000).add(2_000_000)
        frame["volume"] = synthetic.round()

    return frame.dropna(subset=["date", "close"]).sort_values("date").reset_index(drop=True)


def _next_business_day(value: pd.Timestamp) -> pd.Timestamp:
    next_day = value + pd.Timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += pd.Timedelta(days=1)
    return next_day


def _list_chapter_dirs() -> list[Path]:
    return [d for d in sorted(CHAPTERS_DIR.glob("chapter*")) if d.is_dir()]


def _chapter_dir_map() -> dict[str, Path]:
    return {d.name: d for d in _list_chapter_dirs()}


def _chapter_dir(chapter_id: str) -> Path:
    chapter_dir = _chapter_dir_map().get(chapter_id)
    if chapter_dir is None or chapter_dir.parent.resolve() != CHAPTERS_ROOT:
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'를 찾을 수 없어요.")
    return chapter_dir


def _doc_title(md_path: Path) -> str:
    if not md_path.exists():
        return md_path.stem
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip()
    return md_path.stem


def _list_docs() -> list[DocSummary]:
    docs = []
    for md in sorted(DOCS_DIR.glob("*.md"), key=lambda p: int(p.stem) if p.stem.isdigit() else 9999):
        if not md.stem.isdigit():
            continue
        docs.append(DocSummary(id=md.stem, title=_doc_title(md), filename=md.name))
    return docs


def _exec_run(chapter_id: str, params: dict[str, Any] | None = None) -> tuple[dict[str, Any], float, str]:
    chapter_path = _chapter_dir(chapter_id) / "practice.py"
    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'를 찾을 수 없어요.")
    namespace: dict[str, Any] = {}
    code = chapter_path.read_text(encoding="utf-8")
    try:
        exec(compile(code, str(chapter_path), "exec"), namespace)  # noqa: S102
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"코드 로딩 오류: {exc}") from exc
    if "run" not in namespace:
        raise HTTPException(status_code=500, detail="practice.py에 run() 함수가 없어요.")
    buf = io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    t0 = time.perf_counter()
    try:
        sys.stdout = sys.stderr = buf
        try:
            if params and "run_with_params" in namespace:
                result = namespace["run_with_params"](params)
            else:
                result = namespace["run"]()
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
    except Exception as exc:
        sys.stdout, sys.stderr = old_stdout, old_stderr
        raise HTTPException(status_code=500, detail=f"run() 실행 오류: {exc}") from exc
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
    stdout_text = buf.getvalue()
    return result, elapsed_ms, stdout_text


_FEAT_NAMES = {
    "ret": "당일 수익률",
    "ret_5": "5일 수익률",
    "ma5_gap": "5일 이동평균 괴리",
    "ma20_gap": "20일 이동평균 괴리",
    "vol_ratio": "거래량 비율",
    "range_pct": "고저 범위",
    "body_pct": "캔들 몸통 비율",
}


def _fallback_explanation(message: str, ctx: dict[str, Any]) -> str:
    """Ollama 오프라인 시 규칙 기반 설명을 반환합니다."""
    feat_imp: dict[str, float] = ctx.get("feature_importance", {})
    sorted_feats = sorted(feat_imp.items(), key=lambda x: -x[1])
    top_name   = _FEAT_NAMES.get(sorted_feats[0][0], sorted_feats[0][0]) if sorted_feats else "수익률"
    sec_name   = _FEAT_NAMES.get(sorted_feats[1][0], sorted_feats[1][0]) if len(sorted_feats) > 1 else "이동평균"
    acc        = ctx.get("accuracy", 0) * 100
    port       = ctx.get("portfolio_return", 0)
    bh         = ctx.get("buyhold_return", 0)
    auc        = ctx.get("auc", 0)
    model_name = ctx.get("model_name", "모델")

    if any(k in message for k in ["오른", "올라", "상승", "이유", "왜"]):
        resp = (
            f"'{top_name}'이 가장 큰 영향을 미쳤습니다. "
            f"이 값이 높을 때 상승 확률이 높았어요. "
        )
        if feat_imp.get("vol_ratio", 0) > 0.1:
            resp += "특히 거래량이 평소보다 높은 날에 상승이 자주 나타났습니다."
    elif any(k in message for k in ["패턴", "특징", "찾았"]):
        resp = (
            f"{model_name}은 '{top_name}'과 '{sec_name}' 조합에서 패턴을 발견했습니다. "
            f"정확도 {acc:.1f}%, AUC {auc:.3f}로 이 패턴이 어느 정도 유효함을 확인했습니다."
        )
    elif any(k in message for k in ["수익", "결과", "성과"]):
        verdict = "시장보다 나은" if port > bh else "개선이 필요한"
        resp = (
            f"전략 수익률 {port:+.1f}% vs 전량 보유 {bh:+.1f}%로 {verdict} 결과입니다. "
        )
        resp += "매수 신호를 잘 포착했네요! 🎉" if port > bh else "더 많은 데이터로 학습하면 개선될 수 있어요."
    elif any(k in message for k in ["모델", "알고리즘", "방법"]):
        descs = {
            "로지스틱 회귀": "직선으로 구분하는 가장 기본적인 방법이에요.",
            "랜덤 포레스트": "여러 결정 트리가 투표해서 결정해요.",
            "신경망": "인간의 뇌 구조를 흉내 낸 방법이에요.",
            "그래디언트 부스팅": "이전 실수를 보완하며 점점 발전하는 방법이에요.",
        }
        resp = f"{model_name}: {descs.get(model_name, '머신러닝 모델')} 정확도 {acc:.1f}%를 달성했습니다."
    elif any(k in message for k in ["개선", "향상", "더 좋게"]):
        resp = (
            f"현재 정확도 {acc:.1f}%를 개선하려면: "
            "1) 더 많은 데이터 추가, "
            "2) RSI·MACD 같은 추가 지표 활용, "
            "3) 다른 모델 시도해보기를 권장합니다."
        )
    else:
        resp = (
            f"{model_name}으로 분석 완료! 정확도 {acc:.1f}%, "
            f"가장 중요한 요소는 '{top_name}'입니다. "
            f"전략 수익률 {port:+.1f}% vs 보유 {bh:+.1f}%."
        )

    resp += "  (💡 Ollama Docker를 연결하면 더 풍부한 AI 설명을 받을 수 있어요.)"
    return resp


_ASSISTANT_COMPANY_ALIASES = {
    "삼성전자": "삼성전자",
    "005930": "삼성전자",
    "sk하이닉스": "SK하이닉스",
    "하이닉스": "SK하이닉스",
    "000660": "SK하이닉스",
    "카카오": "카카오",
    "035720": "카카오",
    "naver": "NAVER",
    "네이버": "NAVER",
    "035420": "NAVER",
    "현대자동차": "현대자동차",
    "현대차": "현대자동차",
    "005380": "현대자동차",
    "lg화학": "LG화학",
    "051910": "LG화학",
    "롯데호텔": "롯데호텔",
    "포스코a&c": "포스코A&C",
    "포스코a&c ": "포스코A&C",
    "포스코": "포스코A&C",
}

_TRADE_ROUTE_KEYWORDS = [
    "살까", "사도", "매수", "매도", "팔까", "관망", "들어가", "사야", "사면", "팔면",
]
_PRICE_ROUTE_KEYWORDS = [
    "종가", "가격", "주가", "얼마", "예측", "예상가", "목표가", "마감가",
]
_ANALYZE_ROUTE_KEYWORDS = [
    "분석", "추세", "패턴", "신호", "모델", "확률", "전망",
]
_EVENT_ROUTE_KEYWORDS = [
    "전쟁", "가뭄", "뉴스", "속보", "지정학", "금리", "cpi", "물가", "관세", "규제", "환율", "유가",
]


def _normalize_company_name(name: str | None) -> str:
    if not name:
        return ""
    raw = re.sub(r"\s+", "", str(name)).strip()
    raw = re.sub(r"(종목|주식|회사|기업)$", "", raw)
    if not raw:
        return ""

    normalized = raw.lower()
    for alias, company in sorted(_ASSISTANT_COMPANY_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if alias.lower() == normalized:
            return company
    return raw


def _extract_company_name(message: str) -> str:
    compact = re.sub(r"\s+", "", message)
    lowered = compact.lower()
    for alias, company in sorted(_ASSISTANT_COMPANY_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if alias.lower() in lowered:
            return company

    patterns = [
        r"(?:오늘|내일|이번주|이번\s*주|지금)?\s*([A-Za-z0-9가-힣&.\-]+)\s*(?:종목|주식)",
        r"(?:오늘|내일|이번주|이번\s*주|지금)?\s*([A-Za-z0-9가-힣&.\-]+)\s*(?:종가|주가|가격)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return _normalize_company_name(match.group(1))
    return ""


def _assistant_time_hint(message: str) -> str:
    today = date.today()
    if "내일" in message:
        return f"질문 속 '내일'은 {today + timedelta(days=1)} 기준으로 해석했어요."
    if "오늘" in message:
        return f"질문 속 '오늘'은 {today} 기준으로 해석했어요."
    return ""


def _assistant_route_fallback(message: str) -> dict[str, str]:
    clean = re.sub(r"\s+", " ", message).strip()
    company = _extract_company_name(clean) or "관심 종목"

    if any(keyword in clean for keyword in _PRICE_ROUTE_KEYWORDS):
        intent = "close_prediction"
        route_kind = "predict"
        route_label = "예측 실험실"
        title = f"{company} 종가 예측 질문"
        desc = f"{company}의 종가·가격 질문이어서 종가 예측과 다중 기업 비교에 맞는 예측 실험실로 안내할게요."
        reason = f"'{clean}'을 종가/가격 예측형 질문으로 이해했어요."
    elif any(keyword in clean for keyword in _EVENT_ROUTE_KEYWORDS):
        intent = "event_consult"
        route_kind = "advisor"
        route_label = "이벤트 컨설팅"
        title = "뉴스·이벤트 투자 컨설팅"
        desc = "전쟁, 가뭄, 물가, 규제 같은 사건이 업종과 시장에 어떤 영향을 줄지 보는 컨설팅 화면으로 안내할게요."
        reason = f"'{clean}'을 뉴스/이벤트 해석형 질문으로 이해했어요."
    elif any(keyword in clean for keyword in _TRADE_ROUTE_KEYWORDS):
        intent = "trading_decision"
        route_kind = "lab"
        route_label = "주식 AI 실험실"
        title = f"{company} 매수 판단 질문"
        desc = f"{company} 종목을 살지 말지 묻는 질문이어서 신호, 확률, 백테스트를 함께 보는 주식 AI 실험실로 안내할게요."
        reason = f"'{clean}'을 매수/관망 판단형 질문으로 이해했어요."
    elif any(keyword in clean for keyword in _ANALYZE_ROUTE_KEYWORDS):
        intent = "stock_analysis"
        route_kind = "lab"
        route_label = "주식 AI 실험실"
        title = f"{company} 분석 질문"
        desc = f"{company}의 패턴과 신호를 먼저 살펴보기 좋은 주식 AI 실험실로 연결할게요."
        reason = f"'{clean}'을 분석형 질문으로 이해했어요."
    else:
        intent = "general_stock_ai"
        route_kind = "lab"
        route_label = "주식 AI 실험실"
        title = "주식 AI 탐색 질문"
        desc = "질문이 넓어서 먼저 신호와 확률을 같이 볼 수 있는 주식 AI 실험실로 안내할게요."
        reason = "질문이 넓은 편이라 분석형 실습부터 시작하는 것이 자연스러워요."

    extra = _assistant_time_hint(clean)
    if extra:
        desc = f"{desc} {extra}"

    if route_kind == "predict":
        route = f"/predict?{urlencode({'assistant': intent, 'company': company, 'query': clean})}"
    elif route_kind == "advisor":
        route = f"/advisor?{urlencode({'assistant': intent, 'query': clean})}"
    else:
        route = f"/lab?{urlencode({'assistant': intent, 'company': company, 'query': clean, 'title': title, 'desc': desc})}"

    return {
        "intent": intent,
        "company": company,
        "route_kind": route_kind,
        "route_label": route_label,
        "route": route,
        "title": title,
        "description": desc,
        "reason": reason,
    }


async def _assistant_route_with_llm(message: str, fallback: dict[str, str]) -> dict[str, str]:
    prompt = (
        "당신은 주식 AI 학습 웹앱의 라우팅 도우미입니다.\n"
        "사용자 질문을 보고 아래 JSON만 출력하세요.\n"
        '형식: {"intent":"trading_decision|close_prediction|stock_analysis|general_stock_ai|event_consult","company":"회사명","reason":"짧은 이유"}\n'
        "규칙:\n"
        "- 매수/매도/살까 말까/관망 질문은 trading_decision\n"
        "- 종가/가격/얼마/예상가 질문은 close_prediction\n"
        "- 패턴/추세/분석 질문은 stock_analysis\n"
        "- 전쟁/가뭄/물가/금리/관세/규제/뉴스 해석 질문은 event_consult\n"
        "- 회사명이 없으면 빈 문자열\n"
        "- JSON 외의 문장은 절대 쓰지 마세요.\n\n"
        f"사용자 질문: {message}"
    )
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        )
        resp.raise_for_status()
        raw = resp.json().get("response", "").strip()

    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not match:
        return fallback

    parsed = json.loads(match.group(0))
    intent = str(parsed.get("intent", fallback["intent"])).strip()
    company = _normalize_company_name(parsed.get("company")) or fallback["company"]
    reason = str(parsed.get("reason", fallback["reason"])).strip() or fallback["reason"]

    if intent not in {"trading_decision", "close_prediction", "stock_analysis", "general_stock_ai", "event_consult"}:
        intent = fallback["intent"]

    merged = _assistant_route_fallback(message)
    merged["intent"] = intent
    merged["company"] = company
    merged["reason"] = reason

    if intent == "close_prediction":
        merged["route_kind"] = "predict"
        merged["route_label"] = "예측 실험실"
        merged["title"] = f"{company} 종가 예측 질문"
        merged["description"] = f"{company}의 종가나 가격을 묻는 질문으로 이해했어요. 예측 실험실에서 종가 예측 흐름으로 이어가겠습니다. {_assistant_time_hint(message)}".strip()
        merged["route"] = f"/predict?{urlencode({'assistant': intent, 'company': company, 'query': message})}"
    elif intent == "event_consult":
        merged["route_kind"] = "advisor"
        merged["route_label"] = "이벤트 컨설팅"
        merged["title"] = "뉴스·이벤트 투자 컨설팅"
        merged["description"] = f"전쟁, 가뭄, 금리, 규제 같은 뉴스가 업종과 시장에 미치는 영향을 읽는 컨설팅 화면으로 이어가겠습니다. {_assistant_time_hint(message)}".strip()
        merged["route"] = f"/advisor?{urlencode({'assistant': intent, 'query': message})}"
    elif intent in {"trading_decision", "stock_analysis", "general_stock_ai"}:
        merged["route_kind"] = "lab"
        merged["route_label"] = "주식 AI 실험실"
        if intent == "trading_decision":
            merged["title"] = f"{company} 매수 판단 질문"
            merged["description"] = f"{company} 종목을 살지 말지 판단하는 질문으로 이해했어요. 신호, 확률, 백테스트를 보는 주식 AI 실험실로 연결하겠습니다. {_assistant_time_hint(message)}".strip()
        else:
            merged["title"] = f"{company} 분석 질문"
            merged["description"] = f"{company}의 패턴과 신호를 먼저 읽는 질문으로 이해했어요. 분석형 실습에 맞는 주식 AI 실험실로 연결하겠습니다. {_assistant_time_hint(message)}".strip()
        merged["route"] = f"/lab?{urlencode({'assistant': intent, 'company': company, 'query': message, 'title': merged['title'], 'desc': merged['description']})}"

    return merged


# ---------------------------------------------------------------------------
# API 라우터 — 챕터
# ---------------------------------------------------------------------------

@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": "2.0.0"}


@app.get("/api/chapters", response_model=list[ChapterSummary], tags=["chapters"])
def list_chapters() -> list[ChapterSummary]:
    return [_build_summary(d) for d in _list_chapter_dirs()]


@app.get("/api/chapters/{chapter_id}", response_model=ChapterDetail, tags=["chapters"])
def get_chapter(chapter_id: str) -> ChapterDetail:
    chapter_dir = _chapter_dir(chapter_id)
    summary = _build_summary(chapter_dir)
    readme_path = chapter_dir / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    return ChapterDetail(**summary.model_dump(), readme=readme)


@app.get("/api/chapters/{chapter_id}/source", response_model=ChapterSourceResponse, tags=["chapters"])
def chapter_source(chapter_id: str) -> ChapterSourceResponse:
    chapter_path = _chapter_dir(chapter_id) / "practice.py"
    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'의 소스 파일을 찾을 수 없어요.")
    return ChapterSourceResponse(chapter=chapter_id, source=chapter_path.read_text(encoding="utf-8"))


@app.get("/api/chapters/{chapter_id}/source/raw", response_class=StreamingResponse, tags=["chapters"])
def chapter_source_raw(chapter_id: str) -> StreamingResponse:
    chapter_path = _chapter_dir(chapter_id) / "practice.py"
    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'의 소스 파일을 찾을 수 없어요.")
    return StreamingResponse(
        iter([chapter_path.read_text(encoding="utf-8")]),
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'inline; filename="{chapter_id}-practice.py"'},
    )


@app.post("/api/chapters/{chapter_id}/run", response_model=ChapterRunResponse, tags=["chapters"])
def run_chapter(chapter_id: str, req: ChapterRunRequest | None = None) -> ChapterRunResponse:
    params = req.params if req else None
    result, elapsed_ms, stdout = _exec_run(chapter_id, params)
    meta = _parse_practice_meta(_chapter_dir(chapter_id) / "practice.py")
    return ChapterRunResponse(chapter=chapter_id, topic=meta["topic"], result=result,
                               elapsed_ms=elapsed_ms, stdout=stdout)


# ---------------------------------------------------------------------------
# API 라우터 — 문서
# ---------------------------------------------------------------------------

@app.get("/api/docs", response_model=list[DocSummary], tags=["docs"])
def list_docs() -> list[DocSummary]:
    return _list_docs()


@app.get("/api/docs/{doc_id}", response_model=DocDetail, tags=["docs"])
def get_doc(doc_id: str) -> DocDetail:
    md_path = DOCS_DIR / f"{doc_id}.md"
    if not md_path.exists():
        raise HTTPException(status_code=404, detail=f"문서 '{doc_id}.md'를 찾을 수 없어요.")
    content = md_path.read_text(encoding="utf-8")
    return DocDetail(id=doc_id, title=_doc_title(md_path), filename=md_path.name, content=content)


@app.get("/api/datasets", response_model=list[DatasetSummary], tags=["datasets"])
def list_datasets() -> list[DatasetSummary]:
    results: list[DatasetSummary] = []
    for dataset_id in sorted(_DATASET_META):
        try:
            detail = _build_dataset_detail(dataset_id)
        except HTTPException as exc:
            if exc.status_code == 404:
                continue
            raise
        results.append(
            DatasetSummary(
                id=detail.id,
                filename=detail.filename,
                title=detail.title,
                description=detail.description,
                rows=detail.rows,
                n_columns=detail.n_columns,
                recommended_webapp=detail.recommended_webapp,
                practice_label=detail.practice_label,
            )
        )
    return results


@app.get("/api/datasets/{dataset_id}", response_model=DatasetDetail, tags=["datasets"])
def get_dataset(dataset_id: str) -> DatasetDetail:
    return _build_dataset_detail(dataset_id)


@app.get("/api/datasets/{dataset_id}/adapted/stock-lab", tags=["datasets"])
def get_dataset_for_stock_lab(dataset_id: str) -> dict[str, Any]:
    if dataset_id == "stock_ohlcv":
        df = _ensure_ohlcv_frame(pd.read_csv(DATA_DIR / "stock_ohlcv.csv"))
        if len(df) < 40:
            extra_n = 40 - len(df)
            last_date = df["date"].iloc[-1]
            extra_dates = pd.date_range(_next_business_day(last_date), periods=extra_n, freq="B")
            last_close = float(df["close"].iloc[-1])
            drift = np.linspace(0.001, 0.012, extra_n)
            extra_close = [last_close * (1 + d) for d in drift]
            last_volume = float(df["volume"].iloc[-1])
            extra_volume = [last_volume * (1 + 0.02 * idx) for idx in range(extra_n)]
            extra_open = [last_close * (1 + d * 0.4) for d in drift]
            extra_high = [max(o, c) * 1.008 for o, c in zip(extra_open, extra_close)]
            extra_low = [min(o, c) * 0.992 for o, c in zip(extra_open, extra_close)]
            extra_df = pd.DataFrame({
                "date": extra_dates,
                "open": extra_open,
                "high": extra_high,
                "low": extra_low,
                "close": extra_close,
                "volume": extra_volume,
            })
            df = pd.concat([df[["date", "open", "high", "low", "close", "volume"]], extra_df], ignore_index=True)
            df = _ensure_ohlcv_frame(df)
        rows = [
            {
                "date": d.strftime("%Y-%m-%d"),
                "open": round(float(o), 4),
                "high": round(float(h), 4),
                "low": round(float(l), 4),
                "close": round(float(c), 4),
                "volume": int(v),
            }
            for d, o, h, l, c, v in zip(df["date"], df["open"], df["high"], df["low"], df["close"], df["volume"])
        ]
        return {
            "dataset_id": dataset_id,
            "title": _DATASET_META[dataset_id]["title"],
            "note": "대표 종목 OHLCV 시계열을 그대로 불러옵니다. 캔들차트와 내일 예측 점 표시까지 바로 확인할 수 있어요.",
            "rows": rows,
        }

    if dataset_id == "traffic_timeseries":
        df = _ensure_ohlcv_frame(pd.read_csv(DATA_DIR / "traffic_timeseries.csv"))
        if len(df) < 40:
            extra_n = 40 - len(df)
            last_date = df["date"].iloc[-1]
            last_close = float(df["close"].iloc[-1])
            extra_dates = pd.date_range(_next_business_day(last_date), periods=extra_n, freq="B")
            wave = np.sin(np.linspace(0, 3.14, extra_n)) * (last_close * 0.012)
            trend = np.linspace(last_close * 0.002, last_close * 0.018, extra_n)
            extra_close = np.clip(last_close + trend + wave, 1, None)
            last_volume = float(df["volume"].iloc[-1])
            extra_volume = np.linspace(last_volume * 0.95, last_volume * 1.12, extra_n)
            extra_open = extra_close * (1 - 0.004)
            extra_high = extra_close * (1 + 0.006)
            extra_low = extra_close * (1 - 0.007)
            df = pd.concat(
                [df[["date", "open", "high", "low", "close", "volume"]], pd.DataFrame({
                    "date": extra_dates,
                    "open": extra_open,
                    "high": extra_high,
                    "low": extra_low,
                    "close": extra_close,
                    "volume": extra_volume,
                })],
                ignore_index=True,
            )
            df = _ensure_ohlcv_frame(df)
        rows = [
            {
                "date": d.strftime("%Y-%m-%d"),
                "open": round(float(o), 4),
                "high": round(float(h), 4),
                "low": round(float(l), 4),
                "close": round(float(c), 4),
                "volume": int(v),
            }
            for d, o, h, l, c, v in zip(df["date"], df["open"], df["high"], df["low"], df["close"], df["volume"])
        ]
        return {
            "dataset_id": dataset_id,
            "title": _DATASET_META[dataset_id]["title"],
            "note": "섹터 ETF 시계열을 OHLCV 형식으로 보강해 캔들차트 실습과 내일 예측 표시까지 함께 볼 수 있게 만들었습니다.",
            "rows": rows,
        }

    raise HTTPException(
        status_code=400,
        detail=f"'{dataset_id}'는 주식 AI 실험실 형식(date, open, high, low, close, volume)으로 바로 변환할 수 없는 데이터셋입니다.",
    )


# ---------------------------------------------------------------------------
# API 라우터 — DART 공시 투자 파이프라인
# ---------------------------------------------------------------------------

def _load_dart_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=(
                f"{name}.csv 가 아직 없어요. "
                "먼저 `DART_API_KEY=... python scripts/refresh_datasets.py` 로 생성해주세요."
            ),
        )
    df = pd.read_csv(path)
    if "stock_code" in df.columns:
        df["stock_code"] = (
            df["stock_code"]
            .apply(lambda v: "" if pd.isna(v) else str(v).split(".")[0])
            .str.zfill(6)
        )
    if "corp_code" in df.columns:
        df["corp_code"] = (
            df["corp_code"]
            .apply(lambda v: "" if pd.isna(v) else str(v).split(".")[0])
            .str.zfill(8)
        )
    for col in ["receipt_date", "latest_receipt_date", "receipt_no"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda v: "" if pd.isna(v) else str(v).split(".")[0])
    return df


@app.get("/api/dart/overview", tags=["dart"])
def dart_overview() -> dict[str, Any]:
    pipeline = _load_dart_csv("dart_invest_pipeline")
    fundamentals = _load_dart_csv("dart_fundamentals")
    disclosures = _load_dart_csv("dart_disclosures")
    years = sorted(pd.to_numeric(fundamentals["year"], errors="coerce").dropna().astype(int).unique().tolist())
    top = pipeline.sort_values("signal_score", ascending=False).head(3)
    top_companies = [
        {
            "stock_code": str(row["stock_code"]),
            "corp_name": row["corp_name"],
            "signal_score": round(float(row["signal_score"]), 1),
            "investment_view": row["investment_view"],
        }
        for _, row in top.iterrows()
    ]
    return {
        "company_count": int(pipeline["stock_code"].nunique()),
        "fundamental_rows": int(len(fundamentals)),
        "disclosure_rows": int(len(disclosures)),
        "years": years,
        "top_companies": top_companies,
        "dataset_files": [
            "dart_fundamentals.csv",
            "dart_disclosures.csv",
            "dart_invest_pipeline.csv",
        ],
    }


@app.get("/api/dart/companies", tags=["dart"])
def dart_companies() -> list[dict[str, Any]]:
    pipeline = _load_dart_csv("dart_invest_pipeline")
    pipeline = pipeline.sort_values("signal_score", ascending=False)
    results: list[dict[str, Any]] = []
    for _, row in pipeline.iterrows():
        results.append({
            "stock_code": str(row.get("stock_code", "")),
            "ticker": row.get("ticker", ""),
            "corp_name": row.get("corp_name", ""),
            "sector": row.get("sector", ""),
            "year": int(row.get("year", 0)),
            "signal_score": round(float(row.get("signal_score", 0.0)), 1),
            "investment_view": row.get("investment_view", ""),
            "investment_reason": row.get("investment_reason", ""),
            "revenue_tn_krw": None if pd.isna(row.get("revenue_tn_krw")) else round(float(row["revenue_tn_krw"]), 2),
            "operating_income_tn_krw": None if pd.isna(row.get("operating_income_tn_krw")) else round(float(row["operating_income_tn_krw"]), 2),
            "roe": None if pd.isna(row.get("roe")) else round(float(row["roe"]), 2),
            "debt_ratio": None if pd.isna(row.get("debt_ratio")) else round(float(row["debt_ratio"]), 2),
            "momentum_3m": None if pd.isna(row.get("momentum_3m")) else round(float(row["momentum_3m"]), 4),
            "latest_report_name": row.get("latest_report_name", ""),
            "latest_receipt_date": str(row.get("latest_receipt_date", "")),
        })
    return results


@app.get("/api/dart/companies/{stock_code}", tags=["dart"])
def dart_company_detail(stock_code: str) -> dict[str, Any]:
    normalized = stock_code.replace(".KS", "").strip()
    pipeline = _load_dart_csv("dart_invest_pipeline")
    fundamentals = _load_dart_csv("dart_fundamentals")
    disclosures = _load_dart_csv("dart_disclosures")

    company_row = pipeline[pipeline["stock_code"].astype(str) == normalized]
    if company_row.empty:
        raise HTTPException(status_code=404, detail=f"DART 데이터에서 종목코드 '{normalized}'를 찾지 못했어요.")
    company = company_row.iloc[0].to_dict()

    fundamentals_df = fundamentals[fundamentals["stock_code"].astype(str) == normalized].sort_values("year")
    disclosure_df = disclosures[disclosures["stock_code"].astype(str) == normalized].sort_values("receipt_date", ascending=False)

    note_parts: list[str] = []
    if pd.notna(company.get("revenue_yoy")) and float(company["revenue_yoy"]) > 0:
        note_parts.append("매출이 전년보다 커졌어요.")
    if pd.notna(company.get("operating_income_yoy")) and float(company["operating_income_yoy"]) > 0:
        note_parts.append("영업이익도 함께 좋아지고 있어요.")
    if pd.notna(company.get("debt_ratio")) and float(company["debt_ratio"]) < 120:
        note_parts.append("부채비율이 비교적 낮아서 재무 체력이 괜찮은 편이에요.")
    if pd.notna(company.get("momentum_3m")) and float(company["momentum_3m"]) > 0:
        note_parts.append("최근 3개월 주가 흐름도 나쁘지 않아요.")
    if not note_parts:
        note_parts.append("숫자가 아주 강하진 않아서 공시를 하나씩 더 확인하며 보는 편이 좋아요.")

    return {
        "company": {
            "stock_code": normalized,
            "ticker": company.get("ticker", ""),
            "corp_name": company.get("corp_name", ""),
            "sector": company.get("sector", ""),
            "year": int(company.get("year", 0)),
            "signal_score": round(float(company.get("signal_score", 0.0)), 1),
            "investment_view": company.get("investment_view", ""),
            "investment_reason": company.get("investment_reason", ""),
            "consultant_note": " ".join(note_parts),
            "revenue_yoy": None if pd.isna(company.get("revenue_yoy")) else round(float(company.get("revenue_yoy", 0.0)), 2),
            "operating_margin": None if pd.isna(company.get("operating_margin")) else round(float(company.get("operating_margin", 0.0)), 2),
            "debt_ratio": None if pd.isna(company.get("debt_ratio")) else round(float(company.get("debt_ratio", 0.0)), 2),
            "momentum_3m": None if pd.isna(company.get("momentum_3m")) else round(float(company.get("momentum_3m", 0.0)), 4),
            "latest_report_name": company.get("latest_report_name", ""),
            "latest_receipt_date": str(company.get("latest_receipt_date", "")),
        },
        "fundamentals": fundamentals_df.fillna("").to_dict(orient="records"),
        "disclosures": disclosure_df.head(10).fillna("").to_dict(orient="records"),
    }


# ---------------------------------------------------------------------------
# API 라우터 — 외부 데이터 기반 거시경제 투자 파이프라인
# ---------------------------------------------------------------------------

@app.get("/api/macro/overview", tags=["macro"])
def macro_overview() -> dict[str, Any]:
    fred_df = _load_dart_csv("macro_fred_signals")
    world_bank_df = _load_dart_csv("world_bank_korea_indicators")
    macro_df = _load_dart_csv("external_macro_pipeline")
    ml_df = _load_dart_csv("external_invest_ml_dataset")
    latest_year = int(pd.to_numeric(macro_df["year"], errors="coerce").dropna().max())
    latest = macro_df[pd.to_numeric(macro_df["year"], errors="coerce") == latest_year].iloc[0].to_dict()
    recommendations = [
        {
            "name": "DART",
            "kind": "공시/재무",
            "implemented": True,
            "key_required": True,
            "note": "한국 상장사 공식 공시와 재무제표 수집",
        },
        {
            "name": "FRED",
            "kind": "거시경제",
            "implemented": True,
            "key_required": False,
            "note": "금리, CPI, 실업률, VIX, 유가 같은 글로벌 거시 신호 수집",
        },
        {
            "name": "World Bank",
            "kind": "국가 구조지표",
            "implemented": True,
            "key_required": False,
            "note": "한국 GDP 성장률, 수출 비중 같은 장기 구조 데이터 수집",
        },
        {
            "name": "KOSIS",
            "kind": "국내 통계",
            "implemented": False,
            "key_required": True,
            "note": "국내 산업생산, 고용, 소비지표 확장 추천",
        },
        {
            "name": "Alpha Vantage",
            "kind": "가격/뉴스/기술지표",
            "implemented": False,
            "key_required": True,
            "note": "해외 주가, 경제지표, 뉴스 감성, 기술지표 확장 추천",
        },
    ]
    return {
        "fred_rows": int(len(fred_df)),
        "world_bank_rows": int(len(world_bank_df)),
        "macro_rows": int(len(macro_df)),
        "ml_rows": int(len(ml_df)),
        "latest_year": latest_year,
        "latest_macro": {
            "fred_fedfunds": None if pd.isna(latest.get("fred_fedfunds")) else round(float(latest["fred_fedfunds"]), 2),
            "fred_cpi_yoy": None if pd.isna(latest.get("fred_cpi_yoy")) else round(float(latest["fred_cpi_yoy"]), 2),
            "fred_unrate": None if pd.isna(latest.get("fred_unrate")) else round(float(latest["fred_unrate"]), 2),
            "fred_vix": None if pd.isna(latest.get("fred_vix")) else round(float(latest["fred_vix"]), 2),
            "wb_gdp_growth": None if pd.isna(latest.get("wb_gdp_growth")) else round(float(latest["wb_gdp_growth"]), 2),
            "wb_exports_gdp": None if pd.isna(latest.get("wb_exports_gdp")) else round(float(latest["wb_exports_gdp"]), 2),
        },
        "recommendations": recommendations,
    }


@app.get("/api/macro/dataset", tags=["macro"])
def macro_dataset_preview() -> dict[str, Any]:
    df = _load_dart_csv("external_invest_ml_dataset")
    preview = df.head(18).fillna("").to_dict(orient="records")
    return {
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns.tolist()],
        "preview": preview,
    }


@app.post("/api/macro/train", tags=["macro"])
def macro_train() -> dict[str, Any]:
    from sklearn.ensemble import RandomForestClassifier  # noqa: PLC0415
    from sklearn.linear_model import LogisticRegression  # noqa: PLC0415
    from sklearn.metrics import accuracy_score, roc_auc_score  # noqa: PLC0415
    from sklearn.neural_network import MLPClassifier  # noqa: PLC0415
    from sklearn.pipeline import Pipeline  # noqa: PLC0415
    from sklearn.preprocessing import StandardScaler  # noqa: PLC0415
    from sklearn.model_selection import train_test_split  # noqa: PLC0415

    df = _load_dart_csv("external_invest_ml_dataset")
    if len(df) < 12:
        raise HTTPException(status_code=400, detail="외부 데이터 학습셋이 너무 작아요.")

    feature_cols = [
        "revenue_tn_krw",
        "operating_income_tn_krw",
        "operating_margin",
        "net_margin",
        "roe",
        "debt_ratio",
        "current_ratio",
        "revenue_yoy",
        "operating_income_yoy",
        "fred_fedfunds",
        "fred_cpi_yoy",
        "fred_unrate",
        "fred_dgs10",
        "fred_vix",
        "fred_oil_wti",
        "wb_cpi_inflation",
        "wb_exports_gdp",
        "wb_gdp_growth",
        "wb_unemployment",
    ]
    clean = df.copy()
    clean["year"] = pd.to_numeric(clean["year"], errors="coerce")
    clean["label_next_income_up"] = pd.to_numeric(clean["label_next_income_up"], errors="coerce")
    clean = clean.dropna(subset=["year", "label_next_income_up"]).copy()
    for col in feature_cols:
        clean[col] = pd.to_numeric(clean[col], errors="coerce")
        if clean[col].isna().all():
            clean[col] = 0.0
        else:
            clean[col] = clean[col].fillna(clean[col].median())
    X = clean[feature_cols].astype(float)
    y = clean["label_next_income_up"].astype(int)
    stratify = y if len(set(y)) > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=stratify,
    )

    models = {
        "logistic": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=2000)),
        ]),
        "rf": RandomForestClassifier(n_estimators=250, random_state=42, max_depth=5),
        "nn": Pipeline([
            ("scaler", StandardScaler()),
            ("model", MLPClassifier(hidden_layer_sizes=(48, 24), max_iter=3000, random_state=42)),
        ]),
    }
    results: list[dict[str, Any]] = []
    for key, model in models.items():
        model.fit(X_train, y_train)
        probs = model.predict_proba(X_test)[:, 1]
        preds = (probs >= 0.5).astype(int)
        auc = roc_auc_score(y_test, probs) if len(set(y_test)) > 1 else None
        top_features: list[dict[str, Any]]
        if key == "rf":
            importances = model.feature_importances_
            order = np.argsort(importances)[::-1][:5]
            top_features = [{"name": feature_cols[idx], "score": round(float(importances[idx]), 4)} for idx in order]
        elif key == "logistic":
            coefs = model.named_steps["model"].coef_[0]
            order = np.argsort(np.abs(coefs))[::-1][:5]
            top_features = [{"name": feature_cols[idx], "score": round(float(coefs[idx]), 4)} for idx in order]
        else:
            top_features = [{"name": "복합 비선형 패턴", "score": 1.0}]
        results.append({
            "model": key,
            "accuracy": round(float(accuracy_score(y_test, preds)), 4),
            "auc": None if auc is None else round(float(auc), 4),
            "top_features": top_features,
        })

    best = max(results, key=lambda item: ((item["auc"] or 0.0), item["accuracy"]))
    latest_rows = clean.sort_values(["year", "corp_name"]).tail(8)[["corp_name", "year"] + feature_cols[:6] + ["label_next_income_up"]]
    return {
        "target_label": "다음 해 영업이익 증가 여부",
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "feature_count": len(feature_cols),
        "results": results,
        "best_model": best,
        "sample_rows": latest_rows.fillna("").to_dict(orient="records"),
    }


# ---------------------------------------------------------------------------
# API 라우터 — 주식 AI 실험실
# ---------------------------------------------------------------------------

@app.post("/api/stock/analyze", tags=["stock"])
def stock_analyze(req: StockAnalyzeRequest) -> dict[str, Any]:
    """주가 데이터를 받아 선택한 ML 모델로 분석하고 평가 결과를 반환합니다."""
    import numpy as np  # noqa: PLC0415
    import pandas as pd  # noqa: PLC0415
    from sklearn.ensemble import (  # noqa: PLC0415
        GradientBoostingClassifier,
        GradientBoostingRegressor,
        RandomForestClassifier,
        RandomForestRegressor,
    )
    from sklearn.linear_model import LogisticRegression, Ridge  # noqa: PLC0415
    from sklearn.metrics import (  # noqa: PLC0415
        accuracy_score,
        mean_absolute_error,
        mean_squared_error,
        precision_score,
        r2_score,
        roc_auc_score,
    )
    from sklearn.neural_network import MLPClassifier, MLPRegressor  # noqa: PLC0415
    from sklearn.preprocessing import StandardScaler  # noqa: PLC0415

    if len(req.rows) < 25:
        raise HTTPException(status_code=400, detail="최소 25행 이상 입력해주세요.")

    raw_df = pd.DataFrame([
        {
            "date": r.date,
            "open": r.open,
            "high": r.high,
            "low": r.low,
            "close": r.close,
            "volume": r.volume,
        }
        for r in req.rows
    ])
    df = _ensure_ohlcv_frame(raw_df)
    if len(df) < 25:
        raise HTTPException(status_code=400, detail="유효한 OHLCV 데이터가 부족합니다.")

    ma5 = df["close"].rolling(5).mean()
    ma20 = df["close"].rolling(20).mean()
    df["ret"] = df["close"].pct_change()
    df["ret_5"] = df["close"].pct_change(5)
    df["ma5_gap"] = (df["close"] / ma5) - 1.0
    df["ma20_gap"] = (df["close"] / ma20) - 1.0
    df["vol_ratio"] = df["volume"] / df["volume"].rolling(10).mean()
    df["range_pct"] = (df["high"] - df["low"]) / df["close"].replace(0, np.nan)
    df["body_pct"] = (df["close"] - df["open"]) / df["open"].replace(0, np.nan)
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)
    df["target_close"] = df["close"].shift(-1)
    df["target_ret"] = (df["close"].shift(-1) / df["close"]) - 1.0

    feature_rows = df.dropna(subset=[
        "ret", "ret_5", "ma5_gap", "ma20_gap", "vol_ratio", "range_pct", "body_pct",
    ]).reset_index(drop=True)
    supervised = feature_rows.dropna(subset=["target_close", "target_ret"]).reset_index(drop=True)

    if len(supervised) < 15:
        raise HTTPException(status_code=400, detail="유효 데이터 부족 — 행을 더 추가해주세요.")

    features = ["ret", "ret_5", "ma5_gap", "ma20_gap", "vol_ratio", "range_pct", "body_pct"]
    X = supervised[features].values
    y = supervised["target"].values
    y_ret = supervised["target_ret"].values
    current_close = supervised["close"].values
    y_close = supervised["target_close"].values

    split = max(int(len(X) * 0.8), len(X) - 15)
    split = min(split, len(X) - 5)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    y_ret_train, y_ret_test = y_ret[:split], y_ret[split:]
    current_close_test = current_close[split:]
    y_close_test = y_close[split:]

    if len(X_test) < 2:
        raise HTTPException(status_code=400, detail="테스트 데이터 부족 — 행을 더 추가해주세요.")

    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_te_sc = scaler.transform(X_test)

    clf_model_map = {
        "logistic": LogisticRegression(random_state=42, max_iter=300),
        "rf":       RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42),
        "nn":       MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42),
        "gbm":      GradientBoostingClassifier(n_estimators=50, max_depth=3, random_state=42),
    }
    reg_model_map = {
        "logistic": Ridge(alpha=1.0),
        "rf":       RandomForestRegressor(n_estimators=80, max_depth=6, random_state=42),
        "nn":       MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42),
        "gbm":      GradientBoostingRegressor(n_estimators=80, max_depth=3, random_state=42),
    }
    name_map = {
        "logistic": "로지스틱 회귀",
        "rf":       "랜덤 포레스트",
        "nn":       "신경망",
        "gbm":      "그래디언트 부스팅",
    }
    method_map = {
        "logistic": {
            "classification": "로지스틱 회귀로 다음 날 상승/하락 확률을 분류했습니다.",
            "regression": "가격 예측은 같은 선형 계열인 Ridge 회귀로 안정적으로 추정했습니다.",
            "reason": "데이터 수가 많지 않을 때도 기준선을 해석하기 쉽고, 어떤 특성이 위아래로 작용했는지 설명하기 좋습니다.",
        },
        "rf": {
            "classification": "랜덤 포레스트가 여러 결정트리의 투표로 다음 날 방향을 분류했습니다.",
            "regression": "내일 종가는 RandomForestRegressor로 비선형 패턴을 함께 반영했습니다.",
            "reason": "OHLCV에서 자주 나오는 비선형 관계와 분기 규칙을 잘 잡고, 과적합도 비교적 잘 제어합니다.",
        },
        "nn": {
            "classification": "다층 퍼셉트론이 OHLCV 특징을 비선형으로 조합해 상승 확률을 계산했습니다.",
            "regression": "내일 종가도 MLP 회귀기로 같은 신경망 계열에서 추정했습니다.",
            "reason": "캔들 몸통, 변동폭, 이동평균 괴리처럼 상호작용이 있는 입력에서 복합 패턴을 학습하기 좋습니다.",
        },
        "gbm": {
            "classification": "그래디언트 부스팅이 이전 트리의 오차를 보완하며 방향성을 분류했습니다.",
            "regression": "내일 종가도 GradientBoostingRegressor로 잔차를 순차적으로 줄여 예측했습니다.",
            "reason": "작은 특징 차이와 최근 추세 변화에 민감하게 반응해 OHLCV 시계열의 국소 패턴을 잘 잡습니다.",
        },
    }
    model_key = req.model if req.model in clf_model_map else "rf"
    m = clf_model_map[model_key]
    reg = reg_model_map[model_key]
    m.fit(X_tr_sc, y_train)
    reg.fit(X_tr_sc, y_ret_train)

    y_pred = m.predict(X_te_sc)
    y_prob = m.predict_proba(X_te_sc)[:, 1]
    ret_pred_test = reg.predict(X_te_sc)
    close_pred_test = current_close_test * (1.0 + ret_pred_test)

    acc  = float(accuracy_score(y_test, y_pred))
    try:
        auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        auc = 0.5
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    mae = float(mean_absolute_error(y_close_test, close_pred_test))
    rmse = float(np.sqrt(mean_squared_error(y_close_test, close_pred_test)))
    r2 = float(r2_score(y_close_test, close_pred_test)) if len(y_close_test) >= 2 else 0.0
    if not np.isfinite(r2):
        r2 = 0.0

    # Feature importance
    feat_imp: dict[str, float] = {}
    if hasattr(m, "feature_importances_"):
        for f, v in zip(features, m.feature_importances_):
            feat_imp[f] = round(float(v), 4)
    elif hasattr(m, "coef_"):
        raw = np.abs(m.coef_[0])
        total = raw.sum() or 1.0
        for f, v in zip(features, raw / total):
            feat_imp[f] = round(float(v), 4)
    else:
        rng = np.random.default_rng(42)
        base_acc = float(accuracy_score(y_test, y_pred))
        for idx, f in enumerate(features):
            Xp = X_te_sc.copy()
            rng.shuffle(Xp[:, idx])
            drop = base_acc - float(accuracy_score(y_test, m.predict(Xp)))
            feat_imp[f] = round(max(drop, 0.0), 4)

    # Trading simulation
    test_rets = supervised["ret"].values[split: split + len(y_test)]
    portfolio, buyhold = [1.0], [1.0]
    for i, ret in enumerate(test_rets[: len(y_prob)]):
        if y_prob[i] >= 0.55:
            portfolio.append(portfolio[-1] * (1.0 + ret))
        else:
            portfolio.append(portfolio[-1])
        buyhold.append(buyhold[-1] * (1.0 + ret))

    # Prediction signals (up to last 20)
    signals = []
    for i in range(min(len(y_pred), 20)):
        row_idx = split + i
        signals.append({
            "date":    str(supervised["date"].iloc[row_idx].date()),
            "close":   round(float(supervised["close"].iloc[row_idx]), 0),
            "signal":  "매수" if y_prob[i] >= 0.55 else "관망",
            "prob":    round(float(y_prob[i]) * 100, 1),
            "actual":  "상승" if y_test[i] == 1 else "하락",
            "correct": bool(y_pred[i] == y_test[i]),
        })

    latest_features = feature_rows.iloc[[-1]][features].values
    latest_scaled = scaler.transform(latest_features)
    last_close = float(feature_rows["close"].iloc[-1])
    raw_next_ret = float(reg.predict(latest_scaled)[0])
    raw_next_close = last_close * (1.0 + raw_next_ret)
    recent_vol = float(feature_rows["ret"].tail(20).std() or 0.0)
    max_move = max(0.05, recent_vol * 3.2)
    predicted_next_close = float(np.clip(raw_next_close, last_close * (1 - max_move), last_close * (1 + max_move)))
    predicted_move_pct = ((predicted_next_close / last_close) - 1.0) * 100.0
    last_date = pd.Timestamp(feature_rows["date"].iloc[-1])
    next_date = _next_business_day(last_date)

    candle_rows = [
        {
            "date": row["date"].strftime("%Y-%m-%d"),
            "open": round(float(row["open"]), 4),
            "high": round(float(row["high"]), 4),
            "low": round(float(row["low"]), 4),
            "close": round(float(row["close"]), 4),
            "volume": int(row["volume"]),
        }
        for _, row in feature_rows.tail(80).iterrows()
    ]

    sorted_feats = sorted(feat_imp.items(), key=lambda item: item[1], reverse=True)
    top_features = [_FEAT_NAMES.get(key, key) for key, _ in sorted_feats[:3]]
    method_info = method_map[model_key]

    # ── 신경망 시각화 데이터 (nn 모델 전용) ──────────────────────────
    nn_viz: dict[str, Any] | None = None
    if model_key == "nn":
        _feat_labels = {
            "ret": "당일수익", "ret_5": "5일수익",
            "ma5_gap": "MA5괴리", "ma20_gap": "MA20괴리", "vol_ratio": "거래량비",
            "range_pct": "고저폭", "body_pct": "몸통비율",
        }

        def _stock_mlp_forward(x_row: np.ndarray) -> list[list[float]]:
            x = x_row.reshape(1, -1).copy()
            acts: list[list[float]] = [x[0].tolist()]
            fn = m.activation
            for w, b in zip(m.coefs_[:-1], m.intercepts_[:-1]):
                x = x @ w + b
                if fn == "relu":
                    np.maximum(x, 0, out=x)
                elif fn == "tanh":
                    np.tanh(x, out=x)
                else:
                    x = 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
                acts.append(x[0].tolist())
            x = x @ m.coefs_[-1] + m.intercepts_[-1]
            x = 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
            acts.append(x[0].tolist())
            return acts

        _hi_idx = int(np.argmax(y_prob))
        _lo_idx = int(np.argmin(y_prob))
        hi_acts = _stock_mlp_forward(X_te_sc[_hi_idx])
        lo_acts = _stock_mlp_forward(X_te_sc[_lo_idx])

        _MAX_DISP = 8

        def _top_k_abs(vals: list[float], k: int) -> list[int]:
            return sorted(sorted(range(len(vals)), key=lambda i: abs(vals[i]), reverse=True)[:k])

        _hidden_sizes = (
            list(m.hidden_layer_sizes)
            if isinstance(m.hidden_layer_sizes, (list, tuple))
            else [int(m.hidden_layer_sizes)]
        )
        _layer_sizes_full = [len(features)] + [int(h) for h in _hidden_sizes] + [1]
        _disp_input = list(range(len(features)))  # show all 5 input features

        _disp_hidden = [
            _top_k_abs(hi_acts[li], min(_MAX_DISP, len(hi_acts[li])))
            for li in range(1, len(_hidden_sizes) + 1)
        ]
        _disp_indices = [_disp_input] + _disp_hidden + [[0]]

        def _w_sub(layer_i: int, from_sel: list[int], to_sel: list[int]) -> list[list[float]]:
            w = m.coefs_[layer_i]
            return [[round(float(w[f, t]), 4) for t in to_sel] for f in from_sel]

        _weight_mats = [
            _w_sub(li, _disp_indices[li], _disp_indices[li + 1])
            for li in range(len(_disp_indices) - 1)
        ]

        def _trim(acts: list[list[float]]) -> list[list[float]]:
            return [[round(acts[li][s], 4) for s in sel] for li, sel in enumerate(_disp_indices)]

        nn_viz = {
            "layer_sizes":     _layer_sizes_full,
            "display_indices": _disp_indices,
            "weight_matrices": _weight_mats,
            "activation_fn":   m.activation,
            "input_labels":    [_feat_labels.get(f, f) for f in features],
            "samples": [
                {
                    "label":       f"상승 예측 ({float(y_prob[_hi_idx]) * 100:.1f}%)",
                    "prob":        round(float(y_prob[_hi_idx]), 4),
                    "actual":      int(y_test[_hi_idx]),
                    "activations": _trim(hi_acts),
                },
                {
                    "label":       f"하락 예측 ({float(y_prob[_lo_idx]) * 100:.1f}%)",
                    "prob":        round(float(y_prob[_lo_idx]), 4),
                    "actual":      int(y_test[_lo_idx]),
                    "activations": _trim(lo_acts),
                },
            ],
        }

    return {
        "model_key":        model_key,
        "model_name":       name_map[model_key],
        "accuracy":         round(acc, 4),
        "auc":              round(auc, 4),
        "precision":        round(prec, 4),
        "feature_importance": feat_imp,
        "portfolio":        [round(v, 4) for v in portfolio],
        "buyhold":          [round(v, 4) for v in buyhold],
        "portfolio_return": round((portfolio[-1] - 1) * 100, 2),
        "buyhold_return":   round((buyhold[-1] - 1) * 100, 2),
        "signals":          signals,
        "n_train":          int(split),
        "n_test":           int(len(y_test)),
        "nn_viz":           nn_viz,
        "candles":          candle_rows,
        "predicted_next_close": round(predicted_next_close, 2),
        "predicted_next_date": next_date.strftime("%Y-%m-%d"),
        "predicted_move_pct": round(predicted_move_pct, 2),
        "last_close": round(last_close, 2),
        "regression_metrics": {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2": round(r2, 4),
        },
        "dataset_summary": {
            "start_date": feature_rows["date"].iloc[0].strftime("%Y-%m-%d"),
            "end_date": feature_rows["date"].iloc[-1].strftime("%Y-%m-%d"),
            "rows": int(len(feature_rows)),
            "train_rows": int(split),
            "test_rows": int(len(y_test)),
        },
        "method_summary": {
            "classification": method_info["classification"],
            "regression": method_info["regression"],
            "reason": method_info["reason"],
            "top_features": top_features,
        },
        "prediction_summary": {
            "signal": "상승 우세" if predicted_move_pct >= 0 else "하락 우세",
            "basis": (
                f"최근 OHLCV {len(feature_rows)}행을 사용했고, 중요 특성은 "
                f"{', '.join(top_features) if top_features else '기본 수익률 특성'} 입니다."
            ),
        },
    }


@app.post("/api/chat", tags=["stock"])
async def chat(req: ChatRequest) -> dict[str, str]:
    """Ollama를 통해 분석 결과에 대한 자연어 설명을 생성합니다."""
    ctx = req.context
    feat_imp: dict[str, float] = ctx.get("feature_importance", {})
    sorted_feats = sorted(feat_imp.items(), key=lambda x: -x[1])
    feat_str = ", ".join(
        [f"{_FEAT_NAMES.get(k, k)} {v:.3f}" for k, v in sorted_feats[:3]]
    )

    prompt = (
        "당신은 주식 AI 분석 전문가입니다. 개발자도 이해할 수 있는 쉬운 한국어로 답변하세요.\n\n"
        f"현재 분석 결과:\n"
        f"- 모델: {ctx.get('model_name', '알 수 없음')}\n"
        f"- 정확도: {ctx.get('accuracy', 0)*100:.1f}%\n"
        f"- AUC: {ctx.get('auc', 0):.3f}\n"
        f"- 매수 정밀도: {ctx.get('precision', 0)*100:.1f}%\n"
        f"- 전략 수익률: {ctx.get('portfolio_return', 0):+.1f}%\n"
        f"- 전량 보유 수익률: {ctx.get('buyhold_return', 0):+.1f}%\n"
        f"- 주요 예측 요소: {feat_str or '없음'}\n\n"
        f"사용자 질문: {req.message}\n\n"
        "구체적인 수치를 활용해서 인과관계를 설명하세요. "
        "예: '거래량이 평소의 1.8배일 때 상승 확률이 높았습니다.' "
        "200자 이내로 간결하게 답변하세요."
    )

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            )
            resp.raise_for_status()
            return {"response": resp.json().get("response", "답변을 가져올 수 없습니다.")}
    except Exception:
        return {"response": _fallback_explanation(req.message, ctx)}


@app.post("/api/assistant/route", tags=["stock"])
async def assistant_route(req: AssistantRouteRequest) -> dict[str, str]:
    """자연어 질문을 해석해 가장 알맞은 주식 AI 실습 화면으로 안내합니다."""
    clean = re.sub(r"\s+", " ", req.message).strip()
    if not clean:
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    fallback = _assistant_route_fallback(clean)
    route_info = fallback

    try:
        route_info = await _assistant_route_with_llm(clean, fallback)
        route_info["llm_used"] = "true"
    except Exception:
        route_info["llm_used"] = "false"

    route_info["message"] = clean
    route_info["helper_text"] = (
        f"{route_info['reason']} 그래서 {route_info['route_label']}로 이어서 실습하는 흐름이 가장 잘 맞아요."
    )
    return route_info


_EVENT_THEME_LIBRARY: dict[str, dict[str, Any]] = {
    "war": {
        "label": "전쟁·군사 충돌",
        "keywords": ["전쟁", "군사", "충돌", "폭격", "미사일", "휴전 결렬", "중동", "대만해협", "러시아", "우크라"],
        "prototypes": [
            "중동 전쟁이 확대되며 유가와 환율이 동시에 오르는 시나리오",
            "군사 충돌 장기화로 위험자산 회피 심리가 커지는 뉴스",
            "해운과 공급망이 흔들리고 방산과 에너지 업종이 주목받는 상황",
        ],
        "market_summary": "위험자산을 줄이고 현금, 방어주, 원자재 쪽으로 시선이 이동하기 쉬운 뉴스입니다.",
        "risk_bias": 28,
        "market_temperature": [
            {"label": "KRX 성장주", "score": -2, "summary": "리스크 회피 심리로 할인 압력이 커질 수 있습니다."},
            {"label": "방어주", "score": 1, "summary": "필수소비재·방산 같은 방어 성격 업종으로 자금이 피신할 수 있습니다."},
            {"label": "원자재", "score": 2, "summary": "원유·가스 가격이 민감하게 오를 수 있습니다."},
            {"label": "환율", "score": 2, "summary": "원/달러 환율 상승 압력이 커질 수 있습니다."},
        ],
        "sector_impacts": [
            {"sector": "방산", "score": 2, "summary": "군수 수요 기대가 붙을 수 있습니다.", "examples": ["한화에어로스페이스", "한국항공우주"]},
            {"sector": "정유·에너지", "score": 2, "summary": "공급 차질 우려가 원유 가격을 밀어 올릴 수 있습니다.", "examples": ["S-Oil", "SK이노베이션"]},
            {"sector": "항공·여행", "score": -2, "summary": "유가 상승과 이동 위축 우려가 동시에 생길 수 있습니다.", "examples": ["대한항공", "하나투어"]},
            {"sector": "반도체", "score": -1, "summary": "공급망 불안과 투자심리 둔화가 부담이 될 수 있습니다.", "examples": ["삼성전자", "SK하이닉스"]},
        ],
        "watch_points": ["WTI 유가", "원/달러 환율", "해운 운임", "미국 국채 금리", "VIX"],
        "action_plan": [
            "한 번에 공격적으로 매수하기보다 분할 대응을 우선합니다.",
            "유가와 환율에 민감한 보유 종목 비중이 과한지 먼저 점검합니다.",
            "방산·에너지 강세가 나와도 추격매수보다 눌림 확인이 안전합니다.",
        ],
    },
    "drought": {
        "label": "가뭄·기후 충격",
        "keywords": ["가뭄", "폭염", "엘니뇨", "작황 부진", "기후 위기", "농산물 급등", "물 부족", "산불"],
        "prototypes": [
            "엘니뇨와 가뭄으로 농산물 가격과 전력 수요가 동시에 흔들리는 상황",
            "폭염과 물 부족이 식품 원가와 수처리 관련주에 영향을 주는 뉴스",
            "작황 부진으로 비료와 관개 인프라 수요가 부각되는 시나리오",
        ],
        "market_summary": "농산물 가격, 전력 수요, 물 인프라 이슈가 같이 움직여 업종별 온도차가 크게 벌어질 수 있습니다.",
        "risk_bias": 20,
        "market_temperature": [
            {"label": "식품 원가", "score": 2, "summary": "곡물·농산물 가격 상승이 원가 부담으로 번질 수 있습니다."},
            {"label": "유틸리티", "score": 1, "summary": "전력·물 공급 이슈가 부각될 수 있습니다."},
            {"label": "소비주", "score": -1, "summary": "원가 부담을 가격에 전가하기 어려운 기업은 수익성이 눌릴 수 있습니다."},
            {"label": "농업 솔루션", "score": 2, "summary": "비료·관개·물 관리 설비 관심이 커질 수 있습니다."},
        ],
        "sector_impacts": [
            {"sector": "비료·농업", "score": 2, "summary": "작황 불안이 비료·종자·농업 솔루션 수요를 키울 수 있습니다.", "examples": ["남해화학", "효성오앤비"]},
            {"sector": "수처리·관개", "score": 2, "summary": "물 부족 이슈가 인프라 투자 기대를 키울 수 있습니다.", "examples": ["뉴보텍", "코오롱글로벌"]},
            {"sector": "식품", "score": -1, "summary": "곡물 가격 상승이 마진을 압박할 수 있습니다.", "examples": ["농심", "오리온"]},
            {"sector": "음료·유통", "score": -1, "summary": "원재료와 물류비 부담이 커질 수 있습니다.", "examples": ["롯데칠성", "BGF리테일"]},
        ],
        "watch_points": ["국제 밀·옥수수 가격", "전력 수요 피크", "강수량 전망", "식품 물가", "댐 저수율"],
        "action_plan": [
            "식품주는 원가 전가력이 있는 브랜드 중심으로 선별합니다.",
            "비료·수처리 테마는 단기 급등이 잦아 거래량과 눌림을 함께 확인합니다.",
            "기후 뉴스는 하루 반짝 이슈인지 계절성 추세인지 구분해야 합니다.",
        ],
    },
    "inflation": {
        "label": "물가 급등·인플레이션",
        "keywords": ["cpi", "물가", "인플레이션", "소비자물가", "생산자물가", "원자재 급등"],
        "prototypes": [
            "미국 CPI가 예상보다 높아 성장주 밸류에이션이 눌리는 뉴스",
            "물가 상승으로 금리 경로가 위쪽으로 열리는 인플레이션 충격",
            "원자재 가격 급등이 소비와 플랫폼 주식에 부담을 주는 상황",
        ],
        "market_summary": "금리 경로가 위쪽으로 열릴 수 있어 성장주와 고평가주는 할인 압력을 받을 수 있습니다.",
        "risk_bias": 18,
        "market_temperature": [
            {"label": "성장주", "score": -2, "summary": "할인율 부담으로 밸류에이션이 눌릴 수 있습니다."},
            {"label": "은행·보험", "score": 1, "summary": "금리 레벨 상승 기대가 상대적으로 유리할 수 있습니다."},
            {"label": "소비", "score": -1, "summary": "실질 소비 둔화 우려가 붙을 수 있습니다."},
            {"label": "원자재", "score": 1, "summary": "가격 전가력이 있는 업종은 상대적으로 버틸 수 있습니다."},
        ],
        "sector_impacts": [
            {"sector": "은행", "score": 1, "summary": "금리 상승 구간에서 이자마진 기대가 붙을 수 있습니다.", "examples": ["KB금융", "신한지주"]},
            {"sector": "보험", "score": 1, "summary": "장기금리 상승 기대가 상대적으로 우호적일 수 있습니다.", "examples": ["삼성생명", "한화생명"]},
            {"sector": "플랫폼·성장주", "score": -2, "summary": "고평가 성장주는 할인율 상승에 민감합니다.", "examples": ["NAVER", "카카오"]},
            {"sector": "유통·소비", "score": -1, "summary": "물가 부담이 소비 둔화로 이어질 수 있습니다.", "examples": ["이마트", "롯데쇼핑"]},
        ],
        "watch_points": ["미국 CPI", "한국 CPI", "국채 금리", "원자재 지수", "기대인플레이션"],
        "action_plan": [
            "금리 민감 성장주 비중이 크다면 변동성 확대를 먼저 가정합니다.",
            "숫자 발표 하루보다 발표 뒤 금리 시장 반응을 같이 보는 편이 안전합니다.",
            "원가 전가력이 있는 기업과 없는 기업을 분리해서 봅니다.",
        ],
    },
    "rate_cut": {
        "label": "금리 인하",
        "keywords": ["금리 인하", "rate cut", "완화", "유동성 확대", "fed 인하", "pivot"],
        "prototypes": [
            "연준이 금리 인하를 시사하며 성장주와 리츠 심리가 살아나는 뉴스",
            "유동성 확대 기대가 기술주와 경기민감주에 반등을 주는 상황",
            "금리 부담 완화로 자산주와 2차전지 같은 고변동 섹터가 반응하는 시나리오",
        ],
        "market_summary": "유동성 기대로 성장주와 경기민감주에 숨통이 트일 수 있지만, 경기 둔화형 인하인지도 같이 봐야 합니다.",
        "risk_bias": 8,
        "market_temperature": [
            {"label": "성장주", "score": 2, "summary": "할인율 부담 완화 기대가 붙기 쉽습니다."},
            {"label": "건설·리츠", "score": 1, "summary": "금리 부담이 줄면 자산주 심리가 살아날 수 있습니다."},
            {"label": "은행", "score": -1, "summary": "예대마진 축소 우려가 생길 수 있습니다."},
            {"label": "소비", "score": 1, "summary": "심리 개선이 나타나면 소비주에 숨통이 트일 수 있습니다."},
        ],
        "sector_impacts": [
            {"sector": "인터넷·성장주", "score": 2, "summary": "밸류에이션 재평가 기대가 생길 수 있습니다.", "examples": ["NAVER", "카카오"]},
            {"sector": "건설·리츠", "score": 1, "summary": "금리 부담 완화가 투자심리를 돕습니다.", "examples": ["현대건설", "SK리츠"]},
            {"sector": "은행", "score": -1, "summary": "순이자마진 기대는 다소 꺾일 수 있습니다.", "examples": ["하나금융지주", "우리금융지주"]},
            {"sector": "2차전지", "score": 1, "summary": "고변동 성장 섹터 심리 반등에 유리할 수 있습니다.", "examples": ["LG에너지솔루션", "에코프로비엠"]},
        ],
        "watch_points": ["연준 점도표", "국채 금리 하락 폭", "환율", "경기선행지수", "신용 스프레드"],
        "action_plan": [
            "금리 인하가 경기 침체 대응인지, 연착륙 자신감인지 해석을 나눠 봅니다.",
            "성장주 반등이 나와도 실적이 약한 종목은 선별이 필요합니다.",
            "리츠·건설은 금리뿐 아니라 분양·임대 지표도 같이 확인합니다.",
        ],
    },
    "tariff": {
        "label": "관세·규제 충격",
        "keywords": ["관세", "규제", "제재", "수출 규제", "반도체 규제", "관세 부과", "보조금 제한", "무역 분쟁"],
        "prototypes": [
            "반도체 수출 규제가 강화되며 대형주와 소부장 밸류체인이 흔들리는 뉴스",
            "관세 부과와 무역 분쟁으로 수출주의 실적 가이던스가 낮아지는 상황",
            "국산 대체 공급망과 보안 관련주가 상대적으로 부각되는 시나리오",
        ],
        "market_summary": "공급망과 수출 밸류체인에 직접 충격을 줄 수 있어 업종별 승패가 빠르게 갈릴 수 있습니다.",
        "risk_bias": 22,
        "market_temperature": [
            {"label": "수출주", "score": -2, "summary": "직접 규제 대상 업종은 실적 추정치가 낮아질 수 있습니다."},
            {"label": "국산 대체", "score": 1, "summary": "국산화·내수 대체 수혜 기대가 붙을 수 있습니다."},
            {"label": "반도체", "score": -2, "summary": "수출 제한과 CAPEX 불확실성이 부담입니다."},
            {"label": "방산·보안", "score": 1, "summary": "지정학 규제가 길어질수록 상대 수혜가 붙을 수 있습니다."},
        ],
        "sector_impacts": [
            {"sector": "반도체", "score": -2, "summary": "직접 규제 뉴스는 밸류체인 전반에 부담입니다.", "examples": ["삼성전자", "SK하이닉스"]},
            {"sector": "장비·소부장", "score": -1, "summary": "고객사 CAPEX 지연 우려가 생길 수 있습니다.", "examples": ["원익IPS", "한미반도체"]},
            {"sector": "방산", "score": 1, "summary": "긴장 고조 시 상대적인 수혜 기대가 붙습니다.", "examples": ["한화시스템", "LIG넥스원"]},
            {"sector": "국산화 수혜", "score": 1, "summary": "대체 공급망 기대가 붙을 수 있습니다.", "examples": ["동진쎄미켐", "솔브레인"]},
        ],
        "watch_points": ["규제 대상 품목", "미국·중국 발표문", "수출 통계", "CAPEX 가이던스", "환율"],
        "action_plan": [
            "뉴스 제목보다 실제 규제 범위와 시행 시점을 먼저 확인합니다.",
            "반도체는 대형주뿐 아니라 장비·소부장까지 연쇄 반응을 봐야 합니다.",
            "정책 뉴스는 하루 급락 후 해석 수정이 많아 추격 매도도 조심합니다.",
        ],
    },
}

_HOLDING_ALIAS_MAP = {
    "삼성전자": "반도체",
    "sk하이닉스": "반도체",
    "sk 하이닉스": "반도체",
    "naver": "인터넷·성장주",
    "카카오": "인터넷·성장주",
    "현대차": "자동차",
    "현대자동차": "자동차",
    "대한항공": "항공·여행",
    "하나투어": "항공·여행",
    "한화에어로스페이스": "방산",
    "lignex1": "방산",
    "lig넥스원": "방산",
    "s-oil": "정유·에너지",
    "sk이노베이션": "정유·에너지",
    "농심": "식품",
    "오리온": "식품",
    "kb금융": "은행",
    "신한지주": "은행",
    "삼성생명": "보험",
    "lg에너지솔루션": "2차전지",
    "에코프로비엠": "2차전지",
    "남해화학": "비료·농업",
    "효성오앤비": "비료·농업",
    "뉴보텍": "수처리·관개",
    "반도체": "반도체",
    "방산": "방산",
    "식품": "식품",
    "은행": "은행",
    "보험": "보험",
    "항공": "항공·여행",
    "여행": "항공·여행",
    "에너지": "정유·에너지",
}


def _normalize_news_token(text: str) -> str:
    return re.sub(r"\s+", "", str(text)).strip().lower()


def _theme_document(theme: dict[str, Any]) -> str:
    sector_text = " ".join(
        f"{item['sector']} {item['summary']} {' '.join(item.get('examples', []))}"
        for item in theme.get("sector_impacts", [])
    )
    market_text = " ".join(
        f"{item['label']} {item['summary']}"
        for item in theme.get("market_temperature", [])
    )
    return " ".join([
        theme.get("label", ""),
        " ".join(theme.get("keywords", [])),
        " ".join(theme.get("prototypes", [])),
        theme.get("market_summary", ""),
        sector_text,
        market_text,
        " ".join(theme.get("watch_points", [])),
    ])


@lru_cache(maxsize=1)
def _build_theme_tfidf_index() -> tuple[Any, Any, list[str]]:
    from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415

    keys = list(_EVENT_THEME_LIBRARY.keys())
    docs = [_theme_document(_EVENT_THEME_LIBRARY[key]) for key in keys]
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 5),
        sublinear_tf=True,
        min_df=1,
    )
    matrix = vectorizer.fit_transform(docs)
    return vectorizer, matrix, keys


def _score_themes_by_tfidf(message: str) -> dict[str, float]:
    from sklearn.metrics.pairwise import cosine_similarity  # noqa: PLC0415

    vectorizer, matrix, keys = _build_theme_tfidf_index()
    query = vectorizer.transform([message])
    sims = cosine_similarity(query, matrix)[0]
    return {key: float(score) for key, score in zip(keys, sims)}


@lru_cache(maxsize=1)
def _load_sentence_transformer_model() -> Any:
    from sentence_transformers import SentenceTransformer  # noqa: PLC0415

    return SentenceTransformer(NEWS_THEME_EMBED_MODEL)


@lru_cache(maxsize=1)
def _build_theme_sentence_embedding_index() -> tuple[Any, list[str], Any]:
    model = _load_sentence_transformer_model()
    keys = list(_EVENT_THEME_LIBRARY.keys())
    docs = [_theme_document(_EVENT_THEME_LIBRARY[key]) for key in keys]
    embeddings = model.encode(docs, normalize_embeddings=True)
    return model, keys, embeddings


def _score_themes_by_sentence_embedding(message: str) -> dict[str, float]:
    import numpy as np  # noqa: PLC0415

    model, keys, embeddings = _build_theme_sentence_embedding_index()
    query_embedding = model.encode([message], normalize_embeddings=True)[0]
    scores = np.asarray(embeddings) @ np.asarray(query_embedding)
    return {key: float(score) for key, score in zip(keys, scores.tolist())}


def _resolve_theme_backend(message: str) -> tuple[dict[str, float], str]:
    backend = NEWS_THEME_BACKEND.lower().strip()
    if backend in {"kobert", "finbert", "hf-embedding", "sentence-transformer"}:
        try:
            return _score_themes_by_sentence_embedding(message), f"sentence-transformer:{NEWS_THEME_EMBED_MODEL}"
        except Exception:
            return _score_themes_by_tfidf(message), "tfidf-char-ngram-fallback"
    return _score_themes_by_tfidf(message), "tfidf-char-ngram"


def _match_event_themes(message: str) -> list[dict[str, Any]]:
    lowered = _normalize_news_token(message)
    similarity_scores, backend_used = _resolve_theme_backend(message)
    matches: list[dict[str, Any]] = []
    for key, theme in _EVENT_THEME_LIBRARY.items():
        hit_count = sum(1 for keyword in theme["keywords"] if _normalize_news_token(keyword) in lowered)
        similarity = similarity_scores.get(key, 0.0)
        combined_score = (hit_count * 0.65) + (similarity * 5.0)
        if hit_count or similarity >= 0.17:
            copied = dict(theme)
            copied["key"] = key
            copied["hit_count"] = hit_count
            copied["similarity"] = round(similarity, 4)
            copied["combined_score"] = round(combined_score, 4)
            copied["backend_used"] = backend_used
            matches.append(copied)
    matches.sort(key=lambda item: (item["combined_score"], item["hit_count"], item["similarity"]), reverse=True)
    return matches[:2]


def _merge_market_temperature(themes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for theme in themes:
        for item in theme.get("market_temperature", []):
            label = item["label"]
            slot = merged.setdefault(label, {"label": label, "score": 0, "summary_parts": []})
            slot["score"] += int(item["score"])
            slot["summary_parts"].append(item["summary"])
    if not merged:
        return [
            {"label": "시장 전체", "score": 0, "summary": "입력한 뉴스는 단일 업종보다 해석이 넓어 추가 확인이 필요합니다."},
        ]
    results = []
    for item in merged.values():
        score = max(min(item["score"], 2), -2)
        results.append({
            "label": item["label"],
            "score": score,
            "summary": " ".join(dict.fromkeys(item["summary_parts"])),
        })
    results.sort(key=lambda item: abs(item["score"]), reverse=True)
    return results[:4]


def _merge_sector_impacts(themes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for theme in themes:
        for item in theme.get("sector_impacts", []):
            sector = item["sector"]
            slot = merged.setdefault(sector, {"sector": sector, "score": 0, "summary_parts": [], "examples": []})
            slot["score"] += int(item["score"])
            slot["summary_parts"].append(item["summary"])
            slot["examples"].extend(item.get("examples", []))
    results = []
    for item in merged.values():
        score = max(min(item["score"], 2), -2)
        direction = "positive" if score > 0 else "negative" if score < 0 else "mixed"
        results.append({
            "sector": item["sector"],
            "score": score,
            "direction": direction,
            "summary": " ".join(dict.fromkeys(item["summary_parts"])),
            "examples": list(dict.fromkeys(item["examples"]))[:3],
        })
    results.sort(key=lambda item: abs(item["score"]), reverse=True)
    return results[:8]


def _build_base_consultant_note(summary: str, themes: list[dict[str, Any]], sector_impacts: list[dict[str, Any]], horizon_text: str) -> str:
    top_sector = sector_impacts[0]["sector"] if sector_impacts else "주요 업종"
    if themes:
        theme_names = ", ".join(theme["label"] for theme in themes)
        return f"{theme_names} 뉴스로 해석됩니다. {summary} {horizon_text} 동안은 특히 {top_sector} 흐름과 환율·원자재 반응을 같이 보며 대응하는 보수적 접근이 유리합니다."
    return f"입력 뉴스는 여러 해석이 가능해 단정하기 어렵습니다. {horizon_text} 동안은 headline보다 실제 수치 발표와 업종별 가격 반응을 먼저 확인하는 접근이 좋습니다."


async def _refine_consultant_note_with_llm(message: str, payload: dict[str, Any], fallback_note: str) -> tuple[str, bool]:
    prompt = (
        "당신은 뉴스 이벤트를 읽고 주식 투자자에게 짧은 자문을 주는 한국어 컨설턴트입니다.\n"
        "아래 구조화된 판단을 바탕으로 180자 안쪽의 간결한 투자 코멘트를 작성하세요.\n"
        "과장하지 말고, 섹터/환율/원자재/체크포인트를 2~3개만 짚으세요.\n\n"
        f"뉴스 입력: {message}\n"
        f"감지 테마: {', '.join(payload.get('detected_themes', []))}\n"
        f"시장 요약: {payload.get('summary', '')}\n"
        f"주요 업종: {json.dumps(payload.get('sector_impacts', [])[:3], ensure_ascii=False)}\n"
        f"체크포인트: {json.dumps(payload.get('watch_points', [])[:4], ensure_ascii=False)}\n"
        "답변은 평문 한 단락으로만 작성하세요."
    )
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            )
            resp.raise_for_status()
            text = resp.json().get("response", "").strip()
            return text or fallback_note, True
    except Exception:
        return fallback_note, False


def _build_holding_notes(holdings: list[str], sector_impacts: list[dict[str, Any]]) -> list[dict[str, str]]:
    if not holdings:
        return []

    sector_map = {item["sector"]: item for item in sector_impacts}
    notes: list[dict[str, str]] = []
    for raw in holdings:
        token = raw.strip()
        if not token:
            continue
        normalized = _normalize_news_token(token)
        sector = _HOLDING_ALIAS_MAP.get(normalized, token)
        impact = sector_map.get(sector)
        if impact:
            stance = "우호적" if impact["score"] > 0 else "부담" if impact["score"] < 0 else "중립"
            notes.append({
                "target": token,
                "sector": sector,
                "stance": stance,
                "summary": f"{sector} 관점에서는 현재 뉴스가 {stance} 쪽입니다. {impact['summary']}",
            })
        else:
            notes.append({
                "target": token,
                "sector": sector if sector != token else "직접 판별 필요",
                "stance": "직접 확인",
                "summary": "등록된 대표 섹터 매핑이 없어, 최근 가격 반응과 실적 민감도를 직접 함께 확인하는 편이 좋습니다.",
            })
    return notes[:8]


def _generic_news_summary(message: str) -> str:
    if any(word in message for word in ["호재", "수주", "실적 개선", "협력", "승인"]):
        return "개별 호재 뉴스 성격이 있어 특정 업종보다 관련 기업 한두 곳에 영향이 집중될 가능성이 큽니다."
    if any(word in message for word in ["악재", "적자", "하향", "리스크", "불확실"]):
        return "악재 뉴스 성격이 있어 headline보다 실제 실적 영향 범위와 기간을 먼저 확인하는 편이 좋습니다."
    return "입력한 뉴스는 해석 범위가 넓어 headline만으로 결론 내리기보다 관련 수치와 시장 반응을 함께 보는 편이 좋습니다."


@app.post("/api/stock/news-consult", tags=["stock"])
async def stock_news_consult(req: NewsConsultRequest) -> dict[str, Any]:
    """전쟁·가뭄·규제·물가 같은 이벤트/뉴스를 투자 관점으로 해석합니다."""
    message = re.sub(r"\s+", " ", req.message).strip()
    if len(message) < 6:
        raise HTTPException(status_code=400, detail="뉴스나 사건 설명을 조금 더 자세히 입력해주세요.")

    themes = _match_event_themes(message)
    sector_impacts = _merge_sector_impacts(themes)
    market_temperature = _merge_market_temperature(themes)

    horizon_map = {
        "1w": "1주 안팎",
        "1m": "1개월 안팎",
        "3m": "1~3개월",
        "6m": "3~6개월",
    }
    risk_text_map = {
        "conservative": "보수형",
        "neutral": "중립형",
        "aggressive": "공격형",
    }

    summary = " ".join(theme["market_summary"] for theme in themes) if themes else _generic_news_summary(message)
    risk_score = min(95, 25 + sum(theme.get("risk_bias", 0) for theme in themes))
    if req.risk_profile == "conservative":
        risk_score = min(100, risk_score + 8)
    elif req.risk_profile == "aggressive":
        risk_score = max(0, risk_score - 6)

    risk_level = "높음" if risk_score >= 70 else "보통" if risk_score >= 45 else "낮음"
    horizon_text = horizon_map.get(req.horizon, "1개월 안팎")
    action_plan = list(dict.fromkeys(action for theme in themes for action in theme.get("action_plan", [])))[:5]
    if not action_plan:
        action_plan = [
            "뉴스 제목만 따라가기보다 실제 수치 발표와 업종 반응을 확인합니다.",
            "관심 종목이 왜 움직였는지 가격·거래량·환율을 함께 봅니다.",
            "하루 급등락에는 추격보다 분할 대응이 안전합니다.",
        ]
    watch_points = list(dict.fromkeys(point for theme in themes for point in theme.get("watch_points", [])))[:6]
    if not watch_points:
        watch_points = ["거래량 변화", "환율", "국채 금리", "실적 가이던스"]

    payload = {
        "detected_themes": [theme["label"] for theme in themes],
        "theme_backend": themes[0].get("backend_used", "tfidf-char-ngram") if themes else "tfidf-char-ngram",
        "theme_scores": [
            {
                "label": theme["label"],
                "similarity": theme.get("similarity", 0.0),
                "keyword_hits": theme.get("hit_count", 0),
                "combined_score": theme.get("combined_score", 0.0),
            }
            for theme in themes
        ],
        "summary": summary,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "market_scope": req.market_scope,
        "horizon": req.horizon,
        "horizon_text": horizon_text,
        "risk_profile": risk_text_map.get(req.risk_profile, "중립형"),
        "market_temperature": market_temperature,
        "sector_impacts": sector_impacts,
        "watch_points": watch_points,
    }

    fallback_note = _build_base_consultant_note(summary, themes, sector_impacts, horizon_text)
    consultant_note, llm_used = await _refine_consultant_note_with_llm(message, payload, fallback_note)

    holding_notes = _build_holding_notes(req.holdings, sector_impacts)

    return {
        **payload,
        "consultant_note": consultant_note,
        "action_plan": action_plan,
        "holding_notes": holding_notes,
        "llm_used": llm_used,
        "input_message": message,
    }


_TARGET_COMPANIES = ["롯데호텔", "포스코A&C", "현대자동차"]

_FEATURE_COLS = [
    "f1_daily_return", "f2_return_5d", "f3_ma5_ratio", "f4_ma20_ratio",
    "f5_vol_ratio", "f6_rsi", "f7_volatility", "f8_golden_cross",
    "f9_momentum_20d", "f10_vol_change",
]

_FEATURE_LABELS = {
    "f1_daily_return":  "일간 수익률",
    "f2_return_5d":     "5일 수익률",
    "f3_ma5_ratio":     "MA5 비율",
    "f4_ma20_ratio":    "MA20 비율",
    "f5_vol_ratio":     "거래량 비율",
    "f6_rsi":           "RSI (14일)",
    "f7_volatility":    "변동성",
    "f8_golden_cross":  "골든크로스",
    "f9_momentum_20d":  "20일 모멘텀",
    "f10_vol_change":   "거래량 변화율",
}


def _compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values("date").reset_index(drop=True)
    df["close"]  = pd.to_numeric(df["close"],  errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    df["f1_daily_return"] = df["close"].pct_change() * 100
    df["f2_return_5d"]    = df["close"].pct_change(5) * 100

    ma5  = df["close"].rolling(5).mean()
    ma20 = df["close"].rolling(20).mean()
    df["f3_ma5_ratio"]    = df["close"] / ma5 * 100
    df["f4_ma20_ratio"]   = df["close"] / ma20 * 100

    df["f5_vol_ratio"]    = df["volume"] / df["volume"].rolling(10).mean()

    delta = df["close"].diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, np.nan)
    df["f6_rsi"]          = 100 - (100 / (1 + rs))

    df["f7_volatility"]   = df["f1_daily_return"].rolling(20).std()
    df["f8_golden_cross"] = (ma5 > ma20).astype(int)
    df["f9_momentum_20d"] = df["close"].pct_change(20) * 100
    df["f10_vol_change"]  = df["volume"].pct_change() * 100

    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)
    return df.dropna().reset_index(drop=True)


def _train_and_predict(df_feat: pd.DataFrame, model_key: str) -> dict[str, Any]:
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, roc_auc_score
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler

    X = df_feat[_FEATURE_COLS].values
    y = df_feat["target"].values

    split = max(int(len(X) * 0.8), len(X) - 30)
    split = min(split, len(X) - 5)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    scaler   = StandardScaler()
    Xtr_sc   = scaler.fit_transform(X_train)
    Xte_sc   = scaler.transform(X_test)
    # 최신 데이터(마지막 행)를 추론용으로 변환
    X_latest = scaler.transform(X[[-1]])

    model_map = {
        "logistic": LogisticRegression(random_state=42, max_iter=500),
        "rf":       RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "nn":       MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42),
        "gbm":      GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42),
    }
    model_key = model_key if model_key in model_map else "rf"
    m = model_map[model_key]
    m.fit(Xtr_sc, y_train)

    y_pred = m.predict(Xte_sc)
    y_prob = m.predict_proba(Xte_sc)[:, 1]
    try:
        auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        auc = 0.5
    acc = float(accuracy_score(y_test, y_pred))

    # 특성 중요도
    feat_imp: dict[str, float] = {}
    if hasattr(m, "feature_importances_"):
        for f, v in zip(_FEATURE_COLS, m.feature_importances_):
            feat_imp[f] = round(float(v), 4)
    elif hasattr(m, "coef_"):
        raw   = np.abs(m.coef_[0])
        total = raw.sum() or 1.0
        for f, v in zip(_FEATURE_COLS, raw / total):
            feat_imp[f] = round(float(v), 4)

    # 2026-10-01 추론: 최신 행의 특성으로 예측
    pred_prob   = float(m.predict_proba(X_latest)[0, 1])
    pred_label  = "상승" if pred_prob >= 0.5 else "하락"

    # 최근 가격 정보
    last_row    = df_feat.iloc[-1]

    return {
        "accuracy":          round(acc, 4),
        "auc":               round(auc, 4),
        "n_train":           int(split),
        "n_test":            int(len(y_test)),
        "pred_prob":         round(pred_prob * 100, 1),
        "pred_label":        pred_label,
        "last_date":         str(last_row["date"]),
        "last_close":        float(last_row["close"]),
        "feature_importance": feat_imp,
        "latest_features":   {f: round(float(last_row[f]), 3) for f in _FEATURE_COLS},
    }


def _generate_sample_csv() -> str:
    rng = np.random.default_rng(2024)

    companies = [
        ("롯데호텔",   13000, 300,  900_000,  200_000),
        ("포스코A&C",  18000, 400,  250_000,   80_000),
        ("현대자동차", 230000, 4000, 1_200_000, 300_000),
    ]

    rows = []
    # 500거래일 생성 (2024-01-02 ~ 약 2025-12-말)
    dates: list[pd.Timestamp] = []
    d = pd.Timestamp("2024-01-02")
    while len(dates) < 500:
        if d.weekday() < 5:
            dates.append(d)
        d += pd.Timedelta(days=1)

    for name, base_price, price_std, base_vol, vol_std in companies:
        price  = float(base_price)
        volume = float(base_vol)
        for dt in dates:
            price  = max(price + rng.normal(0, price_std), base_price * 0.5)
            volume = max(volume + rng.normal(0, vol_std), 10_000)
            rows.append({
                "date":    dt.strftime("%Y-%m-%d"),
                "company": name,
                "close":   round(price, 0),
                "volume":  int(volume),
            })

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["date", "company", "close", "volume"])
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


@app.get("/api/stock/sample-csv", tags=["stock"])
def get_sample_csv() -> StreamingResponse:
    """롯데호텔·포스코A&C·현대자동차 샘플 CSV를 생성해 다운로드합니다."""
    content = _generate_sample_csv()
    return StreamingResponse(
        io.BytesIO(content.encode("utf-8-sig")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=stock_sample.csv"},
    )


@app.post("/api/stock/predict-target", tags=["stock"])
async def predict_target(
    file:  UploadFile = File(...),
    model: str        = Form(default="rf"),
) -> dict[str, Any]:
    """
    CSV를 업로드받아 3개 회사별로 10개 특성을 계산하고
    2026-10-01을 타겟으로 상승/하락 확률을 반환합니다.
    """
    raw = await file.read()
    try:
        df_all = pd.read_csv(io.BytesIO(raw), parse_dates=["date"])
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"CSV 파싱 오류: {exc}") from exc

    required = {"date", "company", "close", "volume"}
    if not required.issubset(df_all.columns):
        raise HTTPException(
            status_code=400,
            detail=f"필수 열이 없습니다. 필요: {required}, 업로드된 열: {set(df_all.columns)}",
        )

    results: dict[str, Any] = {}
    for company in df_all["company"].unique():
        df_c = df_all[df_all["company"] == company].copy()
        if len(df_c) < 40:
            results[company] = {"error": f"데이터 부족 ({len(df_c)}행). 최소 40행 필요."}
            continue
        try:
            df_feat = _compute_features(df_c)
            if len(df_feat) < 20:
                results[company] = {"error": "특성 계산 후 유효 데이터 부족."}
                continue
            results[company] = _train_and_predict(df_feat, model)
        except Exception as exc:
            results[company] = {"error": str(exc)}

    model_names = {
        "logistic": "로지스틱 회귀", "rf": "랜덤 포레스트",
        "nn": "신경망", "gbm": "그래디언트 부스팅",
    }
    return {
        "model_key":    model,
        "model_name":   model_names.get(model, model),
        "target_date":  "2026-10-01",
        "feature_labels": _FEATURE_LABELS,
        "companies":    results,
    }


@app.get("/api/ollama/status", tags=["stock"])
async def ollama_status() -> dict[str, Any]:
    """Ollama 서버 연결 상태를 반환합니다."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                return {"status": "online", "models": models}
    except Exception:
        pass
    return {"status": "offline", "models": []}


# ---------------------------------------------------------------------------
# API 라우터 — 롯데호텔 주가 예측 (가상 데이터셋)
# ---------------------------------------------------------------------------

_HOTEL_N = 30
_HOTEL_COLS = [f"hotel_{i:02d}_occ" for i in range(1, _HOTEL_N + 1)]
_HOTEL_PRICE_COLS = [
    "prev_month_close", "prev_3m_return", "prev_6m_return",
    "prev_12m_return", "price_ma3", "price_ma6", "volatility_6m",
]
_HOTEL_FEATURE_COLS = (
    _HOTEL_COLS
    + ["month", "quarter", "season", "is_peak_season"]
    + _HOTEL_PRICE_COLS
)


class HotelStockTrainRequest(BaseModel):
    model: str = "rf"        # ML: logistic|dt|rf|gbm|svm|knn  DL: mlp_1|mlp_2|mlp_3|mlp_deep
    n_samples: int = 1000
    test_size: float = 0.3
    seed: int = 42


def _generate_hotel_dataset(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    dates = pd.date_range("2015-01", periods=n, freq="MS")
    months = dates.month.values.astype(int)
    quarters = ((months - 1) // 3 + 1).astype(int)
    seasons = np.where(
        np.isin(months, [12, 1, 2]), 0,
        np.where(np.isin(months, [3, 4, 5]), 1,
                 np.where(np.isin(months, [6, 7, 8]), 2, 3)),
    )
    is_peak = np.isin(months, [7, 8, 12, 1]).astype(int)
    season_boost = np.array([0.88, 1.00, 1.18, 0.97])[seasons]

    hotel_data: dict[str, np.ndarray] = {}
    for col in _HOTEL_COLS:
        base_occ = rng.uniform(62, 82)
        trend = np.linspace(0, rng.uniform(1, 6), n)
        noise = rng.normal(0, 4, size=n)
        hotel_data[col] = np.clip(base_occ * season_boost + trend + noise, 20.0, 99.0)

    mean_occ = np.mean(list(hotel_data.values()), axis=0)

    close = np.zeros(n)
    close[0] = 10_000.0
    for i in range(1, n):
        occ_effect = (mean_occ[i] - 72.0) * 18.0
        season_bonus = np.array([100.0, -30.0, 250.0, 80.0])[seasons[i]]
        macro_drift = rng.normal(10.0, 220.0)
        close[i] = max(close[i - 1] + occ_effect + season_bonus + macro_drift, 2_000.0)

    df = pd.DataFrame(hotel_data)
    df["month"] = months
    df["quarter"] = quarters
    df["season"] = seasons
    df["is_peak_season"] = is_peak
    df["close"] = close
    df["date"] = dates.strftime("%Y-%m")

    df["prev_month_close"] = df["close"].shift(1)
    df["prev_3m_return"] = df["close"].pct_change(3) * 100.0
    df["prev_6m_return"] = df["close"].pct_change(6) * 100.0
    df["prev_12m_return"] = df["close"].pct_change(12) * 100.0
    df["price_ma3"] = df["close"].rolling(3).mean()
    df["price_ma6"] = df["close"].rolling(6).mean()
    df["volatility_6m"] = df["close"].pct_change().rolling(6).std() * 100.0
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)

    return df.dropna().reset_index(drop=True)


@app.post("/api/hotel-stock/train", tags=["hotel-stock"])
def hotel_stock_train(req: HotelStockTrainRequest) -> dict[str, Any]:
    """롯데호텔 가상 주가 데이터셋에서 선택한 ML/DL 모델을 학습하고 평가 결과를 반환합니다."""
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier  # noqa: PLC0415
    from sklearn.linear_model import LogisticRegression  # noqa: PLC0415
    from sklearn.metrics import (  # noqa: PLC0415
        accuracy_score,
        confusion_matrix,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.neighbors import KNeighborsClassifier  # noqa: PLC0415
    from sklearn.neural_network import MLPClassifier  # noqa: PLC0415
    from sklearn.preprocessing import StandardScaler  # noqa: PLC0415
    from sklearn.svm import SVC  # noqa: PLC0415
    from sklearn.tree import DecisionTreeClassifier  # noqa: PLC0415

    n = max(200, min(req.n_samples, 2000))
    df = _generate_hotel_dataset(n=n, seed=req.seed)

    X = df[_HOTEL_FEATURE_COLS].values
    y = df["target"].values

    test_size = max(0.1, min(req.test_size, 0.5))
    split = int(len(X) * (1.0 - test_size))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_te_sc = scaler.transform(X_test)

    _ML_MODELS: dict[str, Any] = {
        "logistic": LogisticRegression(random_state=42, max_iter=500),
        "dt":       DecisionTreeClassifier(max_depth=6, random_state=42),
        "rf":       RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "gbm":      GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42),
        "svm":      SVC(kernel="rbf", C=2.0, probability=True, random_state=42),
        "knn":      KNeighborsClassifier(n_neighbors=7),
    }
    _DL_MODELS: dict[str, Any] = {
        "mlp_1":    MLPClassifier(hidden_layer_sizes=(64,),          max_iter=500, random_state=42),
        "mlp_2":    MLPClassifier(hidden_layer_sizes=(128, 64),      max_iter=500, random_state=42),
        "mlp_3":    MLPClassifier(hidden_layer_sizes=(256, 128, 64), max_iter=500, random_state=42),
        "mlp_deep": MLPClassifier(hidden_layer_sizes=(512, 256, 128, 64), max_iter=700,
                                  learning_rate="adaptive", random_state=42),
    }
    _MODEL_NAMES: dict[str, str] = {
        "logistic": "로지스틱 회귀",
        "dt":       "결정 트리",
        "rf":       "랜덤 포레스트",
        "gbm":      "그래디언트 부스팅",
        "svm":      "서포트 벡터 머신",
        "knn":      "K-최근접 이웃",
        "mlp_1":    "단층 신경망 (64)",
        "mlp_2":    "2층 신경망 (128→64)",
        "mlp_3":    "3층 신경망 (256→128→64)",
        "mlp_deep": "심층 신경망 (512→256→128→64)",
    }

    all_models = {**_ML_MODELS, **_DL_MODELS}
    model_key = req.model if req.model in all_models else "rf"
    model_type = "DL" if model_key in _DL_MODELS else "ML"
    m = all_models[model_key]
    m.fit(X_tr_sc, y_train)

    y_pred = m.predict(X_te_sc)
    y_prob = m.predict_proba(X_te_sc)[:, 1]

    acc  = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec  = float(recall_score(y_test, y_pred, zero_division=0))
    try:
        auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        auc = 0.5

    cm = confusion_matrix(y_test, y_pred).tolist()

    # 특성 중요도
    feat_imp: dict[str, float] = {}
    if hasattr(m, "feature_importances_"):
        for f, v in zip(_HOTEL_FEATURE_COLS, m.feature_importances_):
            feat_imp[f] = round(float(v), 4)
    elif hasattr(m, "coef_"):
        raw = np.abs(m.coef_[0])
        total = raw.sum() or 1.0
        for f, v in zip(_HOTEL_FEATURE_COLS, raw / total):
            feat_imp[f] = round(float(v), 4)
    else:
        # 순열 중요도 근사 (모든 특성에 대해 열 셔플 후 정확도 감소량 측정)
        rng2 = np.random.default_rng(0)
        base_acc = acc
        for idx, f in enumerate(_HOTEL_FEATURE_COLS):
            Xp = X_te_sc.copy()
            rng2.shuffle(Xp[:, idx])
            drop = base_acc - float(accuracy_score(y_test, m.predict(Xp)))
            feat_imp[f] = round(max(drop, 0.0), 4)

    # 월별 예측 결과 (최대 30개)
    signals = []
    dates_list = df["date"].tolist()
    closes_list = df["close"].tolist()
    for i in range(min(len(y_pred), 30)):
        row_idx = split + i
        signals.append({
            "date":    dates_list[row_idx],
            "close":   round(closes_list[row_idx], 0),
            "prob":    round(float(y_prob[i]) * 100, 1),
            "signal":  "상승" if y_prob[i] >= 0.5 else "하락",
            "actual":  "상승" if y_test[i] == 1 else "하락",
            "correct": bool(y_pred[i] == y_test[i]),
        })

    # 월별 주가 (시각화용)
    price_series = [
        {"date": d, "close": round(c, 0)}
        for d, c in zip(df["date"].tolist(), df["close"].tolist())
    ]

    # ── DL 신경망 시각화 데이터 ───────────────────────────────────────
    nn_viz: dict[str, Any] | None = None
    if model_type == "DL":
        _hidden_sizes = (
            list(m.hidden_layer_sizes)
            if isinstance(m.hidden_layer_sizes, (list, tuple))
            else [int(m.hidden_layer_sizes)]
        )
        _layer_sizes_full = (
            [int(len(_HOTEL_FEATURE_COLS))]
            + [int(h) for h in _hidden_sizes]
            + [1]
        )

        _MAX_DISP = 8  # neurons to display per hidden layer

        def _mlp_forward(x_row: np.ndarray) -> list[list[float]]:
            """Run a manual forward pass and return per-layer activations."""
            x = x_row.reshape(1, -1).copy()
            acts: list[list[float]] = [x[0].tolist()]
            fn = m.activation
            for w, b in zip(m.coefs_[:-1], m.intercepts_[:-1]):
                x = x @ w + b
                if fn == "relu":
                    np.maximum(x, 0, out=x)
                elif fn == "tanh":
                    np.tanh(x, out=x)
                else:
                    x = 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
                acts.append(x[0].tolist())
            # output layer always uses logistic for binary classification
            x = x @ m.coefs_[-1] + m.intercepts_[-1]
            x = 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
            acts.append(x[0].tolist())
            return acts

        _hi_idx = int(np.argmax(y_prob))
        _lo_idx = int(np.argmin(y_prob))
        hi_acts = _mlp_forward(X_te_sc[_hi_idx])
        lo_acts = _mlp_forward(X_te_sc[_lo_idx])

        def _top_k_by_abs(vals: list[float], k: int) -> list[int]:
            idxs = sorted(range(len(vals)), key=lambda i: abs(vals[i]), reverse=True)
            return sorted(idxs[:k])

        # Input layer: use top features by importance
        _feat_order = sorted(
            range(len(_HOTEL_FEATURE_COLS)),
            key=lambda i: feat_imp.get(_HOTEL_FEATURE_COLS[i], 0.0),
            reverse=True,
        )
        _disp_input = sorted(_feat_order[:_MAX_DISP])

        # Hidden layers: union of top-k from high and low samples
        _n_hidden = len(_hidden_sizes)
        _disp_hidden: list[list[int]] = []
        for li in range(1, _n_hidden + 1):
            k = min(_MAX_DISP, len(hi_acts[li]))
            hi_top = set(_top_k_by_abs(hi_acts[li], k))
            lo_top = set(_top_k_by_abs(lo_acts[li], k))
            combined = sorted(hi_top | lo_top)[:k]
            _disp_hidden.append(combined)

        _disp_indices = [_disp_input] + _disp_hidden + [[0]]

        def _weight_sub(layer_i: int, from_sel: list[int], to_sel: list[int]) -> list[list[float]]:
            w = m.coefs_[layer_i]
            return [[round(float(w[f, t]), 4) for t in to_sel] for f in from_sel]

        _weight_mats = [
            _weight_sub(li, _disp_indices[li], _disp_indices[li + 1])
            for li in range(len(_disp_indices) - 1)
        ]

        _lbl_map = {
            "month": "월", "quarter": "분기", "season": "계절", "is_peak_season": "성수기",
            "prev_month_close": "전월종가", "prev_3m_return": "3M수익",
            "prev_6m_return": "6M수익", "prev_12m_return": "12M수익",
            "price_ma3": "MA3", "price_ma6": "MA6", "volatility_6m": "변동성",
        }

        def _short_lbl(f: str) -> str:
            if f.startswith("hotel_") and f.endswith("_occ"):
                return "H" + f[6:-4]
            return _lbl_map.get(f, f[:8])

        def _trim_acts(acts: list[list[float]]) -> list[list[float]]:
            return [[round(acts[li][s], 4) for s in sel] for li, sel in enumerate(_disp_indices)]

        nn_viz = {
            "layer_sizes":    _layer_sizes_full,
            "display_indices": _disp_indices,
            "weight_matrices": _weight_mats,
            "activation_fn":  m.activation,
            "input_labels":   [_short_lbl(_HOTEL_FEATURE_COLS[i]) for i in _disp_input],
            "samples": [
                {
                    "label":       f"상승 예측 ({float(y_prob[_hi_idx]) * 100:.1f}%)",
                    "prob":        round(float(y_prob[_hi_idx]), 4),
                    "actual":      int(y_test[_hi_idx]),
                    "activations": _trim_acts(hi_acts),
                },
                {
                    "label":       f"하락 예측 ({float(y_prob[_lo_idx]) * 100:.1f}%)",
                    "prob":        round(float(y_prob[_lo_idx]), 4),
                    "actual":      int(y_test[_lo_idx]),
                    "activations": _trim_acts(lo_acts),
                },
            ],
        }

    return {
        "model_key":          model_key,
        "model_name":         _MODEL_NAMES[model_key],
        "model_type":         model_type,
        "n_samples":          int(len(df)),
        "n_features":         int(len(_HOTEL_FEATURE_COLS)),
        "n_train":            int(len(X_train)),
        "n_test":             int(len(X_test)),
        "accuracy":           round(acc, 4),
        "auc":                round(auc, 4),
        "precision":          round(prec, 4),
        "recall":             round(rec, 4),
        "confusion_matrix":   cm,
        "feature_importance": feat_imp,
        "signals":            signals,
        "price_series":       price_series,
        "nn_viz":             nn_viz,
    }


@app.get("/api/hotel-stock/dataset-info", tags=["hotel-stock"])
def hotel_stock_dataset_info() -> dict[str, Any]:
    """롯데호텔 가상 데이터셋의 구성 정보를 반환합니다."""
    return {
        "n_hotel_features": _HOTEL_N,
        "n_seasonal_features": 4,
        "n_price_features": len(_HOTEL_PRICE_COLS),
        "n_total_features": len(_HOTEL_FEATURE_COLS),
        "feature_groups": {
            "체인 호텔 예약률": _HOTEL_COLS,
            "계절 특성": ["month", "quarter", "season", "is_peak_season"],
            "주가 파생 특성": _HOTEL_PRICE_COLS,
        },
        "ml_models": {
            "logistic": "로지스틱 회귀",
            "dt":       "결정 트리",
            "rf":       "랜덤 포레스트",
            "gbm":      "그래디언트 부스팅",
            "svm":      "서포트 벡터 머신",
            "knn":      "K-최근접 이웃",
        },
        "dl_models": {
            "mlp_1":    "단층 신경망 (64)",
            "mlp_2":    "2층 신경망 (128→64)",
            "mlp_3":    "3층 신경망 (256→128→64)",
            "mlp_deep": "심층 신경망 (512→256→128→64)",
        },
    }


# ---------------------------------------------------------------------------
# 정적 파일 및 SPA 폴백
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# API 라우터 — 마이너스 통장 주식 투자 의사결정 모듈
# ---------------------------------------------------------------------------

_TRADING_DAYS_PER_YEAR: int = 252    # 연간 거래일 수 (시뮬레이션 상수)
_TRADING_DAYS_PER_MONTH: int = 21    # 월평균 거래일 수 (시뮬레이션 상수)


class LoanInvestRequest(BaseModel):
    principal: float = 20_000_000          # 원금 (원)
    interest_rate_pct: float = 4.5         # 연 대출 금리 (%)
    period_months: int = 12                # 투자 기간 (월)
    expected_return_pct: float = 8.0       # 종목 연간 기대 수익률 (%)
    volatility_pct: float = 20.0           # 연간 변동성 (표준편차, %)
    dividend_yield_pct: float = 0.0        # 연간 배당 수익률 (%)
    transaction_cost_pct: float = 0.4      # 매수+매도 거래 비용 합계 (%)
    tax_rate_pct: float = 22.0             # 수익에 대한 실효 세율 (%)
    stop_loss_pct: float = 15.0            # 심리적 손절선 (%)
    inflation_pct: float = 2.5             # 인플레이션 (%)
    n_simulations: int = 1000              # 몬테카를로 시뮬레이션 횟수


@app.post("/api/loan-invest/analyze", tags=["loan-invest"])
def loan_invest_analyze(req: LoanInvestRequest) -> dict[str, Any]:
    """마이너스 통장 자금으로 주식 투자할 때의 손익 분석.

    몬테카를로 시뮬레이션, Sharpe 비율, 규칙 기반 의사결정 트리를 사용합니다.
    """
    if req.tax_rate_pct >= 100:
        raise HTTPException(status_code=422, detail="tax_rate_pct는 100 미만이어야 합니다.")

    rng = np.random.default_rng(42)

    period_ratio = req.period_months / 12.0

    # --- 1. 비용 및 손익분기 계산 ---
    loan_cost_pct = req.interest_rate_pct * period_ratio
    dividend_income_pct = req.dividend_yield_pct * period_ratio
    # 세전 손익분기 수익률
    breakeven_pretax = loan_cost_pct + req.transaction_cost_pct - dividend_income_pct
    # 세후 손익분기 (수익에 세금이 붙으므로 더 높게 벌어야 함)
    tax_factor = 1 - req.tax_rate_pct / 100
    breakeven_aftertax = breakeven_pretax / tax_factor

    # --- 2. 실질 기대 수익률 (인플레이션 반영) ---
    expected_real_return_pct = req.expected_return_pct - req.inflation_pct

    # --- 3. Sharpe 비율 (대출 금리를 무위험 수익률로 사용) ---
    excess_return = req.expected_return_pct - req.interest_rate_pct
    sharpe = excess_return / req.volatility_pct if req.volatility_pct > 0 else 0.0
    sharpe = round(sharpe, 3)

    # --- 4. 몬테카를로 시뮬레이션 ---
    daily_mu = req.expected_return_pct / 100 / _TRADING_DAYS_PER_YEAR
    daily_sigma = req.volatility_pct / 100 / (_TRADING_DAYS_PER_YEAR ** 0.5)
    trading_days = max(1, round(req.period_months * _TRADING_DAYS_PER_MONTH))

    # 각 시뮬레이션의 최종 수익률 (%)
    daily_returns = rng.normal(daily_mu, daily_sigma, size=(req.n_simulations, trading_days))
    # 경로의 최저점(최대낙폭) 확인 — 심리적 손절 적용
    cumulative = np.cumprod(1 + daily_returns, axis=1)
    path_min = np.min(cumulative, axis=1)  # 각 경로의 최저 누적 가격 비율
    final_return_pct = (cumulative[:, -1] - 1) * 100  # 세전 수익률 (%)

    # 심리적 손절 발생 시: 투자자가 손절선(-stop_loss_pct)에 도달한 즉시 매도한다고 가정.
    # 하드 스톱로스 모델이므로 모든 손절 경로의 실현 손실을 -stop_loss_pct로 처리.
    stop_loss_triggered = path_min < (1 - req.stop_loss_pct / 100)
    final_return_pct[stop_loss_triggered] = -req.stop_loss_pct

    # 세후·비용 차감 수익률
    def net_return(gross_pct: np.ndarray) -> np.ndarray:
        profit = np.maximum(gross_pct, 0)
        loss = np.minimum(gross_pct, 0)
        after_tax_profit = profit * (1 - req.tax_rate_pct / 100)
        return after_tax_profit + loss - req.transaction_cost_pct - loan_cost_pct + dividend_income_pct

    net_returns = net_return(final_return_pct)
    profit_prob = float(np.mean(net_returns > 0) * 100)
    expected_net_return = float(np.mean(net_returns))
    median_net_return = float(np.median(net_returns))
    p5_net_return = float(np.percentile(net_returns, 5))
    p95_net_return = float(np.percentile(net_returns, 95))
    stop_loss_rate = float(np.mean(stop_loss_triggered) * 100)

    # 손익 금액 환산
    expected_profit_krw = round(req.principal * expected_net_return / 100)
    p5_krw = round(req.principal * p5_net_return / 100)

    # --- 5. 규칙 기반 의사결정 ---
    warnings: list[str] = []
    recommendation = "투자 유리"

    if req.expected_return_pct < breakeven_aftertax:
        recommendation = "투자 비추천"
        warnings.append(
            f"기대 수익률({req.expected_return_pct:.1f}%)이 세후 손익분기({breakeven_aftertax:.1f}%)보다 낮아 기댓값이 음수입니다."
        )
    if req.volatility_pct > 30 and period_ratio >= 0.5:
        if recommendation == "투자 유리":
            recommendation = "주의"
        warnings.append(
            f"변동성({req.volatility_pct:.0f}%)이 높아 레버리지 투자 중 큰 손실 구간이 생길 수 있습니다."
        )
    if stop_loss_rate > 30:
        if recommendation == "투자 유리":
            recommendation = "주의"
        warnings.append(
            f"시뮬레이션의 {stop_loss_rate:.0f}%에서 심리적 손절({req.stop_loss_pct:.0f}%)이 발생했습니다."
        )
    if sharpe < 0:
        recommendation = "투자 비추천"
        warnings.append(
            f"Sharpe 비율({sharpe:.2f})이 0 미만으로, 위험 대비 초과 수익이 없습니다."
        )
    if profit_prob < 40:
        if recommendation == "투자 유리":
            recommendation = "주의"
        warnings.append(
            f"시뮬레이션 성공 확률({profit_prob:.0f}%)이 40% 미만입니다."
        )

    if not warnings:
        warnings.append("특별한 위험 신호가 없습니다. 단, 시장 상황은 언제나 변합니다.")

    algorithm_explanation = (
        "① 몬테카를로 시뮬레이션: 일별 수익률을 정규분포 N(μ,σ²)로 모델링해 "
        f"{req.n_simulations:,}개의 가격 경로를 생성, 세후·비용 차감 후 이익이 나는 경로 비율로 성공 확률을 추정합니다. "
        "경로 의존성(중간에 크게 떨어지면 회복해도 손절 발생)을 심리적 손절선으로 반영합니다. "
        "② Sharpe 비율: (기대수익률 − 대출금리) / 변동성으로, 단위 위험당 초과 수익이 충분한지 측정합니다. "
        "③ 규칙 기반 의사결정: 손익분기 대비 기대 수익률, 변동성, 손절 발생률, Sharpe를 점검하는 체크리스트로 "
        "최종 판정(투자 유리 / 주의 / 비추천)을 내립니다."
    )

    return {
        "input": req.model_dump(),
        "breakeven": {
            "pretax_pct": round(breakeven_pretax, 2),
            "aftertax_pct": round(breakeven_aftertax, 2),
            "loan_cost_pct": round(loan_cost_pct, 2),
            "dividend_offset_pct": round(dividend_income_pct, 2),
        },
        "expected_real_return_pct": round(expected_real_return_pct, 2),
        "sharpe_ratio": sharpe,
        "simulation": {
            "n": req.n_simulations,
            "profit_probability_pct": round(profit_prob, 1),
            "expected_net_return_pct": round(expected_net_return, 2),
            "median_net_return_pct": round(median_net_return, 2),
            "p5_net_return_pct": round(p5_net_return, 2),
            "p95_net_return_pct": round(p95_net_return, 2),
            "stop_loss_rate_pct": round(stop_loss_rate, 1),
            "expected_profit_krw": expected_profit_krw,
            "worst_case_krw": p5_krw,
        },
        "decision": {
            "recommendation": recommendation,
            "warnings": warnings,
        },
        "algorithm_explanation": algorithm_explanation,
    }


@app.get("/", response_class=FileResponse, include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/lab", response_class=FileResponse, include_in_schema=False)
def lab() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "stock_lab.html")


@app.get("/predict", response_class=FileResponse, include_in_schema=False)
def predict_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "stock_predict.html")


@app.get("/advisor", response_class=FileResponse, include_in_schema=False)
def advisor_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "stock_advisor.html")


@app.get("/dart", response_class=FileResponse, include_in_schema=False)
def dart_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "dart_lab.html")


@app.get("/macro", response_class=FileResponse, include_in_schema=False)
def macro_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "macro_lab.html")


@app.get("/datasets", response_class=FileResponse, include_in_schema=False)
def datasets_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "datasets.html")


@app.get("/hotel-stock", response_class=FileResponse, include_in_schema=False)
def hotel_stock_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "hotel_stock.html")


@app.get("/loan-invest", response_class=FileResponse, include_in_schema=False)
def loan_invest_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "loan_invest.html")


@app.get("/fine-tune", response_class=FileResponse, include_in_schema=False)
def fine_tune_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "fine_tune.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
