# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""텍스트 데이터 입문 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 'collections' 모듈에서 Counter를(을) 불러와요.
from collections import Counter


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "문장을 단어 단위로 나누면 숫자 벡터(빈도)로 바꿀 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "단어 사전을 만들고 문장별 카운트 벡터를 생성한다."


# 설명: '_tokenize' 함수를 정의해요.
def _tokenize(text: str) -> list[str]:
    # 설명: 'text.lower().replace(".", "").replace("!", "").split()'을(를) 함수 호출 측에 반환해요.
    return text.lower().replace(".", "").replace("!", "").split()


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'sentences' 변수에 값을 계산해서 저장해요.
    sentences = [
        # 설명: 이 코드를 실행해요.
        "AI class is fun",
        # 설명: 이 코드를 실행해요.
        "Python class is fun",
        # 설명: 이 코드를 실행해요.
        "AI and Python are useful",
    # 설명: 이 코드를 실행해요.
    ]

    # 설명: 'tokenized' 변수에 값을 계산해서 저장해요.
    tokenized = [_tokenize(s) for s in sentences]
    # 설명: 시퀀스를 정렬한 새 리스트를 반환해요.
    vocab = sorted({token for sent in tokenized for token in sent})

    # 설명: 'vectors' 변수에 값을 계산해서 저장해요.
    vectors = []
    # 설명: 'tokenized'의 각 원소를 'sent'로 받으며 반복해요.
    for sent in tokenized:
        # 설명: 'cnt' 변수에 값을 계산해서 저장해요.
        cnt = Counter(sent)
        # 설명: 이 코드를 실행해요.
        vectors.append([cnt[word] for word in vocab])

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter81",
        # 설명: 이 코드를 실행해요.
        "topic": "텍스트 데이터 입문",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "vocab": vocab,
        # 설명: 이 코드를 실행해요.
        "count_vectors": vectors,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
