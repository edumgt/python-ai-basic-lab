# keras-mnist


## 이 파일은 어떤 실습인가?
MNIST 숫자 분류를 Keras 완전연결 신경망으로 수행하는 대표적인 딥러닝 입문 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch5/keras-mnist.py` 를 실행한다.
2. MNIST가 자동으로 내려받아지고 전처리된 뒤 학습된다.
3. 테스트 정확도로 기본 MLP 성능을 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
입력 784차원 픽셀 벡터에 대해 Dense-ReLU-Dropout을 쌓은 MLP를 사용하며 최종층은 10-way softmax다. 최적화는 Adam을 사용한다.

## 입력과 출력
입력은 Keras가 내려받는 MNIST 데이터, 출력은 학습 로그와 테스트 정확도다.

## 실습 포인트
CNN 이전 단계의 기본 숫자 분류 네트워크를 익히는 예제다.
