# 선형회귀 기준으로 보는 AI/ML 용어와 실제 코드 해설

이 문서는 **선형회귀(Linear Regression) 하나만 기준**으로, AI/ML의 핵심 용어가 실제 Python 코드에서 어떻게 보이는지 설명합니다.

목표는 다음입니다.
- 용어를 단순 암기하지 않고
- 코드에서 어디가 그 용어인지 바로 연결해서 이해하기

---

## 1. 선형회귀를 기준으로 보는 이유

선형회귀는 가장 단순한 모델이지만, AI/ML의 기본 구조가 거의 다 들어 있습니다.

포함되는 핵심 개념:
- 입력(feature)
- 정답(target)
- 가중치(weight)
- 절편(bias/intercept)
- 예측(prediction)
- 오차(error)
- 손실(loss)
- 학습(training)
- 평가(evaluation)

즉, 선형회귀를 이해하면 나중에 로지스틱 회귀, 신경망도 훨씬 쉽게 연결됩니다.

---

## 2. 전체 코드 먼저 보기

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 예시 데이터: 공부시간 -> 시험점수
_df = pd.DataFrame({
    "study_hours": [1, 2, 3, 4, 5, 6, 7, 8],
    "score": [52, 57, 63, 68, 72, 78, 84, 88]
})

# 1) feature, target 분리
X = _df[["study_hours"]]
y = _df["score"]

# 2) train / test 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 3) 모델 생성
model = LinearRegression()

# 4) 학습
model.fit(X_train, y_train)

# 5) 예측
pred = model.predict(X_test)

# 6) 평가
mse = mean_squared_error(y_test, pred)
r2 = r2_score(y_test, pred)

print("coef:", model.coef_)
print("intercept:", model.intercept_)
print("pred:", pred)
print("MSE:", mse)
print("R2:", r2)
```

이제 위 코드의 각 부분을 용어와 연결해보겠습니다.

---

## 3. 데이터(Data)

### 용어
- 한글: 데이터
- 영어: Data

### 코드에서 어디?

```python
_df = pd.DataFrame({
    "study_hours": [1, 2, 3, 4, 5, 6, 7, 8],
    "score": [52, 57, 63, 68, 72, 78, 84, 88]
})
```

### 뜻
학습에 사용하는 원본 값입니다.

### 개발자 관점
- DB 결과셋
- CSV 로드 결과
- API 응답을 DataFrame으로 만든 것

과 같은 원천 데이터라고 보면 됩니다.

---

## 4. 특성(Feature)

### 용어
- 한글: 특성, 특징
- 한자: 特性, 特徵
- 영어: Feature

### 코드에서 어디?

```python
X = _df[["study_hours"]]
```

### 뜻
모델이 입력으로 받는 컬럼입니다.

### 개발자 관점
- `X`는 보통 feature 묶음
- DataFrame의 입력 컬럼들
- SQL로 치면 SELECT 해서 가져온 설명 변수 컬럼들

### 이 예제에서
- `study_hours`가 feature입니다.
- "공부시간"이라는 입력으로 "점수"를 맞추겠다는 의미입니다.

---

## 5. 타깃(Target) / 정답(Label)

### 용어
- 한글: 타깃, 목표값, 정답값
- 영어: Target, Label

### 코드에서 어디?

```python
y = _df["score"]
```

### 뜻
모델이 맞추려는 정답 값입니다.

### 개발자 관점
- `y`는 정답 컬럼
- 모델 출력이 궁극적으로 맞춰야 하는 값

### 이 예제에서
- `score`가 target입니다.

---

## 6. 학습용/테스트용 데이터 분리

### 용어
- 영어: Train / Test Split

### 코드에서 어디?

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
```

### 뜻
- `X_train`, `y_train`: 학습용
- `X_test`, `y_test`: 검증용

### 개발자 관점
- 학습 데이터만 보고 모델을 만든 뒤
- 처음 보는 테스트 데이터로 성능을 확인해야 함

### 왜 필요?
테스트 없이 학습 데이터만 보면, 외워버린 모델도 좋아 보일 수 있습니다.

---

## 7. 모델(Model)

### 용어
- 한글: 모델
- 영어: Model

### 코드에서 어디?

```python
model = LinearRegression()
```

### 뜻
선형회귀 알고리즘을 사용할 준비를 한 객체입니다.

