# mnist-train


## 이 파일은 어떤 실습인가?
MNIST 손글씨 숫자 분류를 SVM으로 수행하는 고전적인 이미지 분류 실습이다.

## 실습은 어떻게 하면 되나?
1. `mnist-download.py`와 `mnist-tocsv.py`를 먼저 실행한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mnist-train.py` 를 실행한다.
3. 테스트 정확도와 분류 리포트를 통해 SVM 성능을 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
각 이미지를 1차원 픽셀 벡터로 보고 `sklearn.svm.SVC`로 10개 숫자를 분류한다.

## 입력과 출력
입력은 `ch4/mnist/train.csv`, `ch4/mnist/t10k.csv`, 출력은 정확도와 분류 리포트다.

## 실습 포인트
딥러닝 이전 방식으로도 이미지 분류가 가능하지만 계산량이 커진다는 점을 체험할 수 있다.
