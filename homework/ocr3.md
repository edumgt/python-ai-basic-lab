# ocr3

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr3.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
MNIST로 학습한 숫자 분류 모델을 실제 이미지 OCR에 적용하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `ocr_mnist.py`로 `mnist.hdf5`를 만든다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr3.py` 를 실행한다.
3. 검출된 각 숫자의 예측 결과와 전체 정확도를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
OpenCV로 숫자 영역을 분리한 뒤, MLP 숫자 분류기(`ocr_mnist.py`의 모델)로 각 영역을 예측한다.

## 입력과 출력
입력은 숫자 이미지와 `mnist.hdf5`, 출력은 예측 숫자, 박스 이미지, 정확도다.

## 실습 포인트
전처리 + 분류 모델을 합쳐 실제 OCR 흐름을 구성한 예제다.
