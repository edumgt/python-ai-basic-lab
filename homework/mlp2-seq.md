# mlp2-seq

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/mlp2-seq.py`
- 장: `CH6`

## 이 파일은 어떤 실습인가?
텍스트 분류용 뉴스 데이터를 사전 기반 숫자 벡터로 바꾸는 전처리 실습이다.

## 실습은 어떻게 하면 되나?
1. 형태소 분리된 뉴스 파일들이 준비되어 있어야 한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/mlp2-seq.py` 를 실행한다.
3. 생성된 `word-dic.json`, `data.json`, `data-mini.json`을 후속 분류 실습에서 사용한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
딥러닝 모델 학습은 없고 Bag-of-Words 빈도 벡터와 단어 사전 구축을 수행한다.

## 입력과 출력
입력은 뉴스 텍스트 파일들, 출력은 단어 사전과 벡터화된 JSON 데이터다.

## 실습 포인트
텍스트를 숫자 피처로 바꾸는 NLP 전처리 단계의 핵심을 보여준다.