### 개발자 관점
이 줄만으로는 아직 학습 전입니다.

즉,
- 현재는 "선형회귀 방식으로 해보겠다"는 설정 단계
- 아직 진짜 예측기는 아님

---

## 8. 학습(Training)

### 용어
- 한글: 학습
- 한자: 學習
- 영어: Training, Fit

### 코드에서 어디?

```python
model.fit(X_train, y_train)
```

### 뜻
입력과 정답을 보고 가장 잘 맞는 직선을 찾는 과정입니다.

### 개발자 관점
`fit()`이 호출되면 내부적으로 다음이 일어납니다.
- 입력값과 정답값의 관계를 분석하고
- 가장 잘 맞는 `weight`, `intercept`를 계산합니다.

즉, 이 시점부터 모델은 **학습된 상태**가 됩니다.

---

## 9. 가중치(Weight) / 계수(Coefficient)

### 용어
- 한글: 가중치, 계수
- 한자: 加重値, 係數
- 영어: Weight, Coefficient

### 코드에서 어디?

```python
print(model.coef_)
```

### 뜻
입력값이 결과에 얼마나 영향을 주는지 나타내는 숫자입니다.

### 개발자 관점
`coef_`는 선형회귀에서 매우 중요한 값입니다.

예를 들어 `coef_ = [5.2]` 라면,
- 공부시간이 1시간 늘 때
- 예측 점수가 약 5.2점 증가한다는 뜻으로 해석할 수 있습니다.

### 수식 연결

```text
y_hat = w*x + b
```

여기서 `w`가 바로 `coef_` 입니다.

---

## 10. 절편(Intercept) / 바이어스(Bias)

### 용어
- 한글: 절편
- 한자: 切片
- 영어: Intercept, Bias

### 코드에서 어디?

```python
print(model.intercept_)
```

### 뜻
입력이 0일 때의 기본값입니다.

### 개발자 관점
- 시작점
- 기본 오프셋

예를 들어 `intercept_ = 47` 이면,
공부시간이 0일 때도 예측 점수는 47점에서 시작한다는 의미로 볼 수 있습니다.

### 수식 연결

```text
y_hat = w*x + b
```

여기서 `b`가 `intercept_` 입니다.

---

## 11. 예측(Prediction)

### 용어
- 한글: 예측
- 영어: Prediction, Inference

### 코드에서 어디?

```python
pred = model.predict(X_test)
```

### 뜻
학습된 모델로 새로운 입력에 대한 결과를 계산합니다.

### 개발자 관점
- `predict()`는 운영 환경에서 가장 많이 쓰는 단계
- 실제 서비스에서는 API 입력값이 여기에 들어간다고 보면 됩니다.

예:
- 사용자 입력 -> feature 가공 -> `predict()` -> 결과 반환

---

## 12. 예측값(Predicted Value)

### 용어
- 한글: 예측값
- 영어: Predicted Value
- 수식 표기: `y_hat`

### 코드에서 어디?

```python
pred = model.predict(X_test)
```

### 뜻
모델이 계산한 결과값입니다.

### 개발자 관점
`pred`가 바로 `y_hat` 입니다.

즉, 수학 문서에서 `y_hat` 이 보이면 코드에서는 대체로:
- `pred`
- `prediction`
- `y_pred`

같은 이름으로 등장합니다.

---

## 13. 실제값(Actual Value)

### 용어
- 한글: 실제값, 정답값
- 영어: Actual Value, Ground Truth
- 수식 표기: `y`

### 코드에서 어디?

```python
y_test
```

### 뜻
정답 데이터입니다.

### 개발자 관점
예측값과 비교해 얼마나 맞는지 판단하는 기준입니다.

---

## 14. 오차(Error)

### 용어
- 한글: 오차
- 한자: 誤差
- 영어: Error

### 수식

```text
error = y - y_hat
```

### 코드 감각

```python
errors = y_test - pred
```

### 뜻
실제값과 예측값의 차이입니다.

### 개발자 관점
모델이 얼마나 틀렸는지 가장 직접적으로 보여주는 값입니다.

---

## 15. 손실(Loss) / 오차함수(Loss Function)

### 용어
- 한글: 손실, 오차함수
- 영어: Loss, Loss Function

### 이 예제에서 어디?
선형회귀 자체는 내부적으로 오차를 최소화하도록 학습합니다. 여기서는 평가 단계에서 MSE로 확인합니다.

