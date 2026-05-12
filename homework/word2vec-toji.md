# word2vec-toji


## 이 파일은 어떤 실습인가?
소설 `토지` 텍스트에서 Word2Vec 임베딩을 학습하는 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/word2vec-toji.py` 를 실행한다.
2. 형태소 분리 결과와 저장된 모델 파일을 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
`gensim`의 Skip-gram 기반 Word2Vec을 사용해 단어 임베딩을 학습한다.

## 입력과 출력
입력은 `ch6/BEXX0003.txt`, 출력은 `toji.gubun`과 `toji.model`이다.

## 실습 포인트
일반 위키 대신 특정 작품 코퍼스에서 임베딩을 만드는 사례다.
