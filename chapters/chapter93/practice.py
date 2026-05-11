# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""프론트 연동 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "프론트와 백엔드는 JSON 요청/응답 규칙으로 연결된다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "fetch 예시를 만들고 요청 페이로드를 검증한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'payload' 변수에 값을 계산해서 저장해요.
    payload = {"study_minutes": 40, "attendance_rate": 0.85, "homework_done": 1}

    # 설명: 'fetch_example' 변수에 값을 계산해서 저장해요.
    fetch_example = (
        # 설명: 이 코드를 실행해요.
        "fetch('/predict', {method: 'POST', headers: {'Content-Type': 'application/json'}, "
        # 설명: 이 코드를 실행해요.
        "body: JSON.stringify(payload)})"
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'flow' 변수에 값을 계산해서 저장해요.
    flow = [
        # 설명: 이 코드를 실행해요.
        "1) 프론트에서 입력값 수집",
        # 설명: 이 코드를 실행해요.
        "2) JSON으로 /predict 요청",
        # 설명: 이 코드를 실행해요.
        "3) 백엔드가 probability/label 반환",
        # 설명: 이 코드를 실행해요.
        "4) 프론트에서 결과를 화면에 렌더링",
    # 설명: 이 코드를 실행해요.
    ]

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter93",
        # 설명: 이 코드를 실행해요.
        "topic": "프론트 연동",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "payload": payload,
        # 설명: 이 코드를 실행해요.
        "fetch_example": fetch_example,
        # 설명: 이 코드를 실행해요.
        "integration_flow": flow,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
