# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""시계열 입문 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "시계열 데이터는 시간 순서를 보존하고 흐름(추세)을 관찰해야 한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "이동평균으로 일별 값의 노이즈를 줄여 추세를 본다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 지정 범위의 정수 시퀀스를 생성해요.
            "date": pd.date_range("2026-02-01", periods=12, freq="D"),
            # 설명: 이 코드를 실행해요.
            "value": [10, 11, 13, 12, 15, 16, 18, 17, 19, 21, 20, 22],
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 이동 윈도우를 설정해 이동평균 등을 계산할 수 있어요.
    df["ma_3"] = df["value"].rolling(window=3).mean()
    # 설명: 'df["diff_1"]' 변수에 값을 계산해서 저장해요.
    df["diff_1"] = df["value"].diff()

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter84",
        # 설명: 이 코드를 실행해요.
        "topic": "시계열 입문",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 지정된 소수점 자릿수에서 반올림해요.
        "preview": df.head(8).round(3).astype(str).to_dict(orient="records"),
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "last_ma_3": round(float(df["ma_3"].iloc[-1]), 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
