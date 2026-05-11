# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""하이퍼파라미터 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: make_classification를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split
# 설명: DecisionTreeClassifier를(을) 결정 트리 모델 도구를 불러와요.
from sklearn.tree import DecisionTreeClassifier


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "하이퍼파라미터는 사람이 정하는 설정값이며 성능에 큰 영향을 준다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "max_depth를 바꿔 성능 변화를 관찰한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
    X, y = make_classification(
        # 설명: 'n_samples' 변수에 값을 계산해서 저장해요.
        n_samples=280,
        # 설명: 'n_features' 변수에 값을 계산해서 저장해요.
        n_features=10,
        # 설명: 'n_informative' 변수에 값을 계산해서 저장해요.
        n_informative=6,
        # 설명: 'n_redundant' 변수에 값을 계산해서 저장해요.
        n_redundant=2,
        # 설명: 'random_state' 변수에 값을 계산해서 저장해요.
        random_state=42,
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'X, y, test_size' 변수에 값을 계산해서 저장해요.
        X, y, test_size=0.25, random_state=42, stratify=y
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'depth_options' 변수에 값을 계산해서 저장해요.
    depth_options = [2, 4, 6, None]
    # 설명: 'results: dict[str, float]' 변수에 값을 계산해서 저장해요.
    results: dict[str, float] = {}
    # 설명: 'best_depth: str | None' 변수에 값을 계산해서 저장해요.
    best_depth: str | None = None
    # 설명: 'best_score' 변수에 값을 계산해서 저장해요.
    best_score = -1.0

    # 설명: 'depth_options'의 각 원소를 'depth'로 받으며 반복해요.
    for depth in depth_options:
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = DecisionTreeClassifier(max_depth=depth, random_state=42)
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        model.fit(X_train, y_train)
        # 설명: 평가 점수를 계산해서 저장해요.
        score = float(accuracy_score(y_test, model.predict(X_test)))
        # 설명: 값을 문자열로 변환해요.
        key = "None" if depth is None else str(depth)
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        results[key] = round(score, 4)
        # 설명: 조건 (score > best_score)이 참인지 확인해요.
        if score > best_score:
            # 설명: 'best_score' 변수에 값을 계산해서 저장해요.
            best_score = score
            # 설명: 'best_depth' 변수에 값을 계산해서 저장해요.
            best_depth = key

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter56",
        # 설명: 이 코드를 실행해요.
        "topic": "하이퍼파라미터",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 이 코드를 실행해요.
        "accuracy_by_max_depth": results,
        # 설명: 이 코드를 실행해요.
        "best_max_depth": best_depth,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
