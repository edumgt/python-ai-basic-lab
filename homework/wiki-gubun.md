# wiki-gubun

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/wiki-gubun.py`
- 장: `CH6`

## 이 파일은 어떤 실습인가?
위키 문서를 형태소 단위로 분해해 Word2Vec 학습용 코퍼스를 만드는 전처리 실습이다.

## 실습은 어떻게 하면 되나?
1. `wiki.txt` 입력 파일을 준비한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/wiki-gubun.py` 를 실행한다.
3. 생성된 `wiki.gubun` 파일을 `wiki-mkdic.py`에 사용한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
학습 알고리즘은 없고 형태소 분석과 불필요한 품사 제거를 통한 코퍼스 정제 작업이다.

## 입력과 출력
입력은 위키 원문 텍스트, 출력은 형태소 분리된 `wiki.gubun` 파일이다.

## 실습 포인트
분산 표현 학습 전에 말뭉치를 정돈하는 단계다.
