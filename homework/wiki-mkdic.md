# wiki-mkdic

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/wiki-mkdic.py`
- 장: `CH6`

## 이 파일은 어떤 실습인가?
전처리한 위키 코퍼스로 Word2Vec 임베딩을 학습하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `wiki-gubun.py`로 `wiki.gubun`을 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/wiki-mkdic.py` 를 실행한다.
3. 생성된 `wiki.model`을 불러 유사 단어 탐색 등에 활용한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`gensim.models.Word2Vec`을 이용한 단어 임베딩 학습이다. 단어의 분산 표현을 학습한다.

## 입력과 출력
입력은 `wiki.gubun`, 출력은 `wiki.model`이다.

## 실습 포인트
의미적으로 비슷한 단어가 가까운 벡터를 갖도록 만드는 전형적인 워드 임베딩 실습이다.
