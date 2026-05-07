#!/usr/bin/env python3
"""Generate beginner-friendly Python comments, folder explanations, and Korean TTS MP3 files."""
from __future__ import annotations

import argparse
import ast
import asyncio
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOICE_NAME = "ko-KR-SunHiNeural"  # Korean female voice

# ---------------------------------------------------------------------------
# 임포트 구문별 구체적 설명 사전
# ---------------------------------------------------------------------------
_IMPORT_MAP: dict[str, str] = {
    "numpy": "수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.",
    "pandas": "표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.",
    "sklearn.datasets": "연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.",
    "sklearn.linear_model": "선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.",
    "sklearn.ensemble": "랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.",
    "sklearn.tree": "결정 트리 모델 도구를 불러와요.",
    "sklearn.cluster": "K-Means 등 비지도 군집화 도구를 불러와요.",
    "sklearn.decomposition": "PCA 등 차원 축소 도구를 불러와요.",
    "sklearn.metrics": "정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.",
    "sklearn.model_selection": "데이터 분리·교차검증 등 모델 선택 도구를 불러와요.",
    "sklearn.pipeline": "전처리와 모델을 하나로 묶는 Pipeline 도구를 불러와요.",
    "sklearn.preprocessing": "표준화·인코딩 등 데이터 전처리 도구를 불러와요.",
    "sklearn.compose": "컬럼별 다른 전처리를 조합하는 ColumnTransformer 도구를 불러와요.",
    "fastapi": "Python용 고성능 웹 API 프레임워크 FastAPI를 불러와요.",
    "pydantic": "데이터 유효성 검사를 위한 Pydantic 라이브러리를 불러와요.",
    "pathlib": "파일·디렉토리 경로를 객체로 다루는 pathlib 도구를 불러와요.",
    "joblib": "모델 저장·병렬 처리를 위한 joblib 라이브러리를 불러와요.",
    "math": "수학 함수(sqrt·log·sin 등)를 제공하는 math 모듈을 불러와요.",
    "random": "난수 생성을 위한 random 모듈을 불러와요.",
    "os": "운영체제 파일·경로 작업을 위한 os 모듈을 불러와요.",
    "sys": "파이썬 런타임 제어를 위한 sys 모듈을 불러와요.",
    "json": "JSON 데이터 인코딩·디코딩을 위한 json 모듈을 불러와요.",
    "typing": "List·Dict 등 타입 힌트를 위한 typing 모듈을 불러와요.",
    "__future__": "최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.",
    "argparse": "커맨드라인 인자를 파싱하는 argparse 모듈을 불러와요.",
    "ast": "파이썬 코드를 문법 트리로 분석하는 ast 모듈을 불러와요.",
    "asyncio": "비동기 프로그래밍을 지원하는 asyncio 모듈을 불러와요.",
    "re": "정규 표현식(패턴 검색·치환)을 위한 re 모듈을 불러와요.",
}

