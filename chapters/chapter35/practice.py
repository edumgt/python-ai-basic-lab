# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""원-핫 인코딩 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "범주형 값은 0/1 깃발 컬럼으로 안전하게 표현할 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "get_dummies로 색상과 동물 컬럼을 원-핫 인코딩한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "color": ["red", "blue", "green", "blue", "red"],
            # 설명: 이 코드를 실행해요.
            "animal": ["cat", "dog", "cat", "bird", "dog"],
            # 설명: 이 코드를 실행해요.
            "value": [10, 20, 12, 18, 16],
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 원-핫 인코딩된 0/1 행렬을 저장해요.
    encoded = pd.get_dummies(df, columns=["color", "animal"], dtype=int)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter35",
        # 설명: 이 코드를 실행해요.
        "topic": "원-핫 인코딩",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "original_columns": df.columns.tolist(),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "encoded_columns": encoded.columns.tolist(),
        # 설명: '"encoded_preview": encoded.to_dict(orient' 변수에 값을 계산해서 저장해요.
        "encoded_preview": encoded.to_dict(orient="records"),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
