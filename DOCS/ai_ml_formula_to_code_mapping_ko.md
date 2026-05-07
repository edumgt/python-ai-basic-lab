# AI/ML 개발자용 수식 -> 코드 대응표

이 문서는 AI/ML 문서에서 자주 보이는 수식을 **개발자 기준으로 코드와 연결**해서 해석할 수 있게 정리한 문서입니다.

---

## 1. 가장 기본 번역 원칙

수학 문서에서 보이는 식은 보통 아래 3가지 역할 중 하나입니다.

1. **모델 식**: 입력으로 어떻게 예측값을 만드는가
2. **손실 식**: 얼마나 틀렸는가
3. **업데이트 식**: 어떻게 덜 틀리게 고칠 것인가

즉, 대부분의 AI 수식은 다음 흐름입니다.

```text
입력 -> 모델 식 -> 예측값 -> 손실 식 -> 기울기 -> 업데이트 식
```

---

## 2. 선형회귀 식

### 수식

```text
y_hat = w*x + b
```

### 의미
- `x`: 입력값
- `w`: 가중치(weight)
- `b`: 절편(bias/intercept)
- `y_hat`: 예측값(prediction)

### Python 대응

```python
x = 3.0
w = 2.0
b = 1.0

y_hat = w * x + b
print(y_hat)  # 7.0
```

### scikit-learn 대응

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

# 내부적으로는 대략 y_hat = w1*x1 + w2*x2 + ... + b 형태
print(model.coef_)      # w
print(model.intercept_) # b
```

---

## 3. 다중선형회귀 식

### 수식

```text
y_hat = w1*x1 + w2*x2 + w3*x3 + b
```

### 의미
입력이 여러 개일 때, 각 입력에 가중치를 곱해 더한 뒤 기본값을 더합니다.

### Python 대응

```python
x1, x2, x3 = 1.5, 3.0, 10.0
w1, w2, w3 = 2.0, -1.0, 0.5
b = 4.0

y_hat = w1*x1 + w2*x2 + w3*x3 + b
print(y_hat)
```

### NumPy 대응

```python
import numpy as np

x = np.array([1.5, 3.0, 10.0])
w = np.array([2.0, -1.0, 0.5])
b = 4.0

y_hat = np.dot(w, x) + b
print(y_hat)
```

### 개발자 메모
- 이 식은 사실상 **가중합(weighted sum)** 입니다.
- 신경망의 기본 계산도 이 구조에서 시작합니다.

---

## 4. 오차(Error)

### 수식

```text
error = y - y_hat
```

### 의미
- `y`: 실제값
- `y_hat`: 예측값
- `error`: 실제와 예측의 차이

### Python 대응

```python
y = 100
y_hat = 92

error = y - y_hat
print(error)  # 8
```

---

## 5. 평균제곱오차(MSE)

### 수식

```text
MSE = (1/n) * Σ (y - y_hat)^2
```

### 의미
오차를 제곱해서 평균낸 값입니다.
큰 오차를 더 크게 벌줍니다.

### Python 대응

```python
actual = [100, 120, 90]
pred = [95, 125, 80]

errors = [(a - p) ** 2 for a, p in zip(actual, pred)]
mse = sum(errors) / len(errors)
print(mse)
```

### scikit-learn 대응

```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_test, pred)
print(mse)
```

---

## 6. 평균절대오차(MAE)

### 수식

```text
MAE = (1/n) * Σ |y - y_hat|
```

### 의미
오차의 절댓값 평균입니다.
MSE보다 이상치에 덜 민감합니다.

### Python 대응

```python
actual = [100, 120, 90]
pred = [95, 125, 80]

errors = [abs(a - p) for a, p in zip(actual, pred)]
mae = sum(errors) / len(errors)
print(mae)
```

---

## 7. 기울기(Gradient)

### 수식 개념

```text
∂L/∂w
```

### 의미
- `L`: 손실(loss)
- `w`: 가중치
- `∂L/∂w`: 가중치를 조금 바꾸면 손실이 얼마나 변하는가

### 개발자 해석
이 값은 **"w를 어느 방향으로, 얼마나 바꿔야 하는가"** 를 알려줍니다.

### Python 감각 예시

```python
# 실제 자동미분 없이 개념만 보는 예시
w = 2.0
grad = 0.8   # 손실 기준 기울기라고 가정
lr = 0.1

