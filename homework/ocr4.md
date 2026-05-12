# ocr4

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr4.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
폰트 기반으로 학습한 OCR 모델을 실제 이미지에 적용하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `font_draw.py`, `ocr_learn_font.py`를 먼저 실행한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr4.py` 를 실행한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
OpenCV 전처리 후, 폰트 데이터로 학습한 MLP 숫자 분류 모델을 사용한다.

## 입력과 출력
입력은 숫자 이미지와 `font_draw.hdf5`, 출력은 예측 결과와 정확도다.

## 실습 포인트
학습 데이터 출처가 달라질 때 OCR 성능이 어떻게 달라질지 비교하기 좋은 실습이다.
