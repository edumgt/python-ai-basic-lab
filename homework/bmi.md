# bmi


## 이 파일은 어떤 실습인가?
BMI 3분류 문제를 TensorFlow 1.x 스타일의 저수준 코드로 학습해 보는 실습이다.

## 실습은 어떻게 하면 되나?
1. `ch5/bmi.csv`를 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch5/bmi.py` 를 실행한다.
3. 학습 반복 중 출력되는 정확도를 보며 손실 최소화가 진행되는지 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
소프트맥스 회귀(다중 로지스틱 회귀)를 `GradientDescentOptimizer`로 학습한다. 입력은 키와 몸무게, 출력은 3개 클래스 확률이다.

## 입력과 출력
입력은 `ch5/bmi.csv`, 출력은 학습 중/후 정확도다.

## 실습 포인트
Keras 같은 고수준 API 없이 placeholder, variable, session으로 직접 모델을 구성하는 것이 핵심 학습 포인트다.
