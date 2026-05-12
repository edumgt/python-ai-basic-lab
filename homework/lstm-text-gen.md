# lstm-text-gen

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/lstm-text-gen.py`
- 장: `CH6`

## 이 파일은 어떤 실습인가?
소설 텍스트를 학습해 다음 문자를 예측하며 문장을 생성하는 LSTM 실습이다.

## 실습은 어떻게 하면 되나?
1. `BEXX0003.txt` 파일이 준비되어 있는지 확인한다.
2. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch6/lstm-text-gen.py` 를 실행한다.
3. 에폭마다 여러 temperature 값으로 생성되는 샘플 문장을 관찰한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
문자 단위 시퀀스를 입력으로 하는 LSTM 기반 언어 모델이다. 출력은 다음 문자 softmax 확률이며 샘플링 temperature를 조절한다.

## 입력과 출력
입력은 `ch6/BEXX0003.txt`, 출력은 콘솔에 생성되는 텍스트다.

## 실습 포인트
RNN/LSTM이 순차 데이터의 문맥을 어떻게 학습하는지 체험할 수 있다.