# ---------------------------------------------------------------------------
# 함수 호출 패턴별 구체적 설명 (순서 중요: 더 구체적인 것이 앞에 위치)
# ---------------------------------------------------------------------------
_CALL_PATTERNS: list[tuple[str, str]] = [
    # 난수·시드
    (r"np\.random\.seed\(", "난수 생성 시드를 고정해요 — 같은 시드이면 항상 같은 결과가 나와요."),
    (r"np\.random\.normal\(", "정규분포(평균·표준편차 지정)를 따르는 난수 배열을 생성해요."),
    (r"np\.random\.binomial\(", "이항분포를 따르는 난수를 생성해요."),
    (r"np\.random\.rand\(", "0~1 사이 균등분포 난수 배열을 생성해요."),
    (r"np\.random\.randn\(", "표준 정규분포(평균 0, 표준편차 1) 난수 배열을 생성해요."),
    (r"np\.random\.randint\(", "지정 범위의 정수 난수 배열을 생성해요."),
    # sklearn 데이터 생성
    (r"make_classification\(", "분류 연습용 가상 데이터셋(특성 X, 레이블 y)을 생성해요."),
    (r"make_regression\(", "회귀 연습용 가상 데이터셋(특성 X, 연속값 y)을 생성해요."),
    # 데이터 분리·교차검증
    (r"train_test_split\(", "데이터를 학습용과 테스트용으로 분리해요."),
    (r"KFold\(", "K-폴드 교차검증 분할기를 생성해요."),
    (r"cross_val_score\(", "K-폴드 교차검증을 수행해 각 폴드의 평가 점수를 반환해요."),
    # 모델 학습·예측
    (r"\.fit_transform\(", "변환기(스케일러 등)를 학습하고 동시에 데이터를 변환해요."),
    (r"\.fit\(", "모델 또는 변환기를 학습 데이터로 훈련시켜요."),
    (r"\.predict_proba\(", "각 클래스에 속할 확률을 예측해요."),
    (r"\.predict\(", "학습된 모델로 새 데이터에 대한 예측값을 계산해요."),
    (r"\.transform\(", "이미 학습된 변환기로 데이터를 변환해요."),
    (r"\.score\(", "학습된 모델의 성능 점수(기본: 정확도/R²)를 계산해요."),
    # 평가 지표
    (r"accuracy_score\(", "정답과 예측값을 비교해 정확도(0~1)를 계산해요."),
    (r"f1_score\(", "정밀도와 재현율의 조화평균인 F1 점수를 계산해요."),
    (r"precision_score\(", "양성으로 예측한 것 중 실제 양성 비율(정밀도)을 계산해요."),
    (r"recall_score\(", "실제 양성 중 양성으로 예측한 비율(재현율)을 계산해요."),
    (r"roc_auc_score\(", "ROC 곡선 아래 면적(AUC)을 계산해요 — 1에 가까울수록 좋아요."),
    (r"r2_score\(", "결정계수(R²)로 모델이 분산을 얼마나 설명하는지 측정해요."),
    (r"mean_absolute_error\(", "예측 오차 절댓값의 평균(MAE)을 계산해요."),
    (r"mean_squared_error\(", "오차 제곱 평균(MSE)을 계산해요 — 클수록 예측이 부정확해요."),
    # 스케일러·인코더
    (r"StandardScaler\(", "데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요."),
    (r"MinMaxScaler\(", "데이터를 0~1 범위로 정규화하는 스케일러를 생성해요."),
    (r"OneHotEncoder\(", "범주형 값을 0/1 이진 벡터로 변환하는 인코더를 생성해요."),
    (r"LabelEncoder\(", "문자열 레이블을 정수 인덱스로 변환하는 인코더를 생성해요."),
    (r"ColumnTransformer\(", "컬럼 종류(수치형·범주형)별로 다른 전처리를 적용해요."),
    (r"pd\.get_dummies\(", "범주형 컬럼을 원-핫 인코딩(0/1 플래그 컬럼)으로 변환해요."),
    # 모델 생성
    (r"LinearRegression\(", "선형 회귀 모델(y = w·x + b)을 생성해요."),
    (r"LogisticRegression\(", "로지스틱 회귀 분류 모델을 생성해요."),
    (r"Ridge\(", "L2 규제(계수 크기 제한)를 적용한 릿지 회귀 모델을 생성해요."),
    (r"Lasso\(", "L1 규제(불필요한 계수를 0으로 만듦)를 적용한 라쏘 회귀 모델을 생성해요."),
    (r"DecisionTreeClassifier\(", "결정 트리 분류 모델을 생성해요."),
    (r"DecisionTreeRegressor\(", "결정 트리 회귀 모델을 생성해요."),
    (r"RandomForestClassifier\(", "여러 결정 트리를 앙상블한 랜덤 포레스트 분류 모델을 생성해요."),
    (r"RandomForestRegressor\(", "랜덤 포레스트 회귀 모델을 생성해요."),
    (r"GradientBoostingClassifier\(", "그래디언트 부스팅 분류 모델을 생성해요."),
    (r"GradientBoostingRegressor\(", "그래디언트 부스팅 회귀 모델을 생성해요."),
    (r"KMeans\(", "K-평균 군집화 모델을 생성해요."),
    (r"PCA\(", "주성분 분석(PCA)으로 고차원 데이터를 저차원으로 줄이는 변환기를 생성해요."),
    (r"IsolationForest\(", "이상치 탐지를 위한 격리 숲 모델을 생성해요."),
    (r"Pipeline\(", "전처리 단계와 모델을 하나의 파이프라인으로 연결해요."),
    # 모델 저장·불러오기
    (r"joblib\.dump\(", "학습된 모델을 파일에 저장해요 — 나중에 다시 불러올 수 있어요."),
    (r"joblib\.load\(", "저장된 모델 파일을 불러와요."),
    # NumPy 배열 생성·조작
    (r"np\.array\(", "파이썬 리스트·시퀀스를 NumPy 배열로 변환해요."),
    (r"np\.zeros\(", "모든 원소가 0인 NumPy 배열을 생성해요."),
    (r"np\.ones\(", "모든 원소가 1인 NumPy 배열을 생성해요."),
    (r"np\.eye\(", "대각선이 1이고 나머지가 0인 단위 행렬을 생성해요."),
    (r"np\.linspace\(", "시작~끝 범위를 균등 간격으로 나눈 배열을 생성해요."),
    (r"np\.arange\(", "지정 범위의 연속 정수·간격 배열을 생성해요."),
    (r"np\.vstack\(", "여러 배열을 수직(행 방향)으로 쌓아요."),
    (r"np\.hstack\(", "여러 배열을 수평(열 방향)으로 이어 붙여요."),
    (r"np\.concatenate\(", "여러 배열을 지정한 축 방향으로 연결해요."),
    (r"np\.reshape\(", "배열의 형태(shape)를 원소 수 유지하며 바꿔요."),
    # NumPy 수학 연산
    (r"np\.maximum\(0", "음수는 0으로, 양수는 그대로 유지하는 ReLU 활성화 함수예요."),
    (r"np\.maximum\(", "두 배열을 원소별로 비교해 더 큰 값을 선택해요."),
    (r"np\.minimum\(", "두 배열을 원소별로 비교해 더 작은 값을 선택해요."),
    (r"np\.exp\(", "e의 거듭제곱(지수 함수)을 원소별로 계산해요."),
    (r"np\.log\(", "자연로그(밑 e)를 원소별로 계산해요."),
    (r"np\.sqrt\(", "제곱근을 원소별로 계산해요."),
    (r"np\.abs\(", "절댓값을 원소별로 계산해요."),
    (r"np\.sin\(", "사인(sin) 값을 원소별로 계산해요."),
    (r"np\.cos\(", "코사인(cos) 값을 원소별로 계산해요."),
    (r"np\.tanh\(", "쌍곡 탄젠트(tanh) 활성화 함수를 원소별로 계산해요."),
    (r"np\.clip\(", "배열 값을 지정된 최솟값·최댓값 범위 안으로 제한해요."),
    (r"np\.sum\(", "배열 원소의 합계를 계산해요."),
    (r"np\.mean\(", "배열 원소의 평균값을 계산해요."),
    (r"np\.std\(", "배열 원소의 표준편차를 계산해요."),
    (r"np\.var\(", "배열 원소의 분산을 계산해요."),
    (r"np\.max\(", "배열에서 가장 큰 값을 찾아요."),
    (r"np\.min\(", "배열에서 가장 작은 값을 찾아요."),
    (r"np\.argmax\(", "배열에서 가장 큰 값이 있는 위치(인덱스)를 반환해요."),
    (r"np\.argmin\(", "배열에서 가장 작은 값이 있는 위치(인덱스)를 반환해요."),
    (r"np\.unique\(", "배열에서 중복을 제거한 고유값 배열을 반환해요."),
    (r"np\.count_nonzero\(", "배열에서 0이 아닌 원소의 개수를 세요."),
    (r"np\.allclose\(", "두 배열의 모든 원소가 허용 오차 내에서 같은지 확인해요."),
    (r"np\.where\(", "조건이 참인 원소의 인덱스를 찾거나 조건부 값을 선택해요."),
    (r"np\.dot\(", "두 배열의 내적(행렬 곱)을 계산해요."),
    (r"np\.linalg\.solve\(", "선형 방정식 Ax = b를 풀어 해 벡터 x를 구해요."),
    (r"np\.linalg\.norm\(", "벡터 또는 행렬의 크기(놈, 유클리드 거리 등)를 계산해요."),
    (r"np\.linalg\.eig\(", "행렬의 고유값(eigenvalue)과 고유벡터를 계산해요."),
    (r"np\.linalg\.det\(", "정방 행렬의 행렬식(determinant)을 계산해요."),
    # Pandas 연산
    (r"pd\.DataFrame\(", "딕셔너리·리스트 등을 Pandas 표(DataFrame)로 만들어요."),
    (r"pd\.Series\(", "1차원 데이터를 Pandas 시리즈(Series)로 만들어요."),
    (r"pd\.read_csv\(", "CSV 파일을 읽어 DataFrame으로 불러와요."),
    (r"pd\.concat\(", "여러 DataFrame을 행 또는 열 방향으로 연결해요."),
    (r"\.groupby\(", "지정한 컬럼 값으로 데이터를 그룹화해요."),
    (r"\.fillna\(", "결측값(NaN)을 지정한 값으로 채워요."),
    (r"\.dropna\(", "결측값이 있는 행 또는 열을 제거해요."),
    (r"\.isna\(\)\.sum\(\)", "컬럼별 결측값 개수를 세요."),
    (r"\.isna\(", "각 원소가 결측값(NaN)인지 True/False로 확인해요."),
    (r"\.rolling\(", "이동 윈도우를 설정해 이동평균 등을 계산할 수 있어요."),
    (r"\.shift\(", "시계열 데이터를 지정된 단계만큼 앞 또는 뒤로 이동시켜요."),
    (r"\.mean\(\)", "평균값을 계산해요."),
    (r"\.std\(\)", "표준편차를 계산해요."),
    (r"\.sum\(\)", "합계를 계산해요."),
    (r"\.abs\(\)", "절댓값을 원소별로 계산해요."),
    # 형변환·유틸
    (r"\.tolist\(\)", "NumPy 배열을 파이썬 리스트로 변환해요."),
    (r"\.round\(", "지정된 소수점 자릿수에서 반올림해요."),
    (r"\.reshape\(", "배열의 형태를 바꿔요."),
    (r"\.flatten\(", "다차원 배열을 1차원으로 펼쳐요."),
    (r"int\(", "값을 정수형으로 변환해요."),
    (r"float\(", "값을 부동소수점(실수)형으로 변환해요."),
    (r"bool\(", "값을 불리언(True/False)형으로 변환해요."),
    (r"str\(", "값을 문자열로 변환해요."),
    (r"list\(", "값을 파이썬 리스트로 변환해요."),
    (r"sorted\(", "시퀀스를 정렬한 새 리스트를 반환해요."),
    (r"len\(", "시퀀스의 원소 개수를 반환해요."),
    (r"range\(", "지정 범위의 정수 시퀀스를 생성해요."),
    (r"enumerate\(", "인덱스와 값을 쌍으로 반환하는 열거 이터레이터를 만들어요."),
    (r"zip\(", "여러 시퀀스를 짝지어 묶는 이터레이터를 만들어요."),
    (r"abs\(", "숫자의 절댓값을 계산해요."),
    (r"round\(", "숫자를 지정한 소수점 자리에서 반올림해요."),
    (r"math\.ceil\(", "소수를 올림하여 가장 가까운 정수를 반환해요."),
    (r"math\.floor\(", "소수를 내림하여 가장 가까운 정수를 반환해요."),
    (r"math\.sqrt\(", "제곱근을 계산해요."),
    (r"math\.log\(", "로그 값을 계산해요."),
    (r"math\.exp\(", "e의 거듭제곱을 계산해요."),
    # FastAPI
    (r"FastAPI\(", "FastAPI 웹 애플리케이션 인스턴스를 생성해요."),
    (r"app\.add_middleware\(", "모든 요청에 공통으로 적용할 미들웨어(CORS 등)를 등록해요."),
    (r"app\.mount\(", "정적 파일(HTML·CSS·JS)을 특정 URL 경로에 연결해요."),
    (r"@app\.get\(", "이 함수를 HTTP GET 요청 처리기로 등록해요."),
    (r"@app\.post\(", "이 함수를 HTTP POST 요청 처리기로 등록해요."),
    (r"raise HTTPException\(", "HTTP 오류 응답(상태 코드 + 메시지)을 반환해요."),
    (r"FileResponse\(", "파일을 HTTP 응답으로 전송해요."),
    (r"exec\(compile\(", "문자열로 된 파이썬 코드를 동적으로 컴파일하고 실행해요."),
    # 경로·파일
    (r"Path\(__file__\)\.resolve\(\)\.parents\[", "현재 파일 기준으로 상위 폴더 경로를 계산해요."),
    (r"Path\(__file__\)", "현재 파이썬 파일의 경로 객체를 가져와요."),
    (r"Path\(", "문자열 경로를 Path 객체(파일·폴더 조작 가능)로 만들어요."),
    (r"\.read_text\(", "파일의 내용을 텍스트 문자열로 읽어요."),
    (r"\.write_text\(", "텍스트를 파일에 써요."),
    (r"\.exists\(\)", "파일 또는 폴더가 실제로 존재하는지 확인해요."),
    (r"\.glob\(", "패턴에 맞는 파일·폴더 목록을 가져와요."),
    (r"\.splitlines\(", "문자열을 줄 단위로 나눠 리스트로 반환해요."),
    # 출력
    (r"print\(run\(\)\)", "run 함수를 실행하고 결과를 화면에 출력해요."),
    (r"print\(", "괄호 안의 값을 화면에 출력해요."),
    # argparse
    (r"ArgumentParser\(", "커맨드라인 인수를 파싱하는 파서를 생성해요."),
    (r"add_argument\(", "파서에 새로운 커맨드라인 옵션을 추가해요."),
    (r"parse_args\(", "실제 커맨드라인 인수를 파싱해 결과 객체를 반환해요."),
    # asyncio
    (r"asyncio\.run\(", "비동기 코루틴을 실행하고 완료될 때까지 기다려요."),
]


