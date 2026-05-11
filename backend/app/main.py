"""AI/ML Basic Class FastAPI 백엔드 — 114개 챕터 + 퀀트 ML/DL 학습 문서 API 서버."""
from __future__ import annotations

import io
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 앱 초기화 및 경로 설정
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI/ML Basic Class API",
    version="2.0.0",
    description="114개 챕터 AI/ML 실습 코드를 웹에서 실행·조회하는 API 서버입니다.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR    = Path(__file__).resolve().parents[2]
CHAPTERS_DIR = BASE_DIR / "chapters"
FRONTEND_DIR = BASE_DIR / "frontend"
DOCS_DIR     = BASE_DIR / "docs"

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


def _exec_run(chapter_id: str) -> tuple[dict[str, Any], float, str]:
    chapter_path = CHAPTERS_DIR / chapter_id / "practice.py"
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
    return [_build_summary(d) for d in sorted(CHAPTERS_DIR.glob("chapter*")) if d.is_dir()]


@app.get("/api/chapters/{chapter_id}", response_model=ChapterDetail, tags=["chapters"])
def get_chapter(chapter_id: str) -> ChapterDetail:
    chapter_dir = CHAPTERS_DIR / chapter_id
    if not chapter_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'를 찾을 수 없어요.")
    summary = _build_summary(chapter_dir)
    readme_path = chapter_dir / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    return ChapterDetail(**summary.model_dump(), readme=readme)


@app.get("/api/chapters/{chapter_id}/source", response_model=ChapterSourceResponse, tags=["chapters"])
def chapter_source(chapter_id: str) -> ChapterSourceResponse:
    chapter_path = CHAPTERS_DIR / chapter_id / "practice.py"
    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'의 소스 파일을 찾을 수 없어요.")
    return ChapterSourceResponse(chapter=chapter_id, source=chapter_path.read_text(encoding="utf-8"))


@app.post("/api/chapters/{chapter_id}/run", response_model=ChapterRunResponse, tags=["chapters"])
def run_chapter(chapter_id: str) -> ChapterRunResponse:
    result, elapsed_ms, stdout = _exec_run(chapter_id)
    meta = _parse_practice_meta(CHAPTERS_DIR / chapter_id / "practice.py")
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
# 정적 파일 및 SPA 폴백
# ---------------------------------------------------------------------------

@app.get("/", response_class=FileResponse, include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/lab", response_class=FileResponse, include_in_schema=False)
def lab() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "stock_lab.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
