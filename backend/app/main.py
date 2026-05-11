"""AI/ML Basic Class FastAPI 백엔드 — 문서 연계 실습 + 퀀트 ML/DL 학습 문서 API 서버."""
from __future__ import annotations

import csv
import io
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

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
    close: float
    volume: float


class StockAnalyzeRequest(BaseModel):
    rows: list[StockRow]
    model: str = "rf"   # logistic | rf | nn | gbm


class ChatRequest(BaseModel):
    message: str
    context: dict[str, Any] = {}


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
    "experiment_log": {
        "title": "모델 실험 로그",
        "description": "모델별 파라미터와 정확도/F1을 비교하는 작은 실험 로그입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "실험 로그 시각화",
        "recommended_path": "/datasets?dataset=experiment_log",
    },
    "financial_statements": {
        "title": "재무제표 샘플",
        "description": "매출, 영업이익, 감가상각, CAPEX로 DCF 기초를 연습하는 재무 데이터입니다.",
        "recommended_webapp": "학습 허브",
        "practice_label": "chapter105 재무제표 실습",
        "recommended_path": "/?chapter=chapter105",
    },
    "gender_approval": {
        "title": "승인 예측 샘플",
        "description": "작은 범주형 분류 예시 데이터입니다. 분류 개념과 편향 해석을 가볍게 볼 수 있습니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "분류 예시 미리보기",
        "recommended_path": "/datasets?dataset=gender_approval",
    },
    "personal_info": {
        "title": "개인정보 샘플",
        "description": "이름, 이메일, 전화번호, 점수를 가진 개인정보 예시입니다. 민감정보 취급 주의를 설명하기 위한 데이터입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "민감정보 미리보기",
        "recommended_path": "/datasets?dataset=personal_info",
    },
    "stock_ohlcv": {
        "title": "OHLCV 시계열",
        "description": "주가 OHLC 시계열입니다. 기술적 지표와 시계열 분석 실습에 가장 잘 맞습니다.",
        "recommended_webapp": "주식 AI 실험실",
        "practice_label": "내장 데이터로 바로 분석",
        "recommended_path": "/lab?dataset=stock_ohlcv",
    },
    "stock_universe": {
        "title": "종목 유니버스 특성",
        "description": "모멘텀, 변동성, 밸류에이션으로 종목을 비교하는 정적 특성 데이터입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "유니버스 비교 시각화",
        "recommended_path": "/datasets?dataset=stock_universe",
    },
    "stocks_features": {
        "title": "주식 군집화 특성",
        "description": "연수익률, 변동성, PER 기반으로 종목 군집을 해석하는 데이터입니다.",
        "recommended_webapp": "학습 허브",
        "practice_label": "chapter109 군집 실습",
        "recommended_path": "/?chapter=chapter109",
    },
    "student_performance": {
        "title": "학생 성과 데이터",
        "description": "공부시간, 출석률, 합격 여부를 담은 지도학습 예시 데이터입니다.",
        "recommended_webapp": "데이터셋 허브",
        "practice_label": "지도학습 개념 미리보기",
        "recommended_path": "/datasets?dataset=student_performance",
    },
    "traffic_timeseries": {
        "title": "트래픽 시계열",
        "description": "날짜별 트래픽 변화를 담은 짧은 시계열 데이터입니다. 시계열 입력 맛보기용입니다.",
        "recommended_webapp": "주식 AI 실험실",
        "practice_label": "시계열 적응 분석",
        "recommended_path": "/lab?dataset=traffic_timeseries",
    },
}


