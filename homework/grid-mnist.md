# grid-mnist

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/grid-mnist.py`
- 장: `CH4`

## 이 파일은 어떤 실습인가?
MNIST 숫자 분류에서 SVM 하이퍼파라미터 탐색을 수행하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `mnist-download.py`와 `mnist-tocsv.py`를 먼저 실행해 CSV 데이터를 만든다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/grid-mnist.py` 를 실행한다.
3. 출력되는 최적 파라미터와 테스트 정확도를 보며 그리드 서치의 역할을 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`sklearn.svm.SVC`에 대해 `GridSearchCV`로 `C`, `kernel`, `gamma` 조합을 탐색하는 하이퍼파라미터 튜닝 실습이다.

## 입력과 출력
입력은 `ch4/mnist/train.csv`, `ch4/mnist/t10k.csv`, 출력은 최적 모델 정보와 정확도다.

## 실습 포인트
단순히 모델을 학습하는 단계가 아니라 모델 선택(Model Selection) 과정을 익히는 예제다.
