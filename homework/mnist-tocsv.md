# mnist-tocsv


## 이 파일은 어떤 실습인가?
MNIST 바이너리 포맷을 사람이 다루기 쉬운 CSV로 바꾸는 전처리 실습이다.

## 실습은 어떻게 하면 되나?
1. `mnist-download.py`를 먼저 실행한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mnist-tocsv.py` 를 실행한다.
3. 생성된 CSV와 예시 이미지 파일을 확인해 레이블과 픽셀 구조를 이해한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
학습 알고리즘은 없고 `struct.unpack`으로 바이너리 포맷을 해석한 뒤 CSV로 직렬화한다.

## 입력과 출력
입력은 MNIST ubyte 파일, 출력은 `train.csv`, `t10k.csv`, 일부 `.pgm` 예시 이미지다.

## 실습 포인트
원시 이미지 데이터를 표 형식 피처 벡터로 바꾸는 과정을 보여준다.