w = w - lr * grad
print(w)  # 1.92
```

---

## 8. 경사하강법(Gradient Descent)

### 수식

```text
w := w - alpha * (∂L/∂w)
```

### 의미
- `alpha`: 학습률(learning rate)
- 기울기 방향의 반대로 조금 이동해서 손실을 줄입니다.

### Python 대응

```python
w = 5.0
lr = 0.01
grad = 2.5

w = w - lr * grad
print(w)
```

### 개발자 메모
- `:=` 는 "업데이트한다"는 뜻으로 읽으면 됩니다.
- 딥러닝 프레임워크에서 optimizer가 이 작업을 대신 수행합니다.

---

## 9. 시그모이드 함수

### 수식

```text
sigma(z) = 1 / (1 + e^(-z))
```

### 의미
임의의 숫자 `z`를 0과 1 사이의 확률처럼 바꾸는 함수입니다.

### Python 대응

```python
import math

z = 1.2
sigmoid = 1 / (1 + math.exp(-z))
print(sigmoid)
```

### 개발자 메모
- 로지스틱 회귀에서 확률 계산에 사용
- 딥러닝에서는 출력층 또는 일부 활성화함수로 사용

---

## 10. 로지스틱 회귀의 예측 확률

### 수식

```text
p = sigma(w*x + b)
```

### 의미
선형식의 결과를 시그모이드에 넣어, 확률처럼 해석 가능한 값으로 바꿉니다.

### Python 대응

```python
import math

x = 2.0
w = 1.5
b = -0.5

z = w * x + b
p = 1 / (1 + math.exp(-z))
print(p)
```

### scikit-learn 대응

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)

proba = model.predict_proba(X_test)[:, 1]
print(proba)
```

---

## 11. 정확도(Accuracy)

### 수식

```text
Accuracy = 맞춘 개수 / 전체 개수
```

### Python 대응

```python
actual = [1, 0, 1, 1]
pred = [1, 0, 0, 1]

correct = sum(1 for a, p in zip(actual, pred) if a == p)
accuracy = correct / len(actual)
print(accuracy)
```

### scikit-learn 대응

```python
from sklearn.metrics import accuracy_score

acc = accuracy_score(y_test, pred)
print(acc)
```

---

## 12. 벡터와 내적

### 수식

```text
z = w · x + b
```

### 의미
- `·` 는 내적(dot product)
- 벡터끼리 곱해서 하나의 숫자를 만들고, 거기에 bias를 더함

### Python 대응

```python
import numpy as np

w = np.array([0.5, 1.2, -0.3])
x = np.array([10, 2, 4])
b = 0.7

z = np.dot(w, x) + b
print(z)
```

### 개발자 메모
- 선형회귀, 로지스틱 회귀, 신경망 Dense Layer 전부 이 형태를 기반으로 함

---

## 13. 행렬곱

### 수식

```text
Y = XW + b
```

### 의미
여러 샘플(X)에 대해 한 번에 계산하는 형태입니다.

### Python 대응

```python
import numpy as np

X = np.array([
    [1.0, 2.0],
    [3.0, 4.0],
])
W = np.array([
    [0.5],
    [1.5],
])
b = np.array([0.2])

Y = X @ W + b
print(Y)
```

### 개발자 메모
- `@` 는 Python의 행렬곱 연산자
- 딥러닝 프레임워크 문서에서 매우 자주 등장

---

## 14. 확률과 로그 손실(Cross Entropy 감각)

### 수식 개념

```text
Loss = -[y*log(p) + (1-y)*log(1-p)]
```

### 의미
분류 문제에서 정답 확률을 높이도록 유도하는 손실 함수입니다.

### Python 대응

```python
import math

y = 1       # 실제 정답
p = 0.9     # 모델이 예측한 정답 확률

loss = -(y * math.log(p) + (1 - y) * math.log(1 - p))
print(loss)
```

### 개발자 메모
- 정답인데 확률을 낮게 주면 손실이 크게 증가
- 분류 모델 학습의 핵심 기준 중 하나

---

## 15. 정규화(Regularization) 감각

### 수식 개념

```text
Loss_total = Loss + lambda * penalty
```