def find_python_files() -> list[Path]:
    """chapters 아래 모든 practice.py와 backend/app/main.py 목록을 반환해요."""
    files = sorted(ROOT.glob("chapters/chapter*/practice.py"))
    backend = ROOT / "backend/app/main.py"
    if backend.exists():
        files.append(backend)
    return files


def _import_explain(stripped: str) -> str:
    """import/from 구문에서 모듈 이름을 추출해 구체적인 설명을 반환해요."""
    # from X import Y 형태
    m = re.match(r"from\s+([\w.]+)\s+import\s+(.+)", stripped)
    if m:
        module = m.group(1)
        names = m.group(2).strip()
        # 가장 긴 매칭 모듈명 우선
        for key in sorted(_IMPORT_MAP, key=len, reverse=True):
            if module.startswith(key):
                desc = _IMPORT_MAP[key]
                return f"{names}를(을) {desc}"
        return f"'{module}' 모듈에서 {names}를(을) 불러와요."
    # import X as Y 또는 import X
    m2 = re.match(r"import\s+([\w.]+)(?:\s+as\s+\w+)?", stripped)
    if m2:
        module = m2.group(1)
        for key in sorted(_IMPORT_MAP, key=len, reverse=True):
            if module.startswith(key):
                return _IMPORT_MAP[key]
        return f"'{module}' 모듈을 불러와요."
    return "필요한 도구를 불러와요."