def _mask_preview(df: pd.DataFrame, dataset_id: str) -> pd.DataFrame:
    masked = df.copy()
    if dataset_id == "personal_info":
        if "email" in masked.columns:
            masked["email"] = masked["email"].astype(str).str.replace(r"(^.).+(@.*$)", r"\1***\2", regex=True)
        if "phone" in masked.columns:
            masked["phone"] = masked["phone"].astype(str).str.replace(r"(\d{3})-\d{4}-(\d{4})", r"\1-****-\2", regex=True)
    return masked


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
    "ma5": "5일 이동평균",
    "ma20": "20일 이동평균",
    "vol_ratio": "거래량 비율",
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
        detail = _build_dataset_detail(dataset_id)
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
        df = pd.read_csv(DATA_DIR / "stock_ohlcv.csv", parse_dates=["date"])
        close = pd.to_numeric(df["close"], errors="coerce").ffill()
        if len(df) < 40:
            extra_n = 40 - len(df)
            last_date = df["date"].iloc[-1]
            extra_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=extra_n, freq="B")
            last_close = float(close.iloc[-1])
            drift = np.linspace(0.001, 0.012, extra_n)
            extra_close = [last_close * (1 + d) for d in drift]
            extra_df = pd.DataFrame({"date": extra_dates, "close": extra_close})
            df = pd.concat([df[["date", "close"]], extra_df], ignore_index=True)
            close = pd.to_numeric(df["close"], errors="coerce").ffill()
        synthetic_volume = close.pct_change().abs().fillna(0) * 8_000_000 + np.linspace(6_000_000, 9_000_000, len(df))
        rows = [
            {
                "date": d.strftime("%Y-%m-%d"),
                "close": round(float(c), 4),
                "volume": int(v),
            }
            for d, c, v in zip(df["date"], close, synthetic_volume)
        ]
        return {
            "dataset_id": dataset_id,
            "title": _DATASET_META[dataset_id]["title"],
            "note": "원본에 거래량이 없어 변화율 기반의 합성 거래량을 만들고, 학습 최소 길이를 맞추기 위해 뒤쪽 영업일을 보강했습니다.",
            "rows": rows,
        }

    if dataset_id == "traffic_timeseries":
        df = pd.read_csv(DATA_DIR / "traffic_timeseries.csv", parse_dates=["date"])
        traffic = pd.to_numeric(df["traffic"], errors="coerce").ffill()
        if len(df) < 40:
            extra_n = 40 - len(df)
            last_date = df["date"].iloc[-1]
            last_traffic = float(traffic.iloc[-1])
            extra_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=extra_n, freq="D")
            wave = np.sin(np.linspace(0, 3.14, extra_n)) * 8
            trend = np.linspace(1, 12, extra_n)
            extra_traffic = np.clip(last_traffic + trend + wave, 1, None)
            df = pd.concat(
                [df[["date", "traffic"]], pd.DataFrame({"date": extra_dates, "traffic": extra_traffic})],
                ignore_index=True,
            )
            traffic = pd.to_numeric(df["traffic"], errors="coerce").ffill()
        rows = [
            {
                "date": d.strftime("%Y-%m-%d"),
                "close": round(float(t), 4),
                "volume": int(max(t * 100, 1000)),
            }
            for d, t in zip(df["date"], traffic)
        ]
        return {
            "dataset_id": dataset_id,
            "title": _DATASET_META[dataset_id]["title"],
            "note": "트래픽 값을 종가처럼, 트래픽의 100배를 거래량처럼 변환하고 부족한 길이는 뒤쪽 날짜로 보강한 시계열 연습용 데이터입니다.",
            "rows": rows,
        }

    raise HTTPException(
        status_code=400,
        detail=f"'{dataset_id}'는 주식 AI 실험실 형식(date, close, volume)으로 바로 변환할 수 없는 데이터셋입니다.",
    )


# ---------------------------------------------------------------------------
# API 라우터 — 주식 AI 실험실
# ---------------------------------------------------------------------------

