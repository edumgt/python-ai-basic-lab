# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""AI 윤리와 편향 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "모델 성능뿐 아니라 집단별 결과 차이(편향)도 함께 봐야 한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "성별 집단별 승인율을 비교해 간단한 편향 지표를 계산한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "gender": ["F", "F", "F", "F", "M", "M", "M", "M", "M", "F"],
            # 설명: 이 코드를 실행해요.
            "pred_approve": [1, 1, 0, 1, 1, 0, 0, 0, 1, 0],
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 집단별 평균 비율을 계산해 딕셔너리로 저장해요.
    group_rate = df.groupby("gender")["pred_approve"].mean().to_dict()
    # 설명: 두 집단 간 비율 차이(공정성 지표)를 계산해요.
    parity_gap = abs(float(group_rate.get("F", 0.0)) - float(group_rate.get("M", 0.0)))

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter95",
        # 설명: 이 코드를 실행해요.
        "topic": "AI 윤리와 편향",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "approval_rate_by_gender": {k: round(float(v), 4) for k, v in group_rate.items()},
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "demographic_parity_gap": round(parity_gap, 4),
        # 설명: 이 코드를 실행해요.
        "note": "gap이 클수록 집단 간 결과 차이가 크므로 추가 점검이 필요하다.",
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
