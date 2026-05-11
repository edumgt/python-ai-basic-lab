# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""미니 복습 프로젝트 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

from pathlib import Path

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd

DATA_DIR = Path(__file__).parent.parent.parent / "data"


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "응용 문제는 데이터 형태(이미지/텍스트/시계열)에 맞는 접근을 선택하는 것이 핵심이다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "시계열 미니 데모를 선택해 이동평균 기반 간단 리포트를 만든다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 미니 데모 선택: 시계열
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.read_csv(DATA_DIR / "traffic_timeseries.csv", parse_dates=["date"])

    # 설명: 이동 윈도우를 설정해 이동평균 등을 계산할 수 있어요.
    df["ma_3"] = df["traffic"].rolling(3).mean()
    # 설명: 'df["trend"]' 변수에 값을 계산해서 저장해요.
    df["trend"] = (df["traffic"].diff() > 0).map({True: "up", False: "down_or_same"})

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter88",
        # 설명: 이 코드를 실행해요.
        "topic": "미니 복습 프로젝트",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "selected_domain": "time_series",
        # 설명: 값을 정수형으로 변환해요.
        "last_traffic": int(df["traffic"].iloc[-1]),
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "last_ma_3": round(float(df["ma_3"].iloc[-1]), 4),
        # 설명: '"preview": df.tail(5).astype(str).to_dict(orient' 변수에 값을 계산해서 저장해요.
        "preview": df.tail(5).astype(str).to_dict(orient="records"),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
