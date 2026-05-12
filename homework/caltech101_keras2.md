# caltech101_keras2

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/caltech101_keras2.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
Caltech101 CNN 학습 결과를 저장하고 오분류 샘플까지 확인하는 확장 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/caltech101_keras2.py` 를 실행한다.
2. 가중치 저장 파일과 error 폴더를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
기본 구조는 CNN이며, 학습된 가중치를 파일로 저장/재사용하고 예측 결과를 분석한다.

## 입력과 출력
입력은 `image/5obj.npy`, 출력은 `image/5obj-model.hdf5`, 오분류 이미지, 평가 결과다.

## 실습 포인트
모델 학습뿐 아니라 결과 분석과 재사용까지 다루는 실습이다.
