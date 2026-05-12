# mnist-deep

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch5/mnist-deep.py`
- 장: `CH5`

## 이 파일은 어떤 실습인가?
MNIST에 대해 합성곱 신경망(CNN)을 직접 TensorFlow 1 스타일로 구성해 보는 실습이다.

## 실습은 어떻게 하면 되나?
1. TensorFlow 1.x 호환 환경을 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch5/mnist-deep.py` 를 실행한다.
3. 학습 단계별 정확도와 TensorBoard 로그를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
Conv2D + MaxPooling + Fully Connected + Dropout + Softmax 구조의 CNN이다. 최적화는 Adam을 사용한다.

## 입력과 출력
입력은 MNIST 데이터셋, 출력은 정확도와 `log_dir` TensorBoard 로그다.

## 실습 포인트
고수준 API 없이 CNN 레이어를 직접 쌓는 방식이라 딥러닝 내부 구조를 공부하기 좋다.
