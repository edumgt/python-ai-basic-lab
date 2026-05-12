# caltech101_keras


## 이 파일은 어떤 실습인가?
Caltech101 일부 클래스를 CNN으로 분류하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `caltech101_makedata.py`로 `5obj.npy`를 만든다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/caltech101_keras.py` 를 실행한다.
3. 학습 후 손실과 정확도를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
Conv2D, MaxPooling, Dropout, Dense를 쌓은 합성곱 신경망(CNN)을 사용한다.

## 입력과 출력
입력은 `image/5obj.npy`, 출력은 학습 로그와 평가 성능이다.

## 실습 포인트
대표적인 소규모 이미지 분류 딥러닝 실습이다.
