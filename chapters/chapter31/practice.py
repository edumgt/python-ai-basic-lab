# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""KNN 맛보기 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: 'sklearn.neighbors' 모듈에서 KNeighborsClassifier를(을) 불러와요.
from sklearn.neighbors import KNeighborsClassifier


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "가까운 점(이웃)을 기준으로 분류할 수 있다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "K 값을 바꿔 정확도가 어떻게 변하는지 비교한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    X = np.array(
        # 설명: 이 코드를 실행해요.
        [
            # 설명: 이 코드를 실행해요.
            [1.0, 1.1],
            # 설명: 이 코드를 실행해요.
            [1.2, 0.9],
            # 설명: 이 코드를 실행해요.
            [0.8, 1.0],
            # 설명: 이 코드를 실행해요.
            [3.8, 4.2],
            # 설명: 이 코드를 실행해요.
            [4.1, 3.9],
            # 설명: 이 코드를 실행해요.
            [3.9, 4.0],
            # 설명: 이 코드를 실행해요.
            [1.1, 1.3],
            # 설명: 이 코드를 실행해요.
            [4.0, 3.7],
            # 설명: 이 코드를 실행해요.
            [0.9, 1.2],
            # 설명: 이 코드를 실행해요.
            [4.2, 4.1],
            # 설명: 이 코드를 실행해요.
            [1.3, 1.0],
            # 설명: 이 코드를 실행해요.
            [3.7, 4.3],
        # 설명: 이 코드를 실행해요.
        ],
        # 설명: 'dtype' 변수에 값을 계산해서 저장해요.
        dtype=float,
    # 설명: 이 코드를 실행해요.
    )
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    y = np.array([0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1], dtype=int)

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.33, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'scores: dict[str, float]' 변수에 값을 계산해서 저장해요.
    scores: dict[str, float] = {}
    # 설명: 'best_k' 변수에 값을 계산해서 저장해요.
    best_k = 1
    # 설명: 'best_score' 변수에 값을 계산해서 저장해요.
    best_score = -1.0

    # 설명: 'range(1, 6)'의 각 원소를 'k'로 받으며 반복해요.
    for k in range(1, 6):
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = KNeighborsClassifier(n_neighbors=k)
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        model.fit(X_train, y_train)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = model.predict(X_test)
        # 설명: 평가 점수를 계산해서 저장해요.
        score = float(accuracy_score(y_test, pred))
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        scores[f"k={k}"] = round(score, 4)
        # 설명: 조건 (score > best_score)이 참인지 확인해요.
        if score > best_score:
            # 설명: 'best_score' 변수에 값을 계산해서 저장해요.
            best_score = score
            # 설명: 'best_k' 변수에 값을 계산해서 저장해요.
            best_k = k

    # 설명: 'best_model' 변수에 값을 계산해서 저장해요.
    best_model = KNeighborsClassifier(n_neighbors=best_k)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    best_model.fit(X_train, y_train)
    # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
    new_point = np.array([[1.05, 1.15]], dtype=float)
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    new_pred = int(best_model.predict(new_point)[0])

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter31",
        # 설명: 이 코드를 실행해요.
        "topic": "KNN 맛보기",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "k_scores": scores,
        # 설명: 이 코드를 실행해요.
        "best_k": best_k,
        # 설명: 값을 정수형으로 변환해요.
        "test_size": int(len(X_test)),
        # 설명: NumPy 배열을 파이썬 리스트로 변환해요.
        "new_point": new_point.flatten().round(2).tolist(),
        # 설명: 이 코드를 실행해요.
        "new_point_prediction": new_pred,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
