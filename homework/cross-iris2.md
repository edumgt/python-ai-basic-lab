# cross-iris2


## 이 파일은 어떤 실습인가?
붓꽃 데이터셋 교차 검증을 `scikit-learn` 표준 API로 수행하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/cross-iris2.py` 를 실행한다.
2. `cross_val_score`가 반환하는 fold별 점수와 평균값을 확인한다.
3. `cross-iris.py` 결과와 비교해 수동 구현과 라이브러리 구현의 차이를 학습한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`sklearn.svm.SVC` + `sklearn.model_selection.cross_val_score`를 사용한 5-fold 교차 검증이다.

## 입력과 출력
입력은 `ch4/iris.csv`, 출력은 교차 검증 점수 배열과 평균 점수다.

## 실습 포인트
실무에서는 보통 이 방식처럼 검증 절차를 라이브러리 API로 일관되게 수행한다.
