# mushroom-train2

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mushroom-train2.py`
- 장: `CH4`

## 이 파일은 어떤 실습인가?
버섯 분류에서 범주형 특성 인코딩 방식을 바꿔보는 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mushroom-train2.py` 를 실행한다.
2. 기존 `mushroom-train.py`와 결과를 비교한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`RandomForestClassifier`는 동일하지만 범주형 값을 one-hot 형태로 펼쳐 표현하는 방식이 핵심이다.

## 입력과 출력
입력은 `ch4/mushroom.csv`, 출력은 정확도다.

## 실습 포인트
같은 알고리즘이라도 피처 인코딩 전략에 따라 입력 표현이 달라질 수 있음을 보여준다.