@app.post("/api/stock/analyze", tags=["stock"])
def stock_analyze(req: StockAnalyzeRequest) -> dict[str, Any]:
    """주가 데이터를 받아 선택한 ML 모델로 분석하고 평가 결과를 반환합니다."""
    import numpy as np  # noqa: PLC0415
    import pandas as pd  # noqa: PLC0415
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier  # noqa: PLC0415
    from sklearn.linear_model import LogisticRegression  # noqa: PLC0415
    from sklearn.metrics import accuracy_score, precision_score, roc_auc_score  # noqa: PLC0415
    from sklearn.neural_network import MLPClassifier  # noqa: PLC0415
    from sklearn.preprocessing import StandardScaler  # noqa: PLC0415

    if len(req.rows) < 25:
        raise HTTPException(status_code=400, detail="최소 25행 이상 입력해주세요.")

    df = pd.DataFrame([{"date": r.date, "close": r.close, "volume": r.volume} for r in req.rows])
    df["close"]  = pd.to_numeric(df["close"],  errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
    df = df.dropna(subset=["close", "volume"])

    df["ret"]       = df["close"].pct_change()
    df["ret_5"]     = df["close"].pct_change(5)
    df["ma5"]       = df["close"].rolling(5).mean()
    df["ma20"]      = df["close"].rolling(20).mean()
    df["vol_ratio"] = df["volume"] / df["volume"].rolling(10).mean()
    df["target"]    = (df["close"].shift(-1) > df["close"]).astype(int)
    df = df.dropna().reset_index(drop=True)

    if len(df) < 15:
        raise HTTPException(status_code=400, detail="유효 데이터 부족 — 행을 더 추가해주세요.")

    features = ["ret", "ret_5", "ma5", "ma20", "vol_ratio"]
    X = df[features].values
    y = df["target"].values

    split = max(int(len(X) * 0.8), len(X) - 15)
    split = min(split, len(X) - 5)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    if len(X_test) < 2:
        raise HTTPException(status_code=400, detail="테스트 데이터 부족 — 행을 더 추가해주세요.")

    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_te_sc = scaler.transform(X_test)

    model_map = {
        "logistic": LogisticRegression(random_state=42, max_iter=300),
        "rf":       RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42),
        "nn":       MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42),
        "gbm":      GradientBoostingClassifier(n_estimators=50, max_depth=3, random_state=42),
    }
    name_map = {
        "logistic": "로지스틱 회귀",
        "rf":       "랜덤 포레스트",
        "nn":       "신경망",
        "gbm":      "그래디언트 부스팅",
    }
    model_key = req.model if req.model in model_map else "rf"
    m = model_map[model_key]
    m.fit(X_tr_sc, y_train)

    y_pred = m.predict(X_te_sc)
    y_prob = m.predict_proba(X_te_sc)[:, 1]

    acc  = float(accuracy_score(y_test, y_pred))
    try:
        auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        auc = 0.5
    prec = float(precision_score(y_test, y_pred, zero_division=0))

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
    test_rets = df["ret"].values[split: split + len(y_test)]
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
            "date":    str(df["date"].iloc[row_idx]),
            "close":   round(float(df["close"].iloc[row_idx]), 0),
            "signal":  "매수" if y_prob[i] >= 0.55 else "관망",
            "prob":    round(float(y_prob[i]) * 100, 1),
            "actual":  "상승" if y_test[i] == 1 else "하락",
            "correct": bool(y_pred[i] == y_test[i]),
        })

    # ── 신경망 시각화 데이터 (nn 모델 전용) ──────────────────────────
    nn_viz: dict[str, Any] | None = None
    if model_key == "nn":
        _feat_labels = {
            "ret": "당일수익", "ret_5": "5일수익",
            "ma5": "MA5", "ma20": "MA20", "vol_ratio": "거래량비",
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

@app.get("/", response_class=FileResponse, include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/lab", response_class=FileResponse, include_in_schema=False)
def lab() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "stock_lab.html")


@app.get("/predict", response_class=FileResponse, include_in_schema=False)
def predict_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "stock_predict.html")


@app.get("/datasets", response_class=FileResponse, include_in_schema=False)
def datasets_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "datasets.html")


@app.get("/hotel-stock", response_class=FileResponse, include_in_schema=False)
def hotel_stock_page() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "hotel_stock.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
