# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""K-Means 맛보기 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: KMeans를(을) K-Means 등 비지도 군집화 도구를 불러와요.
from sklearn.cluster import KMeans


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "정답 라벨이 없어도 비슷한 데이터끼리 묶을 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "2차원 점을 3개 그룹으로 나누고 중심점을 확인한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    X = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [1.0, 1.1],
            # 설명: 이 코드를 실행해요.
            [0.9, 1.0],
            # 설명: 이 코드를 실행해요.
            [1.2, 1.3],
            # 설명: 이 코드를 실행해요.
            [5.0, 5.1],
            # 설명: 이 코드를 실행해요.
            [4.8, 5.0],
            # 설명: 이 코드를 실행해요.
            [5.2, 4.9],
            # 설명: 이 코드를 실행해요.
            [8.5, 1.2],
            # 설명: 이 코드를 실행해요.
            [8.8, 1.0],
            # 설명: 이 코드를 실행해요.
            [8.2, 1.3],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = KMeans(n_clusters=3, random_state=42, n_init="auto")
    # 설명: 'labels' 변수에 값을 계산해서 저장해요.
    labels = model.fit_predict(X)

    # 설명: 'cluster_counts' 변수에 값을 계산해서 저장해요.
    cluster_counts = {
        # 설명: 합계를 계산해요.
        str(cluster_id): int((labels == cluster_id).sum())
        # 설명: 각 원소를 순서대로 꺼내며 반복해요.
        for cluster_id in sorted(np.unique(labels))
    # 설명: 이 코드를 실행해요.
    }

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter32",
        # 설명: 이 코드를 실행해요.
        "topic": "K-Means 맛보기",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "labels": labels.tolist(),
        # 설명: 이 코드를 실행해요.
        "cluster_counts": cluster_counts,
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "centers": model.cluster_centers_.round(3).tolist(),
        # 설명: 값을 부동소수점(실수)형으로 변환해요.
        "inertia": round(float(model.inertia_), 4),
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
