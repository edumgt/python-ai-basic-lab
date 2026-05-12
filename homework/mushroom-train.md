# mushroom-train

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mushroom-train.py`
- 장: `CH4`

## 이 파일은 어떤 실습인가?
버섯의 범주형 특성으로 식용/독성 여부를 분류하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `mushroom-download.py`로 데이터를 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mushroom-train.py` 를 실행한다.
3. 정확도와 분류 리포트를 보며 랜덤 포레스트 분류 결과를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`RandomForestClassifier`를 사용한다. 각 범주형 문자를 단순 ordinal 방식으로 수치화해 학습한다.

## 입력과 출력
입력은 `ch4/mushroom.csv`, 출력은 정확도와 분류 리포트다.

## 실습 포인트
트리 계열 모델이 범주형 성격의 데이터를 잘 다루는 예시로 볼 수 있다.
