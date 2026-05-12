# mnist-download

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mnist-download.py`
- 장: `CH4`

## 이 파일은 어떤 실습인가?
MNIST 원본 데이터를 내려받아 후속 실습에 사용할 준비를 하는 데이터 수집 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/mnist-download.py` 를 실행한다.
2. 생성된 `mnist` 디렉터리 안에 원본 파일이 내려받아졌는지 확인한다.
3. 이후 `mnist-tocsv.py`, `mnist-train.py`, `grid-mnist.py`로 이어간다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
머신러닝 알고리즘은 없고 파일 다운로드 및 gzip 해제만 수행한다.

## 입력과 출력
입력은 없다. 출력은 `ch4/mnist/` 이하의 MNIST 원본 파일들이다.

## 실습 포인트
전처리 이전의 원시 데이터 형식을 체험하는 준비 단계다.
