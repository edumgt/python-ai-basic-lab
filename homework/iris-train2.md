# iris-train2


## 이 파일은 어떤 실습인가?
붓꽃 분류를 `pandas`와 `train_test_split`으로 더 간결하게 수행하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/iris-train2.py` 를 실행한다.
2. `pandas`로 데이터를 읽고 표준 학습/평가 API를 적용하는 흐름을 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`sklearn.svm.SVC`와 `train_test_split`을 사용한 다중 클래스 분류다.

## 입력과 출력
입력은 `ch4/iris.csv`, 출력은 정확도다.

## 실습 포인트
초기 예제에서 수동 처리하던 부분을 라이브러리 중심 방식으로 바꾼 개선판으로 볼 수 있다.
