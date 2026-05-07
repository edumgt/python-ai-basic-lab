"""AI/ML Basic Class FastAPI 백엔드 — 114개 챕터 실습 API 서버."""
from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Any

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

BASE_DIR = Path(__file__).resolve().parents[2]
CHAPTERS_DIR = BASE_DIR / "chapters"
FRONTEND_DIR = BASE_DIR / "frontend"


# ---------------------------------------------------------------------------
# Pydantic 스키마 정의
# ---------------------------------------------------------------------------

class ChapterSummary(BaseModel):
    """챕터 목록 조회 시 반환되는 요약 정보입니다."""
    id: str               # 예: "chapter01"
    title: str            # README.md 첫 줄에서 추출한 제목
    topic: str            # practice.py의 result["topic"] 또는 README의 주제
    lesson_10min: str     # 10분 요약 학습 내용 (없으면 빈 문자열)
    practice_30min: str   # 30분 실습 목표 (없으면 빈 문자열)
    has_run: bool         # practice.py에 run() 함수가 있는지 여부


class ChapterDetail(ChapterSummary):
    """단일 챕터 상세 조회 시 반환됩니다. 요약 정보 + README 전문."""
    readme: str           # README.md 전체 텍스트


class ChapterSourceResponse(BaseModel):
    """소스코드 조회 응답입니다."""
    chapter: str
    source: str


class ChapterRunResponse(BaseModel):
    """챕터 run() 실행 결과 응답입니다."""
    chapter: str
    topic: str
    result: dict[str, Any]
    elapsed_ms: float     # 실행 소요 시간(밀리초)


# ---------------------------------------------------------------------------
# 내부 유틸리티 함수
# ---------------------------------------------------------------------------

def _parse_practice_meta(py_path: Path) -> dict[str, str]:
    """practice.py에서 LESSON_10MIN, PRACTICE_30MIN, topic 상수를 추출해요."""
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
    """챕터 README.md 첫 줄에서 제목을 추출해요."""
    readme = chapter_dir / "README.md"
    if readme.exists():
        first = readme.read_text(encoding="utf-8").splitlines()[0]
        return re.sub(r"^#+\s*", "", first).strip()
    return chapter_dir.name


def _build_summary(chapter_dir: Path) -> ChapterSummary:
    """챕터 폴더를 받아 ChapterSummary 객체를 생성해요."""
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


def _exec_run(chapter_id: str) -> tuple[dict[str, Any], float]:
    """practice.py의 run() 함수를 실행하고 결과와 소요 시간을 반환해요."""
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
    t0 = time.perf_counter()
    try:
        result = namespace["run"]()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"run() 실행 오류: {exc}") from exc
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
    return result, elapsed_ms


# ---------------------------------------------------------------------------
# API 라우터
# ---------------------------------------------------------------------------

@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    """서버 상태를 확인하는 헬스체크 엔드포인트입니다."""
    return {"status": "ok", "version": "2.0.0"}


@app.get("/api/chapters", response_model=list[ChapterSummary], tags=["chapters"])
def list_chapters() -> list[ChapterSummary]:
    """모든 챕터의 요약 정보 목록을 반환합니다."""
    return [_build_summary(d) for d in sorted(CHAPTERS_DIR.glob("chapter*")) if d.is_dir()]


@app.get("/api/chapters/{chapter_id}", response_model=ChapterDetail, tags=["chapters"])
def get_chapter(chapter_id: str) -> ChapterDetail:
    """단일 챕터의 상세 정보(메타데이터 + README 전문)를 반환합니다."""
    chapter_dir = CHAPTERS_DIR / chapter_id
    if not chapter_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'를 찾을 수 없어요.")
    summary = _build_summary(chapter_dir)
    readme_path = chapter_dir / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    return ChapterDetail(**summary.model_dump(), readme=readme)


@app.get("/api/chapters/{chapter_id}/source", response_model=ChapterSourceResponse, tags=["chapters"])
def chapter_source(chapter_id: str) -> ChapterSourceResponse:
    """챕터 practice.py 소스코드 전문을 반환합니다."""
    chapter_path = CHAPTERS_DIR / chapter_id / "practice.py"
    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail=f"챕터 '{chapter_id}'의 소스 파일을 찾을 수 없어요.")
    return ChapterSourceResponse(
        chapter=chapter_id,
        source=chapter_path.read_text(encoding="utf-8"),
    )


@app.post("/api/chapters/{chapter_id}/run", response_model=ChapterRunResponse, tags=["chapters"])
def run_chapter(chapter_id: str) -> ChapterRunResponse:
    """챕터 practice.py의 run() 함수를 실행하고 결과를 반환합니다."""
    result, elapsed_ms = _exec_run(chapter_id)
    meta = _parse_practice_meta(CHAPTERS_DIR / chapter_id / "practice.py")
    return ChapterRunResponse(
        chapter=chapter_id,
        topic=meta["topic"],
        result=result,
        elapsed_ms=elapsed_ms,
    )


# ---------------------------------------------------------------------------
# 정적 파일 및 SPA 폴백
# ---------------------------------------------------------------------------

@app.get("/", response_class=FileResponse, include_in_schema=False)
def index() -> FileResponse:
    """프론트엔드 SPA 진입점(index.html)을 제공합니다."""
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
