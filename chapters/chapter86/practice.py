# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""생성형 AI 개념 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 'collections' 모듈에서 defaultdict를(을) 불러와요.
from collections import defaultdict


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "생성형 AI는 정답 분류 대신 새로운 문장이나 이미지를 만들어 낸다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "아주 단순한 마코프 체인으로 문장 생성을 시도한다."


# 설명: '_build_bigram_model' 함수를 정의해요.
def _build_bigram_model(corpus: list[str]) -> dict[str, list[str]]:
    # 설명: 'model: dict[str, list[str]]' 변수에 값을 계산해서 저장해요.
    model: dict[str, list[str]] = defaultdict(list)
    # 설명: 'corpus'의 각 원소를 'sentence'로 받으며 반복해요.
    for sentence in corpus:
        # 설명: 'tokens' 변수에 값을 계산해서 저장해요.
        tokens = ["<START>"] + sentence.lower().split() + ["<END>"]
        # 설명: 각 원소를 순서대로 꺼내며 반복해요.
        for a, b in zip(tokens[:-1], tokens[1:]):
            # 설명: 이 코드를 실행해요.
            model[a].append(b)
    # 설명: 'model'을(를) 함수 호출 측에 반환해요.
    return model


# 설명: '_generate' 함수를 정의해요.
def _generate(model: dict[str, list[str]], max_len: int = 10) -> str:
    # 설명: 'token' 변수에 값을 계산해서 저장해요.
    token = "<START>"
    # 설명: 'output' 변수에 값을 계산해서 저장해요.
    output = []
    # 설명: 'range(max_len)'의 각 원소를 '_'로 받으며 반복해요.
    for _ in range(max_len):
        # 설명: 시퀀스를 정렬한 새 리스트를 반환해요.
        next_tokens = sorted(model.get(token, ["<END>"]))
        # 설명: 'next_token' 변수에 값을 계산해서 저장해요.
        next_token = next_tokens[0]
        # 설명: 조건 (next_token == "<END>")이 참인지 확인해요.
        if next_token == "<END>":
            # 설명: 현재 반복문을 즉시 탈출해요.
            break
        # 설명: 이 코드를 실행해요.
        output.append(next_token)
        # 설명: 'token' 변수에 값을 계산해서 저장해요.
        token = next_token
    # 설명: '" ".join(output)'을(를) 함수 호출 측에 반환해요.
    return " ".join(output)


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'corpus' 변수에 값을 계산해서 저장해요.
    corpus = [
        # 설명: 이 코드를 실행해요.
        "ai helps people learn",
        # 설명: 이 코드를 실행해요.
        "python helps people build",
        # 설명: 이 코드를 실행해요.
        "ai and python build projects",
    # 설명: 이 코드를 실행해요.
    ]

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = _build_bigram_model(corpus)
    # 설명: 'generated' 변수에 값을 계산해서 저장해요.
    generated = _generate(model, max_len=12)

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter86",
        # 설명: 이 코드를 실행해요.
        "topic": "생성형 AI 개념",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 시퀀스를 정렬한 새 리스트를 반환해요.
        "model_keys": sorted(model.keys()),
        # 설명: 이 코드를 실행해요.
        "generated_sentence": generated,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
