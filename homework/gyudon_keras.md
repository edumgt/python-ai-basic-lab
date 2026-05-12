# gyudon_keras

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/gyudon_keras.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
규동 이미지를 여러 종류로 분류하는 CNN 실습이다.

## 실습은 어떻게 하면 되나?
1. `gyudon-makedata.py` 또는 `gyudon-makedata2.py`로 데이터 파일을 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/gyudon_keras.py` 를 실행한다.
3. 학습 후 가중치 파일과 정확도를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
Conv2D, MaxPooling, Dropout, Dense를 조합한 합성곱 신경망(CNN) 다중 분류 모델이다.

## 입력과 출력
입력은 `image/gyudon.npy` 또는 증강 버전 데이터, 출력은 `image/gyudon-model.hdf5`와 평가 결과다.

## 실습 포인트
음식 이미지 분류라는 실생활형 컴퓨터 비전 예제다.