def _assignment_explain(stripped: str) -> str | None:
    """변수 할당 구문의 왼쪽을 보고 구체적인 설명을 반환해요.
    특정 패턴에 매칭되지 않으면 None을 반환해 CALL_PATTERNS 매칭으로 넘겨줘요.
    """
    # 공통 패턴: X, y = ...  →  특성(X)과 레이블(y) 분리
    if re.match(r"X\s*,\s*y\s*=", stripped):
        return "특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요."
    if re.match(r"X_train\s*,\s*X_test\s*,\s*y_train\s*,\s*y_test\s*=", stripped):
        return "데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요."
    if re.match(r"h\s*,\s*w\s*=", stripped):
        return "배열의 높이(h)와 너비(w)를 한 번에 꺼내요."
    if re.match(r"kh\s*,\s*kw\s*=", stripped):
        return "커널의 높이(kh)와 너비(kw)를 한 번에 꺼내요."
    if re.match(r"out_h\s*=", stripped):
        return "출력 높이를 계산해요 — (입력 크기 - 커널 크기) / 스트라이드 + 1."
    if re.match(r"out_w\s*=", stripped):
        return "출력 너비를 계산해요 — (입력 크기 - 커널 크기) / 스트라이드 + 1."
    # 자주 쓰는 변수명 패턴
    if re.match(r"result\s*=\s*\{", stripped):
        return "챕터·주제 정보와 실습 결과를 담을 딕셔너리를 초기화해요."
    if re.match(r"result\[", stripped):
        return "계산 결과를 result 딕셔너리에 저장해요."
    if re.match(r"LESSON_10MIN\s*=", stripped):
        return "10분 요약 학습 내용을 상수 문자열로 정의해요."
    if re.match(r"PRACTICE_30MIN\s*=", stripped):
        return "30분 실습 목표를 상수 문자열로 정의해요."
    if re.match(r"BASE_DIR\s*=", stripped):
        return "프로젝트 루트 디렉토리 경로를 BASE_DIR에 저장해요."
    if re.match(r"CHAPTERS_DIR\s*=", stripped):
        return "챕터 파일들이 위치한 디렉토리 경로를 저장해요."
    if re.match(r"FRONTEND_DIR\s*=", stripped):
        return "프론트엔드 파일들이 위치한 디렉토리 경로를 저장해요."
    if re.match(r"model\s*=", stripped):
        return "모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요."
    if re.match(r"pred\s*=", stripped):
        return "모델의 예측값을 pred 변수에 저장해요."
    if re.match(r"score\w*\s*=", stripped):
        return "평가 점수를 계산해서 저장해요."
    if re.match(r"loss\w*\s*=", stripped):
        return "손실 값을 계산해서 저장해요."
    if re.match(r"z\s*=", stripped):
        return "z-점수(표준 정규 점수)를 계산해요 — (값 - 평균) / 표준편차."
    if re.match(r"mse\s*=", stripped):
        return "평균 제곱 오차(MSE)를 계산해 저장해요."
    if re.match(r"cross_entropy\s*=", stripped):
        return "크로스 엔트로피 손실(분류 오차 척도)을 계산해요."
    if re.match(r"eps\s*=", stripped):
        return "log(0) 방지를 위한 아주 작은 값(epsilon)을 정의해요."
    if re.match(r"threshold\s*=", stripped):
        return "이상치 판별 기준값(임계값)을 설정해요."
    if re.match(r"outlier_idx\s*=", stripped):
        return "임계값을 초과한 이상치의 인덱스를 찾아요."
    if re.match(r"namespace\s*=", stripped):
        return "동적 코드 실행 결과를 담을 빈 네임스페이스 딕셔너리를 생성해요."
    if re.match(r"code\s*=", stripped):
        return "파이썬 파일의 소스 코드 텍스트를 읽어 저장해요."
    if re.match(r"pipe\s*=", stripped):
        return "전처리와 모델을 하나로 묶은 Pipeline 객체를 생성해요."
    if re.match(r"cv\s*=", stripped):
        return "K-폴드 교차검증 분할기를 생성해요."
    if re.match(r"scores\s*=", stripped):
        return "교차검증 각 폴드별 평가 점수 배열을 저장해요."
    if re.match(r"model_path\s*=", stripped):
        return "모델 파일을 저장할 경로를 지정해요."
    if re.match(r"loaded\s*=", stripped):
        return "저장된 모델 파일을 불러와 loaded 변수에 저장해요."
    if re.match(r"pca\s*=", stripped):
        return "PCA(주성분 분석) 변환기를 생성해요."
    if re.match(r"reduced\s*=", stripped):
        return "PCA로 차원을 축소한 데이터를 저장해요."
    if re.match(r"transformed\s*=", stripped):
        return "전처리 변환이 완료된 데이터를 저장해요."
    if re.match(r"df\s*=", stripped):
        return "표(DataFrame) 형태의 데이터를 df 변수에 저장해요."
    if re.match(r"series\s*=", stripped):
        return "1차원 시계열 데이터를 Series 형태로 저장해요."
    if re.match(r"y_true\w*\s*=", stripped):
        return "실제 정답 레이블 배열을 정의해요."
    if re.match(r"y_pred\w*\s*=", stripped):
        return "모델이 예측한 레이블 배열을 정의해요."
    if re.match(r"y_prob\s*=", stripped):
        return "모델이 각 클래스에 대해 예측한 확률 배열을 정의해요."
    if re.match(r"probs\s*=", stripped):
        return "소프트맥스 출력 등 각 클래스의 확률 배열을 정의해요."
    if re.match(r"chosen\w*\s*=", stripped):
        return "각 샘플에서 정답 클래스에 해당하는 예측 확률을 추출해요."
    if re.match(r"patch\s*=", stripped):
        return "현재 위치에서 커널 크기만큼 이미지 일부분(패치)을 잘라내요."
    if re.match(r"block\s*=", stripped):
        return "현재 위치에서 풀링 크기만큼 특성 맵 블록을 잘라내요."
    if re.match(r"conv_out\s*=", stripped):
        return "합성곱(Convolution) 연산 결과를 저장해요."
    if re.match(r"relu_out\s*=", stripped):
        return "ReLU 활성화 함수를 적용한 결과를 저장해요."
    if re.match(r"pool_out\s*=", stripped):
        return "최대 풀링(Max Pooling) 연산 결과를 저장해요."
    if re.match(r"out\s*=|out_\w+\s*=", stripped):
        return "출력 결과를 저장할 배열을 초기화해요."
    if re.match(r"image\s*=", stripped):
        return "입력 이미지 픽셀 값을 2D 배열로 정의해요."
    if re.match(r"kernel\s*=", stripped):
        return "합성곱 커널(필터) 가중치를 2D 배열로 정의해요."
    if re.match(r"encoded\s*=", stripped):
        return "원-핫 인코딩된 0/1 행렬을 저장해요."
    if re.match(r"group_rate\s*=", stripped):
        return "집단별 평균 비율을 계산해 딕셔너리로 저장해요."
    if re.match(r"parity_gap\s*=", stripped):
        return "두 집단 간 비율 차이(공정성 지표)를 계산해요."
    if re.match(r"steps_per_epoch\s*=", stripped):
        return "한 에폭 당 업데이트 횟수(스텝 수)를 계산해요."
    if re.match(r"total_updates\s*=", stripped):
        return "전체 에폭 동안 총 업데이트 횟수를 계산해요."
    if re.match(r"relative_noise\s*=", stripped):
        return "배치 크기에 따른 상대적 그래디언트 노이즈를 추정해요."
    if re.match(r"shifted\s*=", stripped):
        return "수치 안정성을 위해 로짓에서 최댓값을 빼요 (오버플로 방지)."
    if re.match(r"exp_scores\s*=", stripped):
        return "이동된 로짓에 지수 함수를 적용해요."
    if re.match(r"n\s*=\s*len\(", stripped):
        return "샘플 수(데이터 개수)를 n 변수에 저장해요."
    if re.match(r"mean\s*=", stripped):
        return "데이터의 평균값을 계산해 저장해요."
    if re.match(r"std\s*=", stripped):
        return "데이터의 표준편차를 계산해 저장해요."
    # 특정 패턴 없음 → None 반환 (CALL_PATTERNS로 fallthrough)
    return None


