# CHAPTER115 - Instruction Tuning 지시 분류 시뮬레이션

- 주제: Instruction Tuning 개념 이해 및 도메인 특화 파인튜닝 효과 시뮬레이션
- 목표: 금융 도메인 지시 문장을 TF-IDF + 로지스틱 회귀로 분류하고, 파인튜닝 전후 성능 차이를 확인합니다.
- 실행: `python practice.py`

---

## 핵심 개념

- **Instruction Tuning**: 모델이 사람의 지시를 잘 따르도록 (지시, 입력, 출력) 형식 데이터로 학습합니다.
- **도메인 특화**: 금융 용어와 맥락이 담긴 지시 데이터는 일반 모델보다 훨씬 잘 분류됩니다.
- **적은 데이터의 힘**: LIMA 논문에 따르면 1,000개 고품질 데이터만으로도 충분한 효과를 냅니다.
- **5가지 카테고리**: analysis(분석), summary(요약), signal(매매신호), risk(리스크), qa(질의응답)

## 시뮬레이션 설계

| 구분 | 설명 |
|---|---|
| 파인튜닝 전 | 도메인 외 일반 문장 10개로 학습 (일반 모델 시뮬레이션) |
| 파인튜닝 후 | 금융 Instruction 데이터 30개로 학습 (도메인 파인튜닝 시뮬레이션) |
| 평가 | 동일한 금융 테스트 문장 8개로 비교 |

## 결과 해석 체크리스트

- `accuracy_gain`이 양수이면 파인튜닝 후 성능이 향상된 것입니다.
- `improved: true`인 항목은 파인튜닝으로 개선된 사례입니다.
- `per_category`로 카테고리별 학습 데이터 수를 확인합니다.

## 웹앱 실습 순서

1. `chapter115`를 실행합니다.
2. `before_finetuning`과 `after_finetuning`의 accuracy를 비교합니다.
3. `test_predictions`에서 어떤 지시가 개선되었는지 확인합니다.
4. `docs/13.md`의 Instruction Tuning 데이터 형식 설명과 대조합니다.

## 다음으로 연결할 챕터

- `chapter114` LoRA 파라미터 시뮬레이션
- `chapter113` TF-IDF 텍스트 분류 (기준선 비교)

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=instruction+tuning+LLM+파인튜닝+강의)
