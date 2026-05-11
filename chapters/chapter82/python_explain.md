# Python 쉬운 설명 (chapter82)

이 문서는 개발자도 따라할 수 있도록, 폴더 안 Python 파일을 아주 쉽게 설명해요.

## 먼저 기억해요
- `python 파일이름.py` 로 실행해요.
- 에러가 나면 메시지를 읽고 천천히 한 줄씩 확인해요.
- `run()` 함수가 있으면 그 함수가 핵심 실습이에요.

---

## 🧠 감성분석(Sentiment Analysis)이란?

**감성분석**은 텍스트(문장, 리뷰 등)를 읽고 그 감정이 **긍정(Positive)** 인지 **부정(Negative)** 인지 자동으로 분류하는 NLP 기술이에요.

| 문장 예시 | 감성 |
|---|---|
| "this movie is great" | 😊 긍정 (1) |
| "i hate this" | 😠 부정 (0) |
| "excellent and fun" | 😊 긍정 (1) |
| "very bad service" | 😠 부정 (0) |

실제로 쇼핑몰 상품 리뷰 분석, 영화 평점 예측, SNS 여론 분석 등에 널리 쓰여요.

---

## 📖 핵심 개념 이해하기

### 1. 텍스트 분류 파이프라인 전체 흐름

감성분석은 다음 3단계로 진행돼요:

```
[원본 텍스트] → [벡터화(숫자로 변환)] → [분류 모델 학습] → [새 문장 예측]
```

### 2. CountVectorizer — sklearn의 자동 벡터화 도구

chapter81에서 직접 만들었던 카운트 벡터를 scikit-learn이 자동으로 만들어줘요.

```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)  # 학습: 단어 사전 구축 + 벡터 변환
X_test_vec = vectorizer.transform(X_test)         # 변환만: 이미 만든 사전 사용
```

> ⚠️ **중요**: `fit_transform`은 학습 데이터에만, `transform`은 테스트 데이터에만 써야 해요.
> 테스트 데이터로 `fit`을 하면 **데이터 누수(data leakage)** 가 발생해요!

### 3. LogisticRegression — 텍스트 분류에 적합한 선형 모델

이름에 "Regression(회귀)"가 들어가지만, **분류 문제**에도 자주 써요.
입력(단어 벡터)을 받아 각 클래스(긍정/부정)일 확률을 계산하고, 더 높은 쪽으로 분류해요.

```
입력 벡터 [1, 0, 1, 0, 1, ...]
        ↓ 선형 계산
확률: 긍정=0.85, 부정=0.15
        ↓ 예측
결과: 긍정(1)
```

텍스트처럼 특성(feature)이 많고 희소(sparse)한 데이터에 잘 작동해요.

### 4. train_test_split — 데이터 분리

전체 데이터를 **학습용(train)** 과 **테스트용(test)** 으로 나눠요.
- `test_size=0.25` → 전체의 25%를 테스트에 사용
- `stratify=labels` → 긍정/부정 비율이 train/test에서 동일하게 유지

---

## 파일별 설명

### practice.py
- 이 파일은: 감성분석 맛보기 실습 파일
- 중요한 함수: `run`
- 사용하는 도구: `__future__`, `sklearn.feature_extraction.text`, `sklearn.linear_model`, `sklearn.metrics`, `sklearn.model_selection`
- 직접 해보기: `python practice.py` 실행 후 결과를 읽어보세요.

#### 코드 흐름 단계별 설명

**① 데이터 준비 — 문장과 라벨(정답)**
```python
texts  = ["this movie is great", "i hate this", ...]  # 입력 문장
labels = [1, 1, 1, 0, 0, 0, 1, 0]                     # 1=긍정, 0=부정
```

**② 데이터 분리 — 학습/테스트 나누기**
```python
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=42, stratify=labels
)
```

**③ 벡터화 — 문장을 숫자 배열로 변환**
```python
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)  # 학습 데이터로 사전 만들고 변환
X_test_vec  = vectorizer.transform(X_test)        # 테스트 데이터는 변환만
```

**④ 모델 학습**
```python
model = LogisticRegression(max_iter=500, random_state=42)
model.fit(X_train_vec, y_train)
```
`max_iter=500`: 모델 최적화 반복 횟수 상한선 (작으면 학습이 덜 될 수 있어요)

**⑤ 예측 및 평가**
```python
pred = model.predict(X_test_vec)
acc  = accuracy_score(y_test, pred)  # 정확도 계산
```

**⑥ 새 문장 예측 — 실제 사용 예시**
```python
sample_text = "this day is great"
sample_pred = model.predict(vectorizer.transform([sample_text]))[0]
# → 1 (긍정)
```

---

## 🔑 감성분석에서 기억해야 할 것들

| 개념 | 설명 |
|---|---|
| **CountVectorizer** | 문장을 단어 등장 횟수 벡터로 자동 변환 |
| **fit vs transform** | `fit`은 학습 데이터로만, `transform`은 테스트에도 적용 |
| **LogisticRegression** | 고차원 희소 벡터 분류에 잘 맞는 선형 모델 |
| **accuracy_score** | 전체 중 맞게 예측한 비율 (0~1) |

---

## 한 줄 정리
문장을 CountVectorizer로 숫자 벡터로 바꾸고, LogisticRegression 모델로 긍정/부정을 학습하면 새 문장의 감성을 자동으로 예측할 수 있어요.

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=python+ai+basic+lab+chapter82+%EC%84%A4%EB%AA%85)