```python
mse = mean_squared_error(y_test, pred)
```

### 뜻
전체적으로 얼마나 틀렸는지를 하나의 숫자로 만든 값입니다.

### 개발자 관점
- `mse`가 크면 많이 틀린 것
- `mse`가 작으면 잘 맞춘 것

---

## 16. 평균제곱오차(MSE)

### 용어
- 한글: 평균제곱오차
- 한자: 平均平方誤差
- 영어: Mean Squared Error, MSE

### 코드에서 어디?

```python
mse = mean_squared_error(y_test, pred)
```

### 뜻
오차를 제곱해서 평균낸 값입니다.

### 개발자 관점
- 큰 오차를 더 강하게 벌주는 방식
- 회귀 문제의 대표 평가 지표

### 직접 계산 감각

```python
manual_mse = ((y_test - pred) ** 2).mean()
```

---

## 17. 결정계수(R2 Score)

### 용어
- 한글: 결정계수
- 영어: R2 Score, Coefficient of Determination

### 코드에서 어디?

```python
r2 = r2_score(y_test, pred)
```

### 뜻
모델이 데이터를 얼마나 잘 설명하는지 보는 지표입니다.

### 개발자 관점
- 1에 가까울수록 잘 맞음
- 0이면 평균으로 때우는 수준과 비슷
- 음수가 나오면 오히려 못 맞춘 것

---

## 18. 선형회귀 수식과 코드 1:1 연결

### 수식

```text
y_hat = w*x + b
```

### 코드 대응

```python
# x  -> X_test 혹은 새 입력값
# w  -> model.coef_
# b  -> model.intercept_
# y_hat -> model.predict(...) 결과
```

즉, 아래처럼 읽으면 됩니다.

- `X` = 입력값 x
- `model.coef_` = w
- `model.intercept_` = b
- `pred` = y_hat

---

## 19. 새 데이터 예측 예시

```python
new_data = pd.DataFrame({"study_hours": [9]})
new_pred = model.predict(new_data)
print(new_pred)
```

### 개발자 관점
실제 서비스 API라면 대략 이런 흐름입니다.

1. 사용자가 `study_hours=9` 입력
2. 서버에서 DataFrame 또는 배열로 변환
3. `model.predict()` 호출
4. 예측 점수 반환

즉, 머신러닝 모델도 결국 **입력을 넣으면 출력이 나오는 함수**처럼 사용할 수 있습니다.

---

## 20. 이 예제에서 꼭 기억할 핵심 매핑

- `DataFrame` -> 데이터
- `X` -> feature 묶음
- `y` -> target
- `LinearRegression()` -> 알고리즘 선택
- `fit()` -> 학습
- `coef_` -> 가중치
- `intercept_` -> 절편
- `predict()` -> 추론
- `pred` -> 예측값
- `mean_squared_error()` -> 오차 측정
- `r2_score()` -> 설명력 측정

---

## 21. 선형회귀가 중요한 이유

선형회귀는 단순하지만, 나중에 배우는 거의 모든 모델의 기초를 제공합니다.

연결되는 개념:
- 로지스틱 회귀: 선형식 + 시그모이드
- 신경망: 선형식 여러 층 + 활성화함수
- 딥러닝: 가중치, bias, loss, gradient를 더 크게 확장한 형태

즉, 선형회귀 코드에서 보이는 용어를 이해하면 AI/ML 문서가 훨씬 덜 어렵게 느껴집니다.

---

## 22. 핵심 요약

선형회귀 하나만 놓고 보면 AI/ML 용어는 이렇게 읽으면 됩니다.

- **feature**: 입력 컬럼
- **target**: 정답 컬럼
- **weight(coef_)**: 입력 영향력
- **intercept**: 기본값
- **predict()**: 예측 수행
- **pred(y_hat)**: 예측 결과
- **error**: 실제값과 예측값 차이
- **MSE**: 전체적으로 얼마나 틀렸는지
- **R2**: 얼마나 잘 설명하는지

즉, 수학 용어는 사실 대부분 코드에서 이미 보고 있는 것들입니다. 이름이 어렵게 느껴질 뿐, 실제로는 **변수명 + 메서드 + 결과값**으로 연결하면 훨씬 쉽게 이해할 수 있습니다.

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=python+ai+ml+linear+regression+terms+in+code+%EA%B0%95%EC%9D%98)