def _assignment_explain_generic(stripped: str) -> str:
    """할당문의 최종 fallback 설명이에요."""
    lhs = stripped.split("=")[0].strip()
    if lhs:
        return f"'{lhs}' 변수에 값을 계산해서 저장해요."
    return "값을 저장하거나 바꿔요."


def line_explain(stripped: str) -> str:
    """한 줄 코드를 받아 구체적인 한국어 설명을 반환해요."""
    # --- 1. import / from 구문 ---
    if stripped.startswith("from ") or stripped.startswith("import "):
        return _import_explain(stripped)

    # --- 2. def / class ---
    if stripped.startswith("def "):
        name = stripped[4:].split("(", 1)[0].strip()
        return f"'{name}' 함수를 정의해요."
    if stripped.startswith("class "):
        name = stripped[6:].split("(", 1)[0].split(":", 1)[0].strip()
        return f"'{name}' 데이터 클래스(스키마)를 정의해요."

    # --- 3. 데코레이터 ---
    if stripped.startswith("@app.get("):
        path = re.search(r'@app\.get\("([^"]+)"', stripped)
        return f"'{path.group(1)}' 경로에 HTTP GET 핸들러를 등록해요." if path else "HTTP GET 핸들러를 등록해요."
    if stripped.startswith("@app.post("):
        path = re.search(r'@app\.post\("([^"]+)"', stripped)
        return f"'{path.group(1)}' 경로에 HTTP POST 핸들러를 등록해요." if path else "HTTP POST 핸들러를 등록해요."
    if stripped.startswith("@"):
        return "다음 함수에 데코레이터를 적용해요."

    # --- 4. 제어 흐름 ---
    if re.match(r'if\s+__name__\s*==\s*["\']__main__["\']', stripped):
        return "이 파일을 직접 실행했을 때만 아래 코드를 수행해요."
    if stripped.startswith("if "):
        cond = stripped[3:].rstrip(":")
        return f"조건 ({cond})이 참인지 확인해요."
    if stripped.startswith("elif "):
        cond = stripped[5:].rstrip(":")
        return f"앞 조건이 거짓이면, ({cond}) 조건을 확인해요."
    if stripped.startswith("else:") or stripped == "else":
        return "앞의 모든 조건이 거짓일 때 실행해요."
    if stripped.startswith("for "):
        m = re.match(r"for\s+(\S+)\s+in\s+(.+?):", stripped)
        if m:
            var, iterable = m.group(1), m.group(2).strip()
            return f"'{iterable}'의 각 원소를 '{var}'로 받으며 반복해요."
        return "각 원소를 순서대로 꺼내며 반복해요."
    if stripped.startswith("while "):
        cond = stripped[6:].rstrip(":")
        return f"({cond}) 조건이 참인 동안 반복해요."
    if stripped.startswith("break"):
        return "현재 반복문을 즉시 탈출해요."
    if stripped.startswith("continue"):
        return "이번 반복을 건너뛰고 다음 반복으로 넘어가요."
    if stripped.startswith("return "):
        val = stripped[7:].strip()
        return f"'{val}'을(를) 함수 호출 측에 반환해요." if val else "함수 실행을 종료하고 None을 반환해요."
    if stripped == "return":
        return "함수 실행을 종료하고 None을 반환해요."
    if stripped.startswith("try:"):
        return "오류가 발생할 수 있는 코드를 시도(try)해요."
    if stripped.startswith("except "):
        exc = stripped[7:].rstrip(":").strip()
        return f"{exc} 오류가 발생하면 여기서 안전하게 처리해요."
    if stripped == "except:":
        return "어떤 오류든 발생하면 여기서 안전하게 처리해요."
    if stripped.startswith("finally:"):
        return "오류 발생 여부와 관계없이 항상 실행해요."
    if stripped.startswith("raise "):
        return "오류를 직접 발생시켜요."
    if stripped.startswith("with "):
        return "파일·자원을 안전하게 열고, 블록을 벗어나면 자동으로 닫아요."
    if stripped.startswith("async def "):
        name = stripped[10:].split("(", 1)[0].strip()
        return f"비동기 함수 '{name}'을 정의해요."
    if stripped.startswith("await "):
        return "비동기 작업이 완료될 때까지 기다려요."

    # --- 5. docstring ---
    if stripped.startswith('"""') or stripped.startswith("'''"):
        return "이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요."

    # --- 6. 변수 할당: 이름 기반 패턴 먼저 확인 ---
    has_assign = "=" in stripped and not stripped.startswith("=")
    if has_assign:
        specific = _assignment_explain(stripped)
        if specific is not None:
            return specific

    # --- 7. 함수 호출 패턴 매칭 ---
    for pattern, explanation in _CALL_PATTERNS:
        if re.search(pattern, stripped):
            return explanation

    # --- 8. 할당 최종 fallback ---
    if has_assign:
        return _assignment_explain_generic(stripped)

    # --- 9. 기타 표현식 ---
    return "이 코드를 실행해요."


