# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""실험 기록 자동화 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: Path를(을) 파일·디렉토리 경로를 객체로 다루는 pathlib 도구를 불러와요.
from pathlib import Path

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent / "data"


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "실험 결과를 구조적으로 기록하면 재현성과 협업 품질이 올라간다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "모델, 파라미터, 지표를 CSV로 저장한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 딕셔너리·리스트 등을 Pandas 표(DataFrame)로 만들어요.
    logs = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: '{"run_id": "run_001", "model": "logistic", "params": "C' 변수에 값을 계산해서 저장해요.
            {"run_id": "run_001", "model": "logistic", "params": "C=1.0", "accuracy": 0.81, "f1": 0.79},
            # 설명: '{"run_id": "run_002", "model": "logistic", "params": "C' 변수에 값을 계산해서 저장해요.
            {"run_id": "run_002", "model": "logistic", "params": "C=3.0", "accuracy": 0.83, "f1": 0.81},
            # 설명: '{"run_id": "run_003", "model": "random_forest", "params": "n' 변수에 값을 계산해서 저장해요.
            {"run_id": "run_003", "model": "random_forest", "params": "n=120", "accuracy": 0.86, "f1": 0.84},
        # 설명: 이 코드를 실행해요.
        ]
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 출력 결과를 저장할 배열을 초기화해요.
    out_path = DATA_DIR / "experiment_log.csv"
    # 설명: 'logs.to_csv(out_path, index' 변수에 값을 계산해서 저장해요.
    logs.to_csv(out_path, index=False, encoding="utf-8")

    # 설명: 'best_row' 변수에 값을 계산해서 저장해요.
    best_row = logs.sort_values("f1", ascending=False).iloc[0].to_dict()

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter91",
        # 설명: 이 코드를 실행해요.
        "topic": "실험 기록 자동화",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 문자열로 변환해요.
        "saved_path": str(out_path),
        # 설명: 값을 정수형으로 변환해요.
        "rows_saved": int(len(logs)),
        # 설명: 이 코드를 실행해요.
        "best_by_f1": best_row,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
