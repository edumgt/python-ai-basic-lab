# CHAPTER114 - LoRA 저랭크 적응 파라미터 시뮬레이션

- 주제: LoRA(Low-Rank Adaptation) 개념 이해 및 파라미터 압축 효과 시뮬레이션
- 목표: 사전학습 가중치를 동결하고 저랭크 행렬 B×A만 추가할 때 파라미터 절감 효과를 수치로 확인합니다.
- 실행: `python practice.py`

---

## 핵심 개념

- **LoRA**: 가중치 행렬 W(d×k)의 업데이트 ΔW를 B(d×r) × A(r×k)로 분해합니다. r≪min(d,k)이므로 파라미터가 대폭 줄어듭니다.
- **동결(Freeze)**: 원본 W₀는 학습하지 않습니다. B와 A만 업데이트합니다.
- **초기화**: B는 0으로, A는 랜덤으로 초기화합니다. 따라서 학습 시작 시 ΔW=0입니다.
- **추론 병합**: 학습 후 W₀ + BA를 사전에 계산해두면 추론 속도 저하가 없습니다.

## 수식

```
출력 = W₀x + ΔWx = W₀x + B(Ax)
파라미터 절감 = d×k → d×r + r×k  (r ≪ d, k일 때 극적으로 줄어듦)
```

## 결과 해석 체크리스트

- `compression_pct`가 높을수록 파라미터를 더 많이 절감합니다.
- `rank`가 낮을수록 절감률이 높지만, 표현력이 제한될 수 있습니다.
- `output_diff_mean_abs`가 0에 가까운 것은 학습 전 상태(B=0)이기 때문입니다.

## 웹앱 실습 순서

1. `chapter114`를 실행합니다.
2. `summary_table`에서 랭크별 파라미터 수를 비교합니다.
3. `docs/13.md`의 LoRA 수식 설명과 대조합니다.
4. `chapter115`로 이동해 Instruction Tuning 실습을 이어갑니다.

## 다음으로 연결할 챕터

- `chapter115` Instruction Tuning 시뮬레이션
- `chapter113` TF-IDF 텍스트 분류 (파인튜닝 전 기준선)

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=LoRA+fine+tuning+LLM+강의+한국어)
