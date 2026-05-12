# gyudon-makedata

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/gyudon-makedata.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
규동 이미지 분류용 데이터를 넘파이 배열로 만드는 전처리 실습이다.

## 실습은 어떻게 하면 되나?
1. 카테고리별 이미지 폴더를 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/gyudon-makedata.py` 를 실행한다.
3. 생성된 `gyudon.npy`를 CNN 학습에 사용한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
이미지 리사이즈, 배열화, one-hot 라벨링, train/test 분할을 수행한다.

## 입력과 출력
입력은 음식 이미지 파일들, 출력은 `image/gyudon.npy`다.

## 실습 포인트
CV 딥러닝 학습 전처리의 정석적인 흐름이다.
