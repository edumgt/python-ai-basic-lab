# ocr_mnist

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr_mnist.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
MNIST를 이용해 숫자 인식용 MLP 모델을 학습하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr_mnist.py` 를 실행한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
MNIST 28x28 이미지를 입력으로 하는 Dense-ReLU-Dropout 기반 MLP 분류기다.

## 입력과 출력
입력은 Keras가 내려받는 MNIST 데이터, 출력은 `mnist.hdf5` 가중치와 평가 결과다.

## 실습 포인트
후속 OCR 파이프라인에서 재사용되는 기본 숫자 분류 모델이다.
