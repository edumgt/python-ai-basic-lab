# 📚 Qdrant 벡터 시각화 튜토리얼

## 1️⃣ Qdrant에서 벡터 추출
- Qdrant는 REST API와 gRPC를 지원합니다.  
- 가장 간단한 방법은 REST API를 이용해 컬렉션에서 벡터를 가져오는 것입니다.

```bash
curl -X POST "http://localhost:6333/collections/my_collection/points/scroll" \
  -H "Content-Type: application/json" \
  -d '{"limit": 100}'
응답 JSON에서 "vector" 필드를 추출하면 됩니다.

2️⃣ Python으로 벡터 가져오기
python
import requests

resp = requests.post("http://localhost:6333/collections/my_collection/points/scroll",
                     json={"limit": 200})
points = resp.json()["result"]["points"]

vectors = [p["vector"] for p in points]
3️⃣ 차원 축소 (PCA, t-SNE, UMAP)
벡터는 보통 512차원 이상이므로 그대로는 시각화 불가합니다.
대표적인 차원 축소 기법:

PCA: 빠르고 선형적인 축소

t-SNE: 군집 구조를 잘 보여줌

UMAP: 대규모 데이터에 효율적

python
import numpy as np
from sklearn.decomposition import PCA

X = np.array(vectors)
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)
4️⃣ 시각화 (Matplotlib)
python
import matplotlib.pyplot as plt

plt.scatter(X_reduced[:,0], X_reduced[:,1], alpha=0.7)
plt.title("Qdrant Vectors (PCA 2D)")
plt.show()
5️⃣ 고급 시각화 (t-SNE / UMAP)
python
from sklearn.manifold import TSNE

X_tsne = TSNE(n_components=2, random_state=42).fit_transform(X)

plt.scatter(X_tsne[:,0], X_tsne[:,1], alpha=0.7, c="blue")
plt.title("Qdrant Vectors (t-SNE 2D)")
plt.show()
✅ 요약
Qdrant → REST API로 벡터 추출

차원 축소(PCA, t-SNE, UMAP) → 2D/3D 변환

Matplotlib/Seaborn → 산점도 시각화

이렇게 하면 벡터 DB의 실제 데이터를 시각적으로 탐색할 수 있습니다. 특히 t-SNE나 UMAP을 쓰면 문서/이미지/텍스트 간의 의미적 유사도가 잘 드러납니다.

벡터 DB는 단순한 저장소가 아니라, 내부적으로 근사 최근접 이웃(ANN, Approximate Nearest Neighbor) 알고리즘을 사용합니다. 이 알고리즘 덕분에 다음과 같은 과정이 가능해집니다.

임베딩(Embedding): 텍스트, 이미지 등을 숫자 배열(벡터)로 변환합니다. (이 과정은 별도의 ML 모델이 수행)

인덱싱(Indexing): 벡터들을 공간상에 잘 배치합니다. 이때 클러스터링 기술이 사용됩니다.

검색(Search): "이거랑 비슷한 거 찾아줘"라고 요청하면 분류나 추천의 근거가 되는 데이터를 내놓습니다.

3. 핵심 차이점 요약
모델 (Classification, Regression 등): "이 데이터는 A야", "값은 100이야"라고 판단하는 두뇌.

벡터 DB: 그 판단을 내리기 위해 수많은 과거 데이터를 빛의 속도로 비교/대조해주는 도구.

따라서 벡터 DB가 이 기능들을 모두 '포함'한다기보다는, 현대 머신러닝 시스템에서 위 기능들을 실시간으로 대규모 서비스에 적용하기 위해 반드시 필요한 '엔진' 역할을 한다고 보시는 것이 정확합니다.
