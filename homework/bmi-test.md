# bmi-test


## 이 파일은 어떤 실습인가?
BMI 데이터를 이용해 사람을 `thin`, `normal`, `fat` 3개 클래스로 분류하는 전형적인 지도학습 실습이다.

## 실습은 어떻게 하면 되나?
1. `ch4/bmi.csv`를 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/bmi-test.py` 를 실행한다.
3. 학습/평가 분할 후 정확도와 분류 리포트를 확인하며 SVM 분류기의 동작을 이해한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`sklearn.svm.SVC`를 이용한 서포트 벡터 머신(SVM) 다중 분류를 사용한다. `train_test_split`으로 데이터를 나누고 `accuracy_score`, `classification_report`로 평가한다.

## 입력과 출력
입력은 `ch4/bmi.csv`, 출력은 콘솔의 정확도와 클래스별 정밀도/재현율/F1 값이다.

## 실습 포인트
피처 수가 적고 경계가 비교적 단순한 데이터에서 SVM이 어떻게 분류하는지 살펴보기 좋은 입문 실습이다.
