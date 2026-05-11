# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""문자열 숫자로 바꾸기 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd
# 설명: LabelEncoder를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import LabelEncoder


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "모델은 텍스트를 직접 이해하지 못하므로 숫자로 변환해야 한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "라벨 인코딩으로 도시 이름을 정수로 바꾼다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "city": ["Seoul", "Busan", "Daegu", "Seoul", "Busan", "Incheon"],
            # 설명: 이 코드를 실행해요.
            "score": [88, 76, 91, 84, 79, 90],
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 시퀀스를 정렬한 새 리스트를 반환해요.
    categories = sorted(df["city"].unique())
    # 설명: 인덱스와 값을 쌍으로 반환하는 열거 이터레이터를 만들어요.
    manual_map = {name: idx for idx, name in enumerate(categories)}
    # 설명: 'df["city_manual_encoded"]' 변수에 값을 계산해서 저장해요.
    df["city_manual_encoded"] = df["city"].map(manual_map)

    # 설명: 문자열 레이블을 정수 인덱스로 변환하는 인코더를 생성해요.
    encoder = LabelEncoder()
    # 설명: 변환기(스케일러 등)를 학습하고 동시에 데이터를 변환해요.
    df["city_label_encoded"] = encoder.fit_transform(df["city"])

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter34",
        # 설명: 이 코드를 실행해요.
        "topic": "문자열 숫자로 바꾸기",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "manual_mapping": manual_map,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "label_encoder_classes": encoder.classes_.tolist(),
        # 설명: '"encoded_preview": df.head(6).to_dict(orient' 변수에 값을 계산해서 저장해요.
        "encoded_preview": df.head(6).to_dict(orient="records"),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
