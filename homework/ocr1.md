# ocr1

- 원본 소스: `/home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr1.py`
- 장: `CH7`

## 이 파일은 어떤 실습인가?
OCR 이전 단계로 숫자 영역을 분리하는 영상처리 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/ocr1.py` 를 실행한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
그레이스케일 변환, 가우시안 블러, 적응형 이진화, 컨투어 검출 등 OpenCV 전처리 기법을 사용한다.

## 입력과 출력
입력은 숫자 이미지, 출력은 숫자 위치에 박스를 그린 이미지다.

## 실습 포인트
분류 모델보다 먼저 문자 영역 검출이 필요하다는 점을 보여준다.
