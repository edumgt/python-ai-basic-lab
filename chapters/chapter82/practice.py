# [개발자 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""감성분석 맛보기 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: 'sklearn.feature_extraction.text' 모듈에서 CountVectorizer를(을) 불러와요.
from sklearn.feature_extraction.text import CountVectorizer
# 설명: LogisticRegression를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import LogisticRegression
# 설명: accuracy_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score
# 설명: train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import train_test_split


# 설명: 10분 요약 학습 내용을 상수 문자열로 정의해요.
LESSON_10MIN = "감성분석은 문장을 긍정/부정 라벨로 분류하는 문제다."
# 설명: 30분 실습 목표를 상수 문자열로 정의해요.
PRACTICE_30MIN = "작은 문장 데이터로 텍스트 분류기를 학습한다."


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 'texts' 변수에 값을 계산해서 저장해요.
    texts = [
        # 설명: 이 코드를 실행해요.
        "this movie is great",
        # 설명: 이 코드를 실행해요.
        "i love this song",
        # 설명: 이 코드를 실행해요.
        "what a wonderful day",
        # 설명: 이 코드를 실행해요.
        "this is terrible",
        # 설명: 이 코드를 실행해요.
        "i hate this",
        # 설명: 이 코드를 실행해요.
        "very bad service",
        # 설명: 이 코드를 실행해요.
        "excellent and fun",
        # 설명: 이 코드를 실행해요.
        "awful and boring",
    # 설명: 이 코드를 실행해요.
    ]
    # 설명: 'labels' 변수에 값을 계산해서 저장해요.
    labels = [1, 1, 1, 0, 0, 0, 1, 0]

    # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
    X_train, X_test, y_train, y_test = train_test_split(
        # 설명: 'texts, labels, test_size' 변수에 값을 계산해서 저장해요.
        texts, labels, test_size=0.25, random_state=42, stratify=labels
    # 설명: 이 코드를 실행해요.
    )

    # 설명: 'vectorizer' 변수에 값을 계산해서 저장해요.
    vectorizer = CountVectorizer()
    # 설명: 변환기(스케일러 등)를 학습하고 동시에 데이터를 변환해요.
    X_train_vec = vectorizer.fit_transform(X_train)
    # 설명: 이미 학습된 변환기로 데이터를 변환해요.
    X_test_vec = vectorizer.transform(X_test)

    # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
    model = LogisticRegression(max_iter=500, random_state=42)
    # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
    model.fit(X_train_vec, y_train)

    # 설명: 모델의 예측값을 pred 변수에 저장해요.
    pred = model.predict(X_test_vec)
    # 설명: 정답과 예측값을 비교해 정확도(0~1)를 계산해요.
    acc = float(accuracy_score(y_test, pred))

    # 설명: 'sample_text' 변수에 값을 계산해서 저장해요.
    sample_text = "this day is great"
    # 설명: 학습된 모델로 새 데이터에 대한 예측값을 계산해요.
    sample_pred = int(model.predict(vectorizer.transform([sample_text]))[0])

    # 설명: '{'을(를) 함수 호출 측에 반환해요.
    return {
        # 설명: 이 코드를 실행해요.
        "chapter": "chapter82",
        # 설명: 이 코드를 실행해요.
        "topic": "감성분석 맛보기",
        # 설명: 이 코드를 실행해요.
        "lesson_10min": LESSON_10MIN,
        # 설명: 이 코드를 실행해요.
        "practice_30min": PRACTICE_30MIN,
        # 설명: 값을 정수형으로 변환해요.
        "vocab_size": int(len(vectorizer.vocabulary_)),
        # 설명: 숫자를 지정한 소수점 자리에서 반올림해요.
        "test_accuracy": round(acc, 4),
        # 설명: 이 코드를 실행해요.
        "sample_text": sample_text,
        # 설명: 이 코드를 실행해요.
        "sample_prediction": sample_pred,
    # 설명: 이 코드를 실행해요.
    }


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
