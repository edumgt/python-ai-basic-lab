# [초등학생 설명 주석 적용됨]
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: Path를(을) 파일·디렉토리 경로를 객체로 다루는 pathlib 도구를 불러와요.
from pathlib import Path
# 설명: Any를(을) List·Dict 등 타입 힌트를 위한 typing 모듈을 불러와요.
from typing import Any

# 설명: FastAPI, HTTPException를(을) Python용 고성능 웹 API 프레임워크 FastAPI를 불러와요.
from fastapi import FastAPI, HTTPException
# 설명: CORSMiddleware를(을) Python용 고성능 웹 API 프레임워크 FastAPI를 불러와요.
from fastapi.middleware.cors import CORSMiddleware
# 설명: FileResponse를(을) Python용 고성능 웹 API 프레임워크 FastAPI를 불러와요.
from fastapi.responses import FileResponse
# 설명: StaticFiles를(을) Python용 고성능 웹 API 프레임워크 FastAPI를 불러와요.
from fastapi.staticfiles import StaticFiles
# 설명: BaseModel를(을) 데이터 유효성 검사를 위한 Pydantic 라이브러리를 불러와요.
from pydantic import BaseModel

# 설명: FastAPI 웹 애플리케이션 인스턴스를 생성해요.
app = FastAPI(title="AI/ML Basic Class API", version="1.0.0")

# 설명: 모든 요청에 공통으로 적용할 미들웨어(CORS 등)를 등록해요.
app.add_middleware(
    # 설명: 이 코드를 실행해요.
    CORSMiddleware,
    # 설명: 'allow_origins' 변수에 값을 계산해서 저장해요.
    allow_origins=["*"],
    # 설명: 'allow_credentials' 변수에 값을 계산해서 저장해요.
    allow_credentials=True,
    # 설명: 'allow_methods' 변수에 값을 계산해서 저장해요.
    allow_methods=["*"],
    # 설명: 'allow_headers' 변수에 값을 계산해서 저장해요.
    allow_headers=["*"],
# 설명: 이 코드를 실행해요.
)

# 설명: 프로젝트 루트 디렉토리 경로를 BASE_DIR에 저장해요.
BASE_DIR = Path(__file__).resolve().parents[2]
# 설명: 챕터 파일들이 위치한 디렉토리 경로를 저장해요.
CHAPTERS_DIR = BASE_DIR / "chapters"
# 설명: 프론트엔드 파일들이 위치한 디렉토리 경로를 저장해요.
FRONTEND_DIR = BASE_DIR / "frontend"


# 설명: 'ChapterSummary' 데이터 클래스(스키마)를 정의해요.
class ChapterSummary(BaseModel):
    # 설명: 이 코드를 실행해요.
    id: str
    # 설명: 이 코드를 실행해요.
    title: str
    # 설명: 이 코드를 실행해요.
    path: str


# 설명: 'ChapterRunResponse' 데이터 클래스(스키마)를 정의해요.
class ChapterRunResponse(BaseModel):
    # 설명: 이 코드를 실행해요.
    chapter: str
    # 설명: 이 코드를 실행해요.
    result: dict[str, Any]


# 설명: 'ChapterSourceResponse' 데이터 클래스(스키마)를 정의해요.
class ChapterSourceResponse(BaseModel):
    # 설명: 이 코드를 실행해요.
    chapter: str
    # 설명: 이 코드를 실행해요.
    source: str


# 설명: 'load_chapters' 함수를 정의해요.
def load_chapters() -> list[ChapterSummary]:
    # 설명: 'items: list[ChapterSummary]' 변수에 값을 계산해서 저장해요.
    items: list[ChapterSummary] = []
    # 설명: 'sorted(CHAPTERS_DIR.glob("chapter*"))'의 각 원소를 'chapter_dir'로 받으며 반복해요.
    for chapter_dir in sorted(CHAPTERS_DIR.glob("chapter*")):
        # 설명: 'readme' 변수에 값을 계산해서 저장해요.
        readme = chapter_dir / "README.md"
        # 설명: 'title' 변수에 값을 계산해서 저장해요.
        title = chapter_dir.name
        # 설명: 조건 (readme.exists())이 참인지 확인해요.
        if readme.exists():
            # 설명: 파일의 내용을 텍스트 문자열로 읽어요.
            first_line = readme.read_text(encoding="utf-8").splitlines()[0]
            # 설명: 'title' 변수에 값을 계산해서 저장해요.
            title = first_line.replace("#", "").strip()
        # 설명: 이 코드를 실행해요.
        items.append(
            # 설명: 이 코드를 실행해요.
            ChapterSummary(
                # 설명: 'id' 변수에 값을 계산해서 저장해요.
                id=chapter_dir.name,
                # 설명: 'title' 변수에 값을 계산해서 저장해요.
                title=title,
                # 설명: 값을 문자열로 변환해요.
                path=str(chapter_dir.relative_to(BASE_DIR)),
            # 설명: 이 코드를 실행해요.
            )
        # 설명: 이 코드를 실행해요.
        )
    # 설명: 'items'을(를) 함수 호출 측에 반환해요.
    return items


