# 📌 주식에서 로봇 관련주 vs 반도체 관련주

## 구분 기준
- **로봇 관련주**: 로봇 완성품, 감속기, 센서, 제어기 등 핵심 부품을 생산하는 기업  
- **반도체 관련주**: GPU, NPU, 메모리, 전력 반도체 등 첨단 기술을 가능하게 하는 칩을 생산하는 기업  

| 구분 | 로봇 관련주 | 반도체 관련주 |
|------|-------------|---------------|
| 핵심 제품 | 로봇 완성품, 감속기, 센서, 제어기 | GPU, NPU, 메모리, 전력 반도체 |
| 대표 기업 | 레인보우로보틱스, 두산로보틱스, 유진로봇, SPG | 삼성전자, SK하이닉스, 엔비디아, AMD |
| 투자 포인트 | 산업·서비스 로봇 수요 증가 | AI·클라우드·자율주행 확산 |
| 리스크 | 기술 국산화 속도, 글로벌 경쟁 | 공급망 불안, 사이클 변동성 |

---

# 📌 ML/DL 알고리즘으로 분류하기

## 활용 가능한 알고리즘
- **로지스틱 회귀**: 단순 이진 분류에 적합  
- **랜덤 포레스트**: 다양한 특징 반영 가능  
- **SVM**: 고차원 텍스트 데이터 분류에 강력  
- **딥러닝 기반 모델**  
  - RNN/LSTM: 시퀀스 데이터 분석  
  - CNN: 텍스트 패턴 자동 추출  
  - Transformer (BERT, GPT): 문맥적 이해 기반 분류  

---

# 📌 PyTorch + BERT 예시 코드

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

texts = ["이 회사는 산업용 로봇과 감속기를 생산합니다.", "이 기업은 GPU와 메모리 반도체를 개발합니다."]
labels = [0, 1]  # 0=로봇, 1=반도체

inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
outputs = model(**inputs)
