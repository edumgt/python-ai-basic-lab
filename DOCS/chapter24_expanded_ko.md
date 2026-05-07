# Chapter 24 학습 노트 - 소프트맥스 확률 해석

## 학습 목표
- 로짓(logit)을 확률로 변환하고 온도(temperature) 효과를 확인합니다.
- chapter24/practice.py를 실행해 핵심 값을 직접 확인합니다.

## 핵심 개념
- 이 챕터는 chapter21의 내용을 세분화한 파트입니다.
- 수식을 코드로 옮길 때, `입력 shape -> 가중치 shape -> 출력 shape`를 항상 먼저 점검합니다.

## 실행 방법
```bash
cd chapters/chapter24
python practice.py
```

## 체크 포인트
1. 출력 딕셔너리의 `chapter`, `topic` 필드 확인
2. 각 챕터별 핵심 지표(손실, 정확도, shape, 확률 등) 확인
3. 실험 값(학습률, 에폭, 초기화 스케일)을 바꿔 추가 실험

## 확장 아이디어
- numpy만으로 구현한 연산을 PyTorch/TensorFlow와 비교하기
- 데이터 샘플 수를 늘려 일반화 성능 변화를 확인하기

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=python+ai+basic+lab+chapter24+%EC%8B%A4%EC%8A%B5+%EA%B0%95%EC%9D%98)