### 의미
원래 손실에 패널티를 더해, 모델이 너무 복잡해지는 것을 막습니다.

### 개발자 해석
- 과적합 방지
- weight가 지나치게 커지지 않도록 제어

### scikit-learn 힌트

```python
from sklearn.linear_model import Ridge, Lasso

ridge = Ridge(alpha=1.0)  # L2 정규화 계열
lasso = Lasso(alpha=1.0)  # L1 정규화 계열
```

---



## 16. 소프트맥스(Softmax)

### 수식

```text
softmax(z_i) = exp(z_i) / Σ exp(z_j)
```

### 의미
여러 클래스 점수(logit)를 **합이 1인 확률 분포**로 바꿉니다.

### Python 대응

```python
import numpy as np

logits = np.array([2.2, 0.3, -1.0])
exp_scores = np.exp(logits - np.max(logits))
probs = exp_scores / exp_scores.sum()
print(probs, probs.sum())
```

---

## 17. 다중분류 크로스 엔트로피

### 수식

```text
Loss = - Σ y_i * log(p_i)
```

### 의미
- `y_i`: 원-핫 정답 벡터
- `p_i`: softmax 확률
- 정답 클래스 확률이 낮을수록 손실이 커집니다.

### Python 대응

```python
import numpy as np

y_one_hot = np.array([0, 1, 0])
p = np.array([0.1, 0.8, 0.1])
loss = -np.sum(y_one_hot * np.log(p + 1e-12))
print(loss)
```

---

## 18. 순전파(Forward)와 역전파(Backward)

### 순전파 수식

```text
z1 = XW1 + b1
a1 = ReLU(z1)
z2 = a1W2 + b2
p = softmax(z2)
```

### 역전파 핵심 식

```text
dz2 = p - y

dW2 = a1^T dz2

da1 = dz2 W2^T

dz1 = da1 * ReLU'(z1)

dW1 = X^T dz1
```

### 의미
- 순전파: 입력 -> 예측 확률
- 역전파: 손실 -> 각 가중치에 대한 기울기 계산

---

## 19. fitting(학습 루프)과 경사하강법

### 수식

```text
W := W - lr * dW
b := b - lr * db
```

### Python 대응

```python
for epoch in range(epochs):
    # forward
    # loss
    # backward
    W -= lr * dW
    b -= lr * db
```

### 개발자 메모
- `fit()`은 내부적으로 이 과정을 여러 epoch 반복합니다.
- loss가 점진적으로 감소하면 정상 학습 가능성이 높습니다.

---

## 20. CNN의 기본 합성곱(Convolution)

### 수식

```text
S(i, j) = (X * K) 의 지역합
```

### 의미
입력 이미지의 작은 영역(patch)과 필터(kernel)를 곱해서 더한 값을 feature map으로 만듭니다.

### Python 대응

```python
import numpy as np

patch = np.array([[1, 2, 0], [0, 1, 3], [2, 1, 0]])
kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
conv_value = np.sum(patch * kernel)
print(conv_value)
```

---

## 21. 수식 읽는 실전 요령

문서에서 식을 보면 아래 순서로 해석하면 됩니다.

1. **이 식이 모델 식인가, 손실 식인가, 업데이트 식인가?**
2. **입력(x), 정답(y), 예측(y_hat), 가중치(w), bias(b) 중 무엇이 등장하는가?**
3. **결국 계산 결과가 확률인가, 점수인가, 최종 예측값인가?**
4. **코드에서는 어느 메서드/속성으로 연결되는가?**
   - `fit()`
   - `predict()`
   - `predict_proba()`
   - `coef_`, `intercept_`

---

## 22. 핵심 요약

- 수식은 대부분 **예측 공식 / 손실 공식 / 업데이트 공식** 셋 중 하나입니다.
- `y_hat = wx + b` 는 가장 기본이 되는 예측 식입니다.
- `MSE`, `Cross Entropy` 는 얼마나 틀렸는지를 재는 공식입니다.
- `w = w - lr * grad` 는 덜 틀리게 수정하는 공식입니다.
- 개발자는 수식을 "코드에서 어떤 값/메서드와 대응되는가"로 보면 훨씬 쉬워집니다.

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=python+ai+ml+ai_ml_formula_to_code_mapping_ko+%EA%B0%95%EC%9D%98)
