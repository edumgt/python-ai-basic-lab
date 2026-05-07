# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""오류 처리와 안정성 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "입력 유효성 검사는 서비스 오류와 잘못된 예측을 줄인다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "숫자 범위와 타입 검증 함수를 구현한다."


# 설명: 'validate_payload' 함수를 정의해요.
def validate_payload(payload: dict) -> tuple[bool, str]:
    # 설명: 'required' 변수에 값을 계산해서 저장해요.
    required = ["study_minutes", "attendance_rate", "homework_done"]
    # 설명: 'required'의 각 원소를 'key'로 받으며 반복해요.
    for key in required:
        # 설명: 조건 (key not in payload)이 참인지 확인해요.
        if key not in payload:
            # 설명: 'False, f"missing field: {key}"'을(를) 함수 호출 측에 반환해요.
            return False, f"missing field: {key}"

    # 설명: 오류가 발생할 수 있는 코드를 시도(try)해요.
    try:
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        study = float(payload["study_minutes"])
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        attend = float(payload["attendance_rate"])
        # 설명: 값을 정수형으로 변환해요.
        homework = int(payload["homework_done"])
    # 설명: (TypeError, ValueError) 오류가 발생하면 여기서 안전하게 처리해요.
    except (TypeError, ValueError):
        # 설명: 'False, "type conversion failed"'을(를) 함수 호출 측에 반환해요.
        return False, "type conversion failed"

    # 설명: 조건 (not (0 <= study <= 600))이 참인지 확인해요.
    if not (0 <= study <= 600):
        # 설명: 'False, "study_minutes out of range"'을(를) 함수 호출 측에 반환해요.
        return False, "study_minutes out of range"
    # 설명: 조건 (not (0 <= attend <= 1))이 참인지 확인해요.
    if not (0 <= attend <= 1):
        # 설명: 'False, "attendance_rate out of range"'을(를) 함수 호출 측에 반환해요.
        return False, "attendance_rate out of range"
    # 설명: 조건 (homework not in (0, 1))이 참인지 확인해요.
    if homework not in (0, 1):
        # 설명: 'False, "homework_done must be 0 or 1"'을(를) 함수 호출 측에 반환해요.
        return False, "homework_done must be 0 or 1"

    # 설명: 'True, "ok"'을(를) 함수 호출 측에 반환해요.
    return True, "ok"


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'good' 변수에 값을 계산해서 저장해요.
    good = {"study_minutes": 45, "attendance_rate": 0.9, "homework_done": 1}
    # 설명: 'bad' 변수에 값을 계산해서 저장해요.
    bad = {"study_minutes": -3, "attendance_rate": 1.2, "homework_done": 2}

    # 설명: 'good_result' 변수에 값을 계산해서 저장해요.
    good_result = validate_payload(good)
    # 설명: 'bad_result' 변수에 값을 계산해서 저장해요.
    bad_result = validate_payload(bad)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter94",
        # 설명: 이 코드를 실행해요.
        "topic": "오류 처리와 안정성",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "good_payload_check": {"valid": good_result[0], "message": good_result[1]},
        # 설명: 이 코드를 실행해요.
        "bad_payload_check": {"valid": bad_result[0], "message": bad_result[1]},
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
