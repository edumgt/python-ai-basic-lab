# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""추천시스템 감각 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "벡터 간 코사인 유사도로 취향이 비슷한 사용자나 아이템을 찾을 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "유사도 점수를 계산해 추천 후보를 만든다."


# 설명: 'cosine_similarity' 함수를 정의해요.
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    # 설명: 벡터 또는 행렬의 크기(놈, 유클리드 거리 등)를 계산해요.
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    # 설명: 'float(np.dot(a, b) / denom)'을(를) 함수 호출 측에 반환해요.
    return float(np.dot(a, b) / denom)


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 행: 사용자, 열: 아이템
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    ratings = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [5, 4, 0, 0, 1],
            # 설명: 이 코드를 실행해요.
            [4, 5, 1, 0, 1],
            # 설명: 이 코드를 실행해요.
            [0, 1, 5, 4, 0],
            # 설명: 이 코드를 실행해요.
            [0, 0, 4, 5, 1],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'target_user' 변수에 값을 계산해서 저장해요.
    target_user = 0
    # 설명: 'sims' 변수에 값을 계산해서 저장해요.
    sims = []
    # 설명: 'range(ratings.shape[0])'의 각 원소를 'u'로 받으며 반복해요.
    for u in range(ratings.shape[0]):
        # 설명: 조건 (u == target_user)이 참인지 확인해요.
        if u == target_user:
            # 설명: 이번 반복을 건너뛰고 다음 반복으로 넘어가요.
            continue
        # 설명: 이 코드를 실행해요.
        sims.append((u, cosine_similarity(ratings[target_user], ratings[u])))

    # 설명: 'sims.sort(key' 변수에 값을 계산해서 저장해요.
    sims.sort(key=lambda x: x[1], reverse=True)
    # 설명: 'nearest_user' 변수에 값을 계산해서 저장해요.
    nearest_user = sims[0][0]

    # target 사용자가 아직 안 본 아이템(0)을 nearest user 선호도로 추천
    # 설명: 조건이 참인 원소의 인덱스를 찾거나 조건부 값을 선택해요.
    unseen = np.where(ratings[target_user] == 0)[0]
    # 설명: 값을 정수형으로 변환해요.
    candidate_scores = {int(i): float(ratings[nearest_user, i]) for i in unseen}
    # 설명: 시퀀스를 정렬한 새 리스트를 반환해요.
    recommended_items = [k for k, _ in sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)]

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter83",
        # 설명: 이 코드를 실행해요.
        "topic": "추천시스템 감각",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 정수형으로 변환해요.
        "similarities": [{"user": int(u), "score": round(s, 4)} for u, s in sims],
        # 설명: 값을 정수형으로 변환해요.
        "nearest_user": int(nearest_user),
        # 설명: 이 코드를 실행해요.
        "recommended_item_indices": recommended_items,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
