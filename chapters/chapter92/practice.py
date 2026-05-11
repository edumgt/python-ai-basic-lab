# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""모델 배포 맛보기 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "학습 코드와 서비스 코드를 분리하면 운영 중 안정성을 높일 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "입력 JSON을 받아 예측값을 반환하는 API 계약을 설계한다."


# 설명: 'predict_pass' 함수를 정의해요.
def predict_pass(study_minutes: float, attendance_rate: float, homework_done: int) -> dict:
    # 간단한 규칙 기반 예측(배포 흐름 데모용)
    # 설명: 평가 점수를 계산해서 저장해요.
    score = 0.02 * study_minutes + 2.5 * attendance_rate + 0.8 * homework_done
    # 설명: 'prob' 변수에 값을 계산해서 저장해요.
    prob = min(max(score / 5.0, 0.0), 1.0)
    # 설명: 값을 정수형으로 변환해요.
    label = int(prob >= 0.5)
    # 설명: '{"probability": round(prob, 4), "label": label}'을(를) 함수 호출 측에 반환해요.
    return {"probability": round(prob, 4), "label": label}


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'sample_input' 변수에 값을 계산해서 저장해요.
    sample_input = {"study_minutes": 45.0, "attendance_rate": 0.9, "homework_done": 1}
    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = predict_pass(**sample_input)

    # 설명: 'api_contract' 변수에 값을 계산해서 저장해요.
    api_contract = {
        # 설명: 이 코드를 실행해요.
        "method": "POST",
        # 설명: 이 코드를 실행해요.
        "path": "/predict",
        # 설명: 이 코드를 실행해요.
        "request_json": {
            # 설명: 이 코드를 실행해요.
            "study_minutes": "float",
            # 설명: 이 코드를 실행해요.
            "attendance_rate": "float",
            # 설명: 값을 정수형으로 변환해요.
            "homework_done": "int(0 or 1)",
        # 설명: 이 코드를 실행해요.
        },
        # 설명: 이 코드를 실행해요.
        "response_json": {
            # 설명: 값을 부동소수점(실수)형으로 변환해요.
            "probability": "float(0~1)",
            # 설명: 값을 정수형으로 변환해요.
            "label": "int(0 or 1)",
        # 설명: 이 코드를 실행해요.
        },
    # 설명: 이 코드를 실행해요.
    }

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter92",
        # 설명: 이 코드를 실행해요.
        "topic": "모델 배포 맛보기",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "api_contract": api_contract,
        # 설명: 이 코드를 실행해요.
        "sample_input": sample_input,
        # 설명: 이 코드를 실행해요.
        "sample_prediction": pred,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
