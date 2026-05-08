# AI/ML 개발자용 Python 코드 예제 포함 확장판

이 문서는 수학 전공자가 아닌 IT 개발자를 기준으로, AI/ML의 핵심 개념을 **실행 가능한 Python 코드 예제**와 함께 설명합니다. 목표는 "수학 용어"를 "데이터 -> 코드 -> 결과" 흐름으로 이해하는 것입니다.

---

## 1. 가장 먼저 이해할 핵심 흐름

AI/ML은 아래 한 줄로 요약할 수 있습니다.

**입력 데이터를 넣고 -> 예측하고 -> 실제값과 비교해서 -> 덜 틀리게 수정한다.**

코드에서는 보통 아래 구조로 보입니다.

```python
# 1) 데이터 준비
X = df[["feature1", "feature2"]]
y = df["target"]

# 2) 모델 선택
model = SomeModel()

# 3) 학습
model.fit(X, y)

# 4) 예측
pred = model.predict(X)
```

---

## 2. 선형회귀: 숫자 예측의 가장 기본

### 개념
선형회귀(Linear Regression)는 **숫자**를 예측하는 가장 기본적인 모델입니다.

예:
- 광고비로 매출 예측
- 금리와 실업률로 집값 예측
- 어제 수익률과 거래량으로 내일 수익률 예측

수식은 다음과 같습니다.

```text
y_hat = w1*x1 + w2*x2 + ... + b
```

뜻:
- `x`: 입력값(feature)
- `w`: 각 입력의 영향력(weight)
- `b`: 기본값(bias, intercept)
- `y_hat`: 예측값(prediction)

### Python 예제

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 예시 데이터: 금리, 실업률, 소득 -> 주택가격
_df = pd.DataFrame({
    "interest_rate": [1.5, 1.7, 2.0, 2.2, 2.5, 2.7, 3.0, 3.2],
    "unemployment": [3.2, 3.4, 3.6, 3.8, 4.0, 4.1, 4.3, 4.5],
    "income": [4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900],
    "house_price": [52000, 51500, 50500, 49800, 49000, 48500, 47500, 46800]
})

