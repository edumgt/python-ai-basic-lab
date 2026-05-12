# bmi-create

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/bmi-create.py`
- 장: `CH4`

## 이 파일은 어떤 실습인가?
BMI 분류용 예제 데이터를 직접 생성해 보는 실습이다. 키와 몸무게를 임의로 만들고 BMI 공식을 적용해 `thin`, `normal`, `fat` 라벨을 부여하는 흐름을 익힌다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/bmi-create.py` 를 실행한다.
2. 루트가 아니라 `ch4` 폴더에 `bmi.csv`가 생성되므로 이후 BMI 분류 예제의 입력 데이터로 사용한다.
3. 생성된 CSV를 열어 키/몸무게/라벨 구조를 확인한 뒤 후속 분류 실습(`bmi-test.py`, `bmi.py`, `keras-bmi.py`)에 연결한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
머신러닝 알고리즘은 사용하지 않는다. BMI = 체중 / (키(m)^2) 공식을 이용한 규칙 기반 라벨링과 난수 데이터 생성만 수행한다.

## 입력과 출력
입력은 없다. 출력은 `ch4/bmi.csv`이며 각 행은 height, weight, label 정보를 가진다.

## 실습 포인트
데이터 생성 단계이므로 모델 학습 이전에 데이터셋 구조를 이해하기 위한 준비 실습으로 보면 된다.
