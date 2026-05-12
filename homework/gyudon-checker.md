# gyudon-checker

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/gyudon-checker.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
학습된 규동 분류 모델로 음식 종류를 판정하고 칼로리까지 표시하는 추론 실습이다.

## 실습은 어떻게 하면 되나?
1. `gyudon_keras.py`로 모델 가중치를 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/gyudon-checker.py <이미지경로>` 를 실행한다.
3. 콘솔/HTML 출력으로 분류 결과를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
내부적으로는 CNN 분류 모델을 로드해 softmax 예측을 수행한다.

## 입력과 출력
입력은 음식 이미지와 `gyudon-model.hdf5`, 출력은 예측 클래스명과 칼로리 정보, HTML 결과다.

## 실습 포인트
학습 모델을 실제 판별 도구처럼 사용하는 데 초점이 있다.
