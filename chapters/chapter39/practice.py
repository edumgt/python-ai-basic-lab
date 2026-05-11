# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""중복과 오탈자 정리 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "같은 데이터 중복과 오탈자를 정리하면 분석 품질이 올라간다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "replace와 drop_duplicates로 데이터 품질을 개선한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "name": ["Mina", "Mina", "Joon", "Sara", "Sara", "Noah", "Noah"],
            # 설명: 이 코드를 실행해요.
            "city": ["Seol", "Seol", "Busn", "Seoul", "Seoul", "Inchon", "Incheon"],
            # 설명: 이 코드를 실행해요.
            "score": [91, 91, 84, 88, 88, 79, 79],
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'typo_map' 변수에 값을 계산해서 저장해요.
    typo_map = {
        # 설명: 이 코드를 실행해요.
        "Seol": "Seoul",
        # 설명: 이 코드를 실행해요.
        "Busn": "Busan",
        # 설명: 이 코드를 실행해요.
        "Inchon": "Incheon",
    # 설명: 이 코드를 실행해요.
    }

    # 설명: 'cleaned' 변수에 값을 계산해서 저장해요.
    cleaned = df.copy()
    # 설명: 'cleaned["city"]' 변수에 값을 계산해서 저장해요.
    cleaned["city"] = cleaned["city"].replace(typo_map)
    # 설명: 'cleaned' 변수에 값을 계산해서 저장해요.
    cleaned = cleaned.drop_duplicates(subset=["name", "city", "score"], keep="first")

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter39",
        # 설명: 이 코드를 실행해요.
        "topic": "중복/오탈자 정리",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 정수형으로 변환해요.
        "rows_before": int(len(df)),
        # 설명: 값을 정수형으로 변환해요.
        "rows_after": int(len(cleaned)),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "city_values_before": sorted(df["city"].unique().tolist()),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "city_values_after": sorted(cleaned["city"].unique().tolist()),
        # 설명: '"cleaned_preview": cleaned.to_dict(orient' 변수에 값을 계산해서 저장해요.
        "cleaned_preview": cleaned.to_dict(orient="records"),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