X = _df[["interest_rate", "unemployment", "income"]]
y = _df["house_price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("coef:", dict(zip(X.columns, model.coef_)))
print("intercept:", model.intercept_)
print("MSE:", mean_squared_error(y_test, pred))
print("R2:", r2_score(y_test, pred))
```

### 개발자 관점 해석
- `X`: 입력 컬럼 묶음
- `y`: 정답 컬럼
- `coef_`: 각 컬럼의 영향력
- `intercept_`: 입력이 0일 때의 기본값
- `MSE`: 얼마나 틀렸는지 숫자로 측정
- `R2`: 설명력(1에 가까울수록 잘 맞음)

---

## 3. 로지스틱 회귀: 오를까 내릴까 같은 분류

### 개념
로지스틱 회귀(Logistic Regression)는 이름에 회귀가 들어가지만, 실제로는 **분류(Classification)** 에 많이 사용됩니다.

예:
- 내일 주가가 상승할까(1) / 하락할까(0)
- 고객이 이탈할까 / 유지할까
- 대출이 부실화될까 / 아닐까

### Python 예제

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 예시: 주식 상승/하락 예측용 간단 데이터
_df = pd.DataFrame({
    "return_1d": [0.01, -0.02, 0.015, -0.01, 0.005, 0.02, -0.03, 0.01, -0.005, 0.018],
    "volume_change": [0.10, 0.15, -0.05, 0.02, 0.03, 0.20, -0.10, 0.12, -0.03, 0.18],
    "ma_gap": [1.2, -0.8, 1.5, -1.0, 0.5, 2.0, -1.5, 1.1, -0.4, 1.8],
    "volatility": [0.8, 1.4, 0.9, 1.2, 0.7, 1.0, 1.6, 0.85, 1.1, 0.95],
    "target_up": [1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
})

X = _df[["return_1d", "volume_change", "ma_gap", "volatility"]]
y = _df["target_up"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))
print("상승 확률:", proba)
```

### 개발자 관점 해석
- `predict()`: 최종 라벨 반환 (0 또는 1)
- `predict_proba()`: 확률 반환
- 분류 문제는 `accuracy`, `precision`, `recall`, `f1-score`를 자주 봄

---

## 4. 의사결정트리: 규칙 기반 판단

### 개념
의사결정트리(Decision Tree)는 if-else 규칙처럼 데이터를 나눕니다.

예:
- 금리가 높고 소비심리가 낮으면 경기 위험
- 거래량 급증 + 변동성 확대면 과열 가능성

### Python 예제

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

_df = pd.DataFrame({
    "interest_rate": [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 2.2, 3.8, 1.8, 4.2],
    "consumer_sentiment": [110, 105, 98, 95, 90, 85, 102, 88, 108, 82],
    "manufacturing_index": [55, 53, 50, 48, 45, 43, 52, 44, 54, 41],
    "recession_risk": [0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
})

X = _df[["interest_rate", "consumer_sentiment", "manufacturing_index"]]
y = _df["recession_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print("Feature importance:", dict(zip(X.columns, model.feature_importances_)))
```

### 개발자 관점 해석
- 코드 리뷰 시 가장 읽기 쉬운 모델 중 하나
- `feature_importances_`로 어떤 입력이 중요한지 확인 가능
- 너무 깊게 두면 과적합되기 쉬움

---

## 5. 랜덤포레스트: 트리 여러 개의 앙상블

### 개념
랜덤포레스트(Random Forest)는 의사결정트리를 여러 개 만들어 투표/평균으로 판단합니다.

장점:
- 단일 트리보다 안정적
- 비선형 관계를 잘 잡음
- 기본 성능이 괜찮은 편

### Python 예제

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

_df = pd.DataFrame({
    "rsi": [35, 45, 60, 70, 30, 55, 65, 40, 25, 75, 50, 68],
    "macd": [-0.5, 0.1, 0.8, 1.2, -0.8, 0.5, 1.0, -0.1, -1.0, 1.4, 0.2, 0.9],
    "volume_change": [0.05, 0.02, 0.10, 0.15, -0.03, 0.08, 0.12, 0.01, -0.05, 0.20, 0.03, 0.11],
    "volatility": [1.2, 1.0, 0.9, 1.3, 1.5, 1.1, 0.8, 1.0, 1.6, 1.4, 1.0, 0.9],
    "target_up": [0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1]
})

X = _df[["rsi", "macd", "volume_change", "volatility"]]
y = _df["target_up"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print("Feature importance:", dict(zip(X.columns, model.feature_importances_)))
```

---

## 6. K-Means: 정답 없이 그룹 찾기

### 개념
K-Means는 라벨 없이 비슷한 것끼리 자동으로 묶는 **군집화** 알고리즘입니다.

예:
- 고객 세분화
- 투자자 유형 분리
- 제품 사용 패턴 그룹화

### Python 예제

```python
import pandas as pd
from sklearn.cluster import KMeans

_df = pd.DataFrame({
    "trade_count": [5, 8, 30, 35, 10, 40, 6, 32, 7, 45],
    "monthly_invest": [50, 80, 300, 350, 100, 400, 60, 320, 70, 420],
    "risk_score": [2, 3, 8, 9, 4, 10, 2, 8, 3, 9]
})

model = KMeans(n_clusters=3, random_state=42, n_init=10)
model.fit(_df)

_df["cluster"] = model.labels_
print(_df)
print("Centers:")
print(model.cluster_centers_)
```

### 개발자 관점 해석
- `labels_`: 각 row가 어느 군집에 속하는지
- `cluster_centers_`: 각 군집의 대표 중심값
- 정답 컬럼이 없어도 동작함

---

## 7. 평가 지표를 코드에서 읽는 법

### 회귀 지표
- `MSE`: 큰 오차에 더 민감
- `MAE`: 절대 오차 평균, 직관적
- `R2`: 설명력

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, pred)
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)
```

### 분류 지표
- `Accuracy`: 전체 중 맞춘 비율
- `Precision`: 맞다고 한 것 중 진짜 맞은 비율
- `Recall`: 실제 정답 중 찾아낸 비율
- `F1`: Precision / Recall 균형

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

acc = accuracy_score(y_test, pred)
prec = precision_score(y_test, pred)
rec = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)
```

---

## 8. 실무에서 꼭 조심할 것

### 1) 데이터 누수(Data Leakage)
미래 정보를 실수로 학습에 넣으면, 테스트 점수는 높아도 실전에서 망가집니다.

예:
- 내일 수익률을 예측하는데 내일 종가 정보가 feature에 들어감

### 2) 과적합(Overfitting)
학습 데이터만 너무 잘 외운 상태입니다.

증상:
- train 점수는 높은데 test 점수는 낮음

### 3) 검증 방식
주식/시계열 데이터는 `train_test_split`보다 **시간 순서 분리**가 더 적절합니다.

---



## 9. 신경망 모델: 가중치 행렬, 순전파, softmax

신경망(Neural Network)은 층(layer)마다 **행렬곱 + 활성화 함수**를 반복합니다.

```python
import numpy as np

X = np.array([[0.2, 0.1, 0.7, 0.0]])  # (batch, input_dim)
W1 = np.random.randn(4, 5) * 0.1       # (input_dim, hidden_dim)
b1 = np.zeros((1, 5))
W2 = np.random.randn(5, 3) * 0.1       # (hidden_dim, num_classes)
b2 = np.zeros((1, 3))

z1 = X @ W1 + b1
a1 = np.maximum(0, z1)                 # ReLU
logits = a1 @ W2 + b2

exp_scores = np.exp(logits - logits.max(axis=1, keepdims=True))
probs = exp_scores / exp_scores.sum(axis=1, keepdims=True)  # softmax
print(probs)
```

핵심 포인트:
- `W1`, `W2`가 바로 가중치 행렬입니다.
- 출력층에서 softmax를 쓰면 다중분류 확률을 만들 수 있습니다.

---

## 10. fitting: 크로스 엔트로피 + 역전파 + 경사하강법

`fit()` 내부에서는 아래 과정을 반복합니다.

```python
# y_one_hot: (batch, num_classes)
loss = -np.mean(np.sum(y_one_hot * np.log(probs + 1e-12), axis=1))

# backward(핵심 아이디어)
dlogits = (probs - y_one_hot) / X.shape[0]
dW2 = a1.T @ dlogits

# gradient descent update
W2 -= lr * dW2
```

핵심 포인트:
- 크로스 엔트로피는 정답 클래스 확률을 높이도록 학습시킵니다.
- 역전파는 각 가중치의 기울기(`dW`)를 계산합니다.
- 경사하강법은 `W = W - lr * dW`로 업데이트합니다.

---

## 11. CNN 핵심 아이디어(합성곱)

CNN은 이미지의 로컬 패턴(엣지, 질감)을 필터로 추출합니다.

```python
import numpy as np

patch = np.array([[1, 2, 0], [0, 1, 3], [2, 1, 0]])
kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])

conv_value = np.sum(patch * kernel)
print(conv_value)
```

핵심 포인트:
- 커널은 학습되는 작은 가중치 행렬입니다.
- CNN도 결국 `loss -> backward -> gradient descent` 흐름으로 학습됩니다.

---

## 12. 개발자 추천 학습 순서

1. 선형회귀: `y = wx + b`
2. 로지스틱 회귀: 분류 + 확률
3. 의사결정트리: 규칙 이해
4. 랜덤포레스트: 실전 기본기
5. K-Means: 비지도학습 감 잡기
6. 이후 XGBoost, LightGBM, 신경망 확장

---

## 13. 핵심 요약

- AI/ML은 결국 **입력 -> 예측 -> 오차 계산 -> 수정**의 반복입니다.
- 회귀는 숫자를 맞추고, 분류는 라벨을 맞춥니다.
- 코드에서는 `fit()`이 학습, `predict()`가 추론입니다.
- `coef_`, `feature_importances_`, `predict_proba()` 같은 속성을 읽을 수 있으면 문서 해석이 훨씬 쉬워집니다.
- 모델보다 먼저, **문제를 회귀/분류/군집화 중 무엇으로 볼지 정의하는 것**이 중요합니다.

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=python+ai+ml+ai+ml+python+examples+expanded+%EA%B0%95%EC%9D%98)
