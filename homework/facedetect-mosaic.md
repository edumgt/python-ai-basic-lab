# facedetect-mosaic


## 이 파일은 어떤 실습인가?
얼굴 검출 후 해당 영역에 모자이크를 적용하는 OpenCV 실습이다.

## 실습은 어떻게 하면 되나?
1. `python /home/runner/work/py-ml-dl-lab/py-ml-dl-lab/ch7/facedetect-mosaic.py <이미지경로>` 형태로 실행한다.
2. 출력 이미지에서 얼굴 영역이 흐려졌는지 확인한다.

## 사용되는 ML / DL / 데이터 처리 알고리즘
OpenCV Haar Cascade로 얼굴을 검출하고, 검출 박스 영역을 축소/확대해 모자이크 효과를 만든다.

## 입력과 출력
입력은 이미지 파일, 출력은 모자이크 처리된 이미지 파일이다.

## 실습 포인트
검출과 후처리를 연결한 실용 예제다.
