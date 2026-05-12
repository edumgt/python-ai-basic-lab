# font_draw


## 이 파일은 어떤 실습인가?
폰트로 숫자 이미지를 대량 생성해 OCR 학습 데이터를 만드는 실습이다.

## 실습은 어떻게 하면 되나?
1. 시스템에 사용 가능한 폰트가 있는지 확인한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/font_draw.py` 를 실행한다.
3. 생성된 NPZ 파일을 `ocr_learn_font.py`에서 학습 데이터로 사용한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
딥러닝 학습은 없고 PIL 렌더링, 회전/크기 변경, OpenCV 이진화 등 데이터 증강 기법을 사용한다.

## 입력과 출력
입력은 시스템 폰트, 출력은 `image/font_draw.npz`다.

## 실습 포인트
실제 손글씨 데이터가 부족할 때 synthetic data를 만드는 아이디어를 배울 수 있다.