def strip_generated_comments(text: str) -> str:
    """기존에 generate_kids_assets.py가 추가한 마커 줄과 '# 설명:' 주석 줄을 제거해요."""
    marker = "# [초등학생 설명 주석 적용됨]"
    lines: list[str] = []
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        # 마커 줄 제거
        if stripped == marker:
            continue
        # 자동 생성된 '# 설명:' 주석 줄 제거 (들여쓰기 상관없이)
        if re.match(r"^\s*# 설명: ", line):
            continue
        lines.append(line)
    return "".join(lines)


def add_line_comments(py_file: Path, *, reset: bool = False) -> bool:
    """py_file에 상세 한국어 주석을 추가해요.

    reset=True이면 기존 자동 주석을 제거한 뒤 새로 생성해요.
    이미 마커가 있고 reset=False이면 건너뛰어요.
    """
    text = py_file.read_text(encoding="utf-8")
    marker = "# [초등학생 설명 주석 적용됨]"

    if reset:
        text = strip_generated_comments(text)
    elif marker in text:
        return False

    out: list[str] = [marker + "\n"]
    for raw in text.splitlines(keepends=True):
        stripped = raw.strip()
        indent = raw[: len(raw) - len(raw.lstrip(" "))]

        if stripped == "" or stripped.startswith("#"):
            out.append(raw)
            continue

        explain = line_explain(stripped)
        out.append(f"{indent}# 설명: {explain}\n")
        out.append(raw)

    py_file.write_text("".join(out), encoding="utf-8")
    return True


