# caltech101_makedata


## 이 파일은 어떤 실습인가?
Caltech101 이미지를 CNN 학습용 넘파이 배열로 변환하는 전처리 실습이다.

## 실습은 어떻게 하면 되나?
1. 대상 이미지 폴더를 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/caltech101_makedata.py` 를 실행한다.
3. 생성된 `5obj.npy`를 후속 CNN 학습 스크립트에 사용한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
학습 알고리즘은 없고 이미지 리사이즈, 배열화, one-hot 라벨링, train/test 분할을 수행한다.

## 입력과 출력
입력은 원본 이미지들, 출력은 `image/5obj.npy` 데이터 파일이다.

## 실습 포인트
컴퓨터 비전 딥러닝에서 필수적인 데이터셋 구축 단계다.
