# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""개인정보와 보안 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "민감정보는 최소 수집하고, 저장 전 마스킹/비식별화를 적용해야 한다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "이메일과 전화번호를 마스킹해 안전한 출력 형태를 만든다."


# 설명: 'mask_email' 함수를 정의해요.
def mask_email(email: str) -> str:
    # 설명: 조건 ("@" not in email)이 참인지 확인해요.
    if "@" not in email:
        # 설명: '"***"'을(를) 함수 호출 측에 반환해요.
        return "***"
    # 설명: 'local, domain' 변수에 값을 계산해서 저장해요.
    local, domain = email.split("@", 1)
    # 설명: 조건 (len(local) <= 2)이 참인지 확인해요.
    if len(local) <= 2:
        # 설명: 'masked_local' 변수에 값을 계산해서 저장해요.
        masked_local = local[0] + "*"
    # 설명: 앞의 모든 조건이 거짓일 때 실행해요.
    else:
        # 설명: 시퀀스의 원소 개수를 반환해요.
        masked_local = local[:2] + "*" * (len(local) - 2)
    # 설명: 'f"{masked_local}@{domain}"'을(를) 함수 호출 측에 반환해요.
    return f"{masked_local}@{domain}"


# 설명: 'mask_phone' 함수를 정의해요.
def mask_phone(phone: str) -> str:
    # 설명: 'digits' 변수에 값을 계산해서 저장해요.
    digits = "".join(ch for ch in phone if ch.isdigit())
    # 설명: 조건 (len(digits) < 7)이 참인지 확인해요.
    if len(digits) < 7:
        # 설명: '"***"'을(를) 함수 호출 측에 반환해요.
        return "***"
    # 설명: 'f"{digits[:3]}-****-{digits[-4:]}"'을(를) 함수 호출 측에 반환해요.
    return f"{digits[:3]}-****-{digits[-4:]}"


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
    df = pd.DataFrame(
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "name": ["Mina", "Joon"],
            # 설명: 이 코드를 실행해요.
            "email": ["mina.choi@example.com", "joon.kim@example.com"],
            # 설명: 이 코드를 실행해요.
            "phone": ["010-1234-5678", "010-9876-5432"],
            # 설명: 이 코드를 실행해요.
            "score": [88, 92],
        # 설명: 이 코드를 실행해요.
        }
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'masked' 변수에 값을 계산해서 저장해요.
    masked = df.copy()
    # 설명: 'masked["email"]' 변수에 값을 계산해서 저장해요.
    masked["email"] = masked["email"].map(mask_email)
    # 설명: 'masked["phone"]' 변수에 값을 계산해서 저장해요.
    masked["phone"] = masked["phone"].map(mask_phone)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter96",
        # 설명: 이 코드를 실행해요.
        "topic": "개인정보와 보안",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: '"original_preview": df.to_dict(orient' 변수에 값을 계산해서 저장해요.
        "original_preview": df.to_dict(orient="records"),
        # 설명: '"masked_preview": masked.to_dict(orient' 변수에 값을 계산해서 저장해요.
        "masked_preview": masked.to_dict(orient="records"),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
