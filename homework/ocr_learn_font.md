# ocr_learn_font

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr_learn_font.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
합성 폰트 숫자 이미지로 OCR 분류 모델을 학습하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `font_draw.py`로 `font_draw.npz`를 만든다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr_learn_font.py` 를 실행한다.
3. 가중치 파일과 평가 성능을 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
Dense-ReLU-Dropout 기반 다층 퍼셉트론(MLP) 숫자 분류기다.

## 입력과 출력
입력은 `image/font_draw.npz`, 출력은 `font_draw.hdf5`와 평가 결과다.

## 실습 포인트
합성 데이터만으로도 OCR 모델을 학습할 수 있음을 보여준다.
