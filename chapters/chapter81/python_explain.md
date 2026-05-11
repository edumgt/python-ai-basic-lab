# Python 쉬운 설명 (chapter81)

이 문서는 개발자도 따라할 수 있도록, 폴더 안 Python 파일을 아주 쉽게 설명해요.

## 먼저 기억해요
- `python 파일이름.py` 로 실행해요.
- 에러가 나면 메시지를 읽고 천천히 한 줄씩 확인해요.
- `run()` 함수가 있으면 그 함수가 핵심 실습이에요.

---

## 🧠 NLP(자연어 처리)란 무엇인가요?

**NLP(Natural Language Processing, 자연어 처리)** 는 컴퓨터가 사람이 쓰는 말(문장, 단어)을 이해하고 처리할 수 있게 만드는 AI 분야예요.

컴퓨터는 숫자만 이해해요. 그래서 문장을 그냥 넣으면 컴퓨터가 뭔지 몰라요.
"AI class is fun" → ❌ 컴퓨터가 바로 처리할 수 없음

그래서 NLP의 첫 번째 목표는 **문장을 숫자로 바꾸는 것**이에요!

---

## 📖 핵심 개념 이해하기

### 1. 토큰화(Tokenization) — 문장을 단어로 쪼개기

문장을 가장 작은 단위인 **토큰(token)** 으로 나누는 작업이에요.
보통 영어는 공백(space)을 기준으로, 한국어는 형태소 단위로 나눠요.

```
"AI class is fun" → ["ai", "class", "is", "fun"]
```

이 코드에서는 `_tokenize()` 함수가 이 역할을 해요:
- 소문자로 변환 (`.lower()`)
- 특수문자 제거 (`.replace(".", "")` 등)
- 공백으로 분리 (`.split()`)

### 2. 단어 사전(Vocabulary) — 등장한 단어 전체 목록 만들기

여러 문장에 나온 단어를 모두 모아 중복 없이 정렬한 목록이에요.

```
문장들: ["AI class is fun", "Python class is fun", "AI and Python are useful"]
단어 사전: ["ai", "and", "are", "class", "fun", "is", "python", "useful"]
```

단어 사전이 있어야 문장을 고정된 크기의 숫자 배열로 바꿀 수 있어요.

### 3. 카운트 벡터(Count Vector) — 단어 등장 횟수로 문장 표현하기

**Bag-of-Words(BoW)** 라고도 불러요. 단어 사전의 각 단어가 문장에 몇 번 나왔는지 세어 숫자 배열로 만들어요.

```
단어 사전: ["ai", "and", "are", "class", "fun", "is", "python", "useful"]
문장: "AI class is fun" → [1, 0, 0, 1, 1, 1, 0, 0]
문장: "Python class is fun" → [0, 0, 0, 1, 1, 1, 1, 0]
문장: "AI and Python are useful" → [1, 1, 1, 0, 0, 0, 1, 1]
```

이제 문장이 숫자 배열이 됐어요! 컴퓨터(ML 모델)가 처리할 수 있는 형태예요.

---

## 파일별 설명

### practice.py
- 이 파일은: 텍스트 데이터 입문 실습 파일
- 중요한 함수: `_tokenize`, `run`
- 사용하는 도구: `__future__`, `collections`
- 직접 해보기: `python practice.py` 실행 후 결과를 읽어보세요.

#### 코드 흐름 단계별 설명

**① 문장 준비**
```python
sentences = [
    "AI class is fun",
    "Python class is fun",
    "AI and Python are useful",
]
```
분석할 문장 3개를 준비해요.

**② 토큰화 — 각 문장을 단어 목록으로 변환**
```python
tokenized = [_tokenize(s) for s in sentences]
# → [["ai","class","is","fun"], ["python","class","is","fun"], ["ai","and","python","are","useful"]]
```

**③ 단어 사전 구성 — 중복 없이 전체 단어 모으기**
```python
vocab = sorted({token for sent in tokenized for token in sent})
# → ["ai", "and", "are", "class", "fun", "is", "python", "useful"]
```
`set`으로 중복을 제거하고, `sorted`로 알파벳 순서로 정렬해요.

**④ 카운트 벡터 생성 — 각 문장을 숫자 배열로**
```python
cnt = Counter(sent)  # 단어별 등장 횟수 세기
vectors.append([cnt[word] for word in vocab])  # 사전 순서대로 배열 만들기
```
`Counter`는 단어가 몇 번 나왔는지 자동으로 세어주는 도구예요.

---

## ⚠️ Bag-of-Words의 한계도 알아두세요

카운트 벡터는 단순하고 강력하지만 단점도 있어요:
- **순서 무시**: "나는 밥을 좋아해"와 "밥은 나를 좋아해"가 같은 벡터가 될 수 있어요.
- **의미 무시**: "좋다"와 "훌륭하다"가 다른 단어로 취급돼요.
- **희소 벡터**: 단어 사전이 커질수록 대부분의 값이 0이 돼요.

이런 한계를 보완하는 기법으로 **TF-IDF**, **Word2Vec**, **BERT** 등이 있어요.

---

## 한 줄 정리
문장을 토큰으로 쪼개고, 단어 사전을 만들고, 등장 횟수를 세면 → 숫자 배열(카운트 벡터)이 돼서 ML 모델이 처리할 수 있어요.

---

## 🎬 유튜브 동영상 찾아보기

- [관련 유튜브 동영상 검색하기](https://www.youtube.com/results?search_query=python+ai+basic+lab+chapter81+%EC%84%A4%EB%AA%85)
