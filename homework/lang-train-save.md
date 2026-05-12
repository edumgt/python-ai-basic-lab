# lang-train-save


## 이 파일은 어떤 실습인가?
문자 빈도 기반 언어 판별 모델을 학습한 뒤 파일로 저장하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `lang-train.py`로 `lang/freq.json`을 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch4/lang-train-save.py` 를 실행한다.
3. 생성된 `freq.pkl`을 웹앱이나 재사용 스크립트에서 불러온다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`sklearn.svm.SVC`를 이용한 언어 분류 모델을 학습하고 `joblib.dump`로 직렬화한다.

## 입력과 출력
입력은 `ch4/lang/freq.json`, 출력은 `ch4/lang/freq.pkl` 모델 파일이다.

## 실습 포인트
모델 학습과 저장을 분리해 재사용 가능한 추론 자산을 만드는 예제다.