def summarize_python_file(py_file: Path) -> tuple[str, list[str], list[str]]:
    text = py_file.read_text(encoding="utf-8")
    tree = ast.parse(text)
    doc = ast.get_docstring(tree) or "이 파일은 Python 실습 예제를 담고 있어요."
    funcs: list[str] = []
    imports: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            funcs.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if base:
                imports.append(base)

    doc_line = doc.strip().splitlines()[0]
    return doc_line, sorted(set(funcs)), sorted(set(imports))


def make_explain_md(folder: Path) -> None:
    py_files = sorted(folder.glob("*.py"))
    title = f"# Python 쉬운 설명 ({folder.name})\n\n"
    intro = (
        "이 문서는 초등학생도 따라할 수 있도록, 폴더 안 Python 파일을 아주 쉽게 설명해요.\n\n"
        "## 먼저 기억해요\n"
        "- `python 파일이름.py` 로 실행해요.\n"
        "- 에러가 나면 메시지를 읽고 천천히 한 줄씩 확인해요.\n"
        "- `run()` 함수가 있으면 그 함수가 핵심 실습이에요.\n\n"
        "## 파일별 설명\n"
    )

    sections: list[str] = []
    for py in py_files:
        doc_line, funcs, imports = summarize_python_file(py)
        funcs_line = ", ".join(f"`{f}`" for f in funcs) if funcs else "없음"
        imports_line = ", ".join(f"`{i}`" for i in imports[:8]) if imports else "없음"
        sections.append(
            f"\n### {py.name}\n"
            f"- 이 파일은: {doc_line}\n"
            f"- 중요한 함수: {funcs_line}\n"
            f"- 사용하는 도구: {imports_line}\n"
            f"- 직접 해보기: `python {py.name}` 실행 후 결과를 읽어보세요.\n"
        )

    outro = (
        "\n## 한 줄 정리\n"
        "이 폴더의 코드는 데이터를 읽고, 계산하고, 결과를 보여주는 연습이에요.\n"
    )

    content = title + intro + "".join(sections) + outro
    (folder / "python_explain.md").write_text(content, encoding="utf-8")


