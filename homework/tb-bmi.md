# tb-bmi


## 이 파일은 어떤 실습인가?
BMI 소프트맥스 회귀 실습에 TensorBoard 그래프 기록을 추가한 버전이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch5/tb-bmi.py` 를 실행한다.
2. 학습 후 TensorBoard에서 그래프 구조를 살펴본다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
소프트맥스 회귀 + 경사하강법이며, 그래프 기록을 위한 `FileWriter`를 함께 사용한다.

## 입력과 출력
입력은 `ch5/bmi.csv`, 출력은 정확도와 TensorBoard 로그다.

## 실습 포인트
학습 과정 자체보다 연산 그래프를 관찰하는 교육 목적이 강하다.
