# keras-bmi

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch5/keras-bmi.py`
- 장: `CH5`

## 이 파일은 어떤 실습인가?
BMI 분류를 Keras 다층 퍼셉트론(MLP)으로 수행하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch5/keras-bmi.py` 를 실행한다.
2. 모델 구조, 학습 로그, 최종 정확도를 확인한다.
3. 과적합 방지를 위한 Dropout과 EarlyStopping의 역할을 함께 본다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
Dense-ReLU-Dropout 층을 여러 개 쌓은 MLP와 소프트맥스 출력층을 사용한다. 다중 분류 손실로 categorical crossentropy 계열 설정이 적용된다.

## 입력과 출력
입력은 `ch5/bmi.csv`, 출력은 학습 로그와 평가 손실/정확도다.

## 실습 포인트
같은 BMI 문제를 저수준 TF 코드 대신 고수준 Keras로 더 간단히 구현하는 비교 실습이다.
