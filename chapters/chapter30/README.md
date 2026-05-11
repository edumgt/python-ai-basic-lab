# CHAPTER30 - CNN 핵심 연산(Convolution/Pooling)

- 주제: CNN 핵심 연산(Convolution/Pooling)
- 목표: 합성곱과 맥스풀링을 NumPy로 직접 구현합니다.
- 실행: `python practice.py`

---

## 핵심 개념

- **Convolution**: 작은 필터로 국소 패턴을 훑으며 특징을 추출합니다.
- **ReLU**: 음수를 0으로 바꿔 비선형성을 넣습니다.
- **Pooling**: 중요한 값만 남기며 차원을 줄이고 잡음을 덜어냅니다.

## 언제 쓰나요?

- 이미지·차트·센서처럼 **인접한 패턴**이 중요한 데이터에서
- 전체보다 작은 지역 특징을 먼저 찾고 싶을 때
- 시계열의 국소 패턴을 감지하는 1D-CNN 개념으로 확장할 때

## 결과 해석 체크리스트

- `conv_output`이 필터를 적용한 직후의 값인지 확인합니다.
- `relu_output`에서 음수가 0으로 바뀌는지 봅니다.
- `pool_output`으로 정보가 압축되는 과정을 단계별로 비교합니다.

## 웹앱 실습 순서

1. 실행 결과에서 합성곱 → ReLU → 풀링 순서를 확인합니다.
2. 설명 탭에서 필터가 어떤 패턴을 강조하는지 읽습니다.
3. `chapter21`의 기본 신경망과 비교해 CNN이 왜 지역 패턴에 강한지 정리합니다.
4. 이후 `doc/07.md` 또는 관련 챕터에서 시계열 패턴 실습으로 확장합니다.

## 다음으로 연결할 챕터

- `chapter21` 신경망 기초와 학습
- `chapter101` RNN 시계열 예측 기초
- `chapter103` Transformer 시계열 기초

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=python+ai+ml+cnn+기초+강의)
