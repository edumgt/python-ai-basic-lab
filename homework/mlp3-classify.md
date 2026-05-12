# mlp3-classify

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/mlp3-classify.py`
- 장: `CH6`

## 이 파일은 어떤 실습인가?
벡터화된 뉴스 데이터를 MLP로 다중 분류하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `mlp2-seq.py`를 먼저 실행해 `data-mini.json`을 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/mlp3-classify.py` 를 실행한다.
3. 정확도와 classification report를 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
Bag-of-Words 입력에 대해 Dense-ReLU-Dropout 구조의 다층 퍼셉트론을 사용한다. 출력은 6개 뉴스 카테고리 softmax다.

## 입력과 출력
입력은 `newstext/data-mini.json` 계열 파일, 출력은 정확도와 분류 리포트다.

## 실습 포인트
텍스트를 순서 정보 없이 벡터화해도 기본적인 문서 분류가 가능함을 보여준다.