def markdown_to_speech_text(md_text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", md_text)
    text = re.sub(r"#+\s*", "", text)
    text = text.replace("-", "")
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


async def write_mp3(md_file: Path) -> None:
    try:
        import edge_tts  # type: ignore
    except ImportError as exc:  # pragma: no cover - runtime guard
        raise RuntimeError("edge-tts is not installed. Run: pip install edge-tts") from exc

    text = markdown_to_speech_text(md_file.read_text(encoding="utf-8"))
    out = md_file.with_name("python_explain_ko_female.mp3")
    communicate = edge_tts.Communicate(text=text, voice=VOICE_NAME, rate="-8%")
    await communicate.save(str(out))


async def write_all_mp3(md_files: list[Path]) -> None:
    for md in md_files:
        await write_mp3(md)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["comments", "explain", "audio", "all", "reset"],
        default="all",
        help=(
            "처리 모드를 선택해요. "
            "reset: 기존 자동 주석을 제거하고 새 주석을 다시 생성해요."
        ),
    )
    args = parser.parse_args()

    py_files = find_python_files()
    folders = sorted({py.parent for py in py_files})

    if args.mode in {"comments", "all", "reset"}:
        do_reset = args.mode == "reset"
        changed = 0
        for py in py_files:
            if add_line_comments(py, reset=do_reset):
                changed += 1
        print(f"[comments] updated files: {changed}")

    if args.mode in {"explain", "all"}:
        for folder in folders:
            make_explain_md(folder)
        print(f"[explain] generated markdown files: {len(folders)}")

    if args.mode in {"audio", "all"}:
        md_files = [folder / "python_explain.md" for folder in folders if (folder / "python_explain.md").exists()]
        asyncio.run(write_all_mp3(md_files))
        print(f"[audio] generated mp3 files: {len(md_files)}")


if __name__ == "__main__":
    main()
