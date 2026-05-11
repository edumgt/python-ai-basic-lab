# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""날짜 데이터 다루기 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "날짜 하나에서 월, 요일, 주말 여부 같은 파생 정보를 만들 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "datetime 변환 후 파생 컬럼을 생성하고 요일별 평균을 구한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 지정 범위의 정수 시퀀스를 생성해요.
            "date": pd.date_range("2026-01-01", periods=14, freq="D").astype(str),
            # 설명: 이 코드를 실행해요.
            "sales": [120, 135, 128, 140, 150, 165, 158, 162, 170, 175, 168, 180, 190, 185],
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'df["date"]' 변수에 값을 계산해서 저장해요.
    df["date"] = pd.to_datetime(df["date"])
    # 설명: 'df["month"]' 변수에 값을 계산해서 저장해요.
    df["month"] = df["date"].dt.month
    # 설명: 'df["day_of_week"]' 변수에 값을 계산해서 저장해요.
    df["day_of_week"] = df["date"].dt.day_name()
    # 설명: 'df["is_weekend"]' 변수에 값을 계산해서 저장해요.
    df["is_weekend"] = (df["date"].dt.dayofweek >= 5).astype(int)

    # 설명: 'weekday_order' 변수에 값을 계산해서 저장해요.
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # 설명: 'df["day_of_week"]' 변수에 값을 계산해서 저장해요.
    df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=weekday_order, ordered=True)

    # 설명: 'by_weekday' 변수에 값을 계산해서 저장해요.
    by_weekday = (
        # 설명: 지정한 컬럼 값으로 데이터를 그룹화해요.
        df.groupby("day_of_week", observed=False)["sales"].mean().dropna().round(2).to_dict()
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'preview_cols' 변수에 값을 계산해서 저장해요.
    preview_cols = ["date", "sales", "month", "day_of_week", "is_weekend"]

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter40",
        # 설명: 이 코드를 실행해요.
        "topic": "날짜 데이터 다루기",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "derived_columns": ["month", "day_of_week", "is_weekend"],
        # 설명: 이 코드를 실행해요.
        "weekday_average_sales": by_weekday,
        # 설명: '"preview": df[preview_cols].head(7).astype(str).to_dict(orient' 변수에 값을 계산해서 저장해요.
        "preview": df[preview_cols].head(7).astype(str).to_dict(orient="records"),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