# 설명: '/api/health' 경로에 HTTP GET 핸들러를 등록해요.
@app.get("/api/health")
# 설명: 'health' 함수를 정의해요.
def health() -> dict[str, str]:
    # 설명: '{"status": "ok"}'을(를) 함수 호출 측에 반환해요.
    return {"status": "ok"}


# 설명: '/api/chapters' 경로에 HTTP GET 핸들러를 등록해요.
@app.get("/api/chapters", response_model=list[ChapterSummary])
# 설명: 'chapters' 함수를 정의해요.
def chapters() -> list[ChapterSummary]:
    # 설명: 'load_chapters()'을(를) 함수 호출 측에 반환해요.
    return load_chapters()


# 설명: '/api/chapters/{chapter_id}/run' 경로에 HTTP POST 핸들러를 등록해요.
@app.post("/api/chapters/{chapter_id}/run", response_model=ChapterRunResponse)
# 설명: 'run_chapter' 함수를 정의해요.
def run_chapter(chapter_id: str) -> ChapterRunResponse:
    # 설명: 'chapter_path' 변수에 값을 계산해서 저장해요.
    chapter_path = CHAPTERS_DIR / chapter_id / "practice.py"
    # 설명: 조건 (not chapter_path.exists())이 참인지 확인해요.
    if not chapter_path.exists():
        # 설명: 오류를 직접 발생시켜요.
        raise HTTPException(status_code=404, detail="chapter not found")

    # 설명: 'namespace: dict[str, Any]' 변수에 값을 계산해서 저장해요.
    namespace: dict[str, Any] = {}
    # 설명: 파이썬 파일의 소스 코드 텍스트를 읽어 저장해요.
    code = chapter_path.read_text(encoding="utf-8")
    # 설명: 값을 문자열로 변환해요.
    exec(compile(code, str(chapter_path), "exec"), namespace)
    # 설명: 조건 ("run" not in namespace)이 참인지 확인해요.
    if "run" not in namespace:
        # 설명: 오류를 직접 발생시켜요.
        raise HTTPException(status_code=500, detail="run function not found")

    # 설명: 'result' 변수에 값을 계산해서 저장해요.
    result = namespace["run"]()
    # 설명: 'ChapterRunResponse(chapter=chapter_id, result=result)'을(를) 함수 호출 측에 반환해요.
    return ChapterRunResponse(chapter=chapter_id, result=result)


# 설명: '/api/chapters/{chapter_id}/source' 경로에 HTTP GET 핸들러를 등록해요.
@app.get("/api/chapters/{chapter_id}/source", response_model=ChapterSourceResponse)
# 설명: 'chapter_source' 함수를 정의해요.
def chapter_source(chapter_id: str) -> ChapterSourceResponse:
    # 설명: 'chapter_path' 변수에 값을 계산해서 저장해요.
    chapter_path = CHAPTERS_DIR / chapter_id / "practice.py"
    # 설명: 조건 (not chapter_path.exists())이 참인지 확인해요.
    if not chapter_path.exists():
        # 설명: 오류를 직접 발생시켜요.
        raise HTTPException(status_code=404, detail="chapter not found")

    # 설명: 파일의 내용을 텍스트 문자열로 읽어요.
    source = chapter_path.read_text(encoding="utf-8")
    # 설명: 'ChapterSourceResponse(chapter=chapter_id, source=source)'을(를) 함수 호출 측에 반환해요.
    return ChapterSourceResponse(chapter=chapter_id, source=source)


# 설명: '/' 경로에 HTTP GET 핸들러를 등록해요.
@app.get("/")
# 설명: 'index' 함수를 정의해요.
def index() -> FileResponse:
    # 설명: 'FileResponse(FRONTEND_DIR / "index.html")'을(를) 함수 호출 측에 반환해요.
    return FileResponse(FRONTEND_DIR / "index.html")


# 설명: 정적 파일(HTML·CSS·JS)을 특정 URL 경로에 연결해요.
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
