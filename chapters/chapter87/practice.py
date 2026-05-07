# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""프롬프트 기초 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "좋은 프롬프트는 역할, 목표, 형식, 제약을 명확히 담는다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "같은 작업을 3가지 프롬프트로 비교하고 구조 점수를 확인한다."


# 설명: '_prompt_score' 함수를 정의해요.
def _prompt_score(prompt: str) -> int:
    # 설명: 'p' 변수에 값을 계산해서 저장해요.
    p = prompt.lower()
    # 설명: 평가 점수를 계산해서 저장해요.
    score = 0
    # 설명: 조건 ("role" in p or "역할" in p)이 참인지 확인해요.
    if "role" in p or "역할" in p:
        # 설명: 'score +' 변수에 값을 계산해서 저장해요.
        score += 1
    # 설명: 조건 ("goal" in p or "목표" in p)이 참인지 확인해요.
    if "goal" in p or "목표" in p:
        # 설명: 'score +' 변수에 값을 계산해서 저장해요.
        score += 1
    # 설명: 조건 ("format" in p or "형식" in p)이 참인지 확인해요.
    if "format" in p or "형식" in p:
        # 설명: 'score +' 변수에 값을 계산해서 저장해요.
        score += 1
    # 설명: 조건 ("limit" in p or "제약" in p)이 참인지 확인해요.
    if "limit" in p or "제약" in p:
        # 설명: 'score +' 변수에 값을 계산해서 저장해요.
        score += 1
    # 설명: 'score'을(를) 함수 호출 측에 반환해요.
    return score


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'prompts' 변수에 값을 계산해서 저장해요.
    prompts = {
        # 설명: 이 코드를 실행해요.
        "basic": "서울 맛집 알려줘",
        # 설명: 이 코드를 실행해요.
        "better": "역할: 여행 가이드. 목표: 서울 점심 맛집 3개 추천. 형식: 표.",
        # 설명: 이 코드를 실행해요.
        "best": "역할: 여행 가이드. 목표: 서울 점심 맛집 3개 추천. 형식: 표(이름/메뉴/가격). 제약: 1인 2만원 이하, 2026년 기준 인기 지역 중심.",
    # 설명: 이 코드를 실행해요.
    }

    # 설명: 평가 점수를 계산해서 저장해요.
    scored = [
        # 설명: 이 코드를 실행해요.
        {
            # 설명: 이 코드를 실행해요.
            "label": name,
            # 설명: 이 코드를 실행해요.
            "score": _prompt_score(text),
            # 설명: 이 코드를 실행해요.
            "prompt": text,
        # 설명: 이 코드를 실행해요.
        }
        # 설명: 각 원소를 순서대로 꺼내며 반복해요.
        for name, text in prompts.items()
    # 설명: 이 코드를 실행해요.
    ]

    # 설명: 'scored.sort(key' 변수에 값을 계산해서 저장해요.
    scored.sort(key=lambda x: x["score"], reverse=True)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter87",
        # 설명: 이 코드를 실행해요.
        "topic": "프롬프트 기초",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "ranked_prompts": scored,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
