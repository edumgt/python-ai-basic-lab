# 📚 Overfitting vs Underfitting

## 🔎 Overfitting
- **정의**: 모델이 학습 데이터에 너무 과하게 맞춰져서 노이즈까지 학습하는 상태.  
- **원인**:  
  - 지나치게 복잡한 모델  
  - 데이터 부족  
  - 규제(regularization) 없음  
  - 너무 많은 특징(feature)  
- **특징**:  
  - 학습 데이터 성능은 높음  
  - 새로운 데이터(테스트 데이터) 성능은 낮음  
- **Bias/Variance**: **Low Bias, High Variance**  
- **비유**: 기출문제 답만 외워서 변형 문제를 못 푸는 경우  

---

## 🔎 Underfitting
- **정의**: 모델이 너무 단순해서 데이터의 중요한 패턴을 잡지 못하는 상태.  
- **원인**:  
  - 단순한 모델 (예: 직선으로 곡선 데이터 맞추기)  
  - 과도한 규제  
  - 부족한 특징(feature)  
- **특징**:  
  - 학습 데이터와 테스트 데이터 모두 성능 낮음  
- **Bias/Variance**: **High Bias, Low Variance**  
- **비유**: 개념을 너무 단순하게 이해해서 문제를 못 푸는 경우  

---

## ⚖️ Bias-Variance Tradeoff
- **Bias(편향)**: 모델이 데이터에 대해 강한 가정을 해서 단순화하는 정도 → 높으면 underfitting 발생  
- **Variance(분산)**: 모델이 데이터의 변동에 민감하게 반응하는 정도 → 높으면 overfitting 발생  
- **핵심**: 좋은 모델은 bias와 variance 사이에서 균형을 맞춰야 함  

---

## 📊 비교 표

| 구분 | **Underfitting** | **Overfitting** |
|------|------------------|-----------------|
| **정의** | 패턴을 못 잡음 | 노이즈까지 학습 |
| **원인** | 단순 모델, 과도한 규제 | 복잡 모델, 데이터 부족 |
| **Bias/Variance** | High Bias, Low Variance | Low Bias, High Variance |
| **성능** | 학습/테스트 모두 낮음 | 학습 높음, 테스트 낮음 |
| **비유** | 개념 단순화 → 문제 못 풂 | 답 외우기 → 변형 문제 못 풂 |

---

## ✅ 요약
- **Underfitting** → 너무 단순 → **High Bias**  
- **Overfitting** → 너무 복잡 → **High Variance**  
- 해결책: 데이터 양 늘리기, 모델 복잡성 조절, Regularization, Cross-validation 활용  
