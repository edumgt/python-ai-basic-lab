# [초등학생 설명 주석 적용됨]
# 설명: 이 파일(또는 함수)의 목적을 설명하는 문서 문자열이에요.
"""Pandas 데이터프레임 실습 파일"""
# 설명: annotations를(을) 최신 파이썬 문법(annotations 등)을 이전 버전에서도 쓸 수 있게 해줘요.
from __future__ import annotations

# 설명: Path를(을) 파일·디렉토리 경로를 객체로 다루는 pathlib 도구를 불러와요.
from pathlib import Path

# 설명: 수치 계산(배열·행렬·통계)을 위한 NumPy 라이브러리를 불러와요.
import numpy as np
# 설명: 표(DataFrame) 형태 데이터를 다루는 Pandas 라이브러리를 불러와요.
import pandas as pd
# 설명: make_classification, make_regression를(을) 연습용 가상 데이터셋(분류·회귀용)을 생성하는 도구를 불러와요.
from sklearn.datasets import make_classification, make_regression
# 설명: IsolationForest, RandomForestClassifier를(을) 랜덤 포레스트·부스팅 등 앙상블 모델 도구를 불러와요.
from sklearn.ensemble import IsolationForest, RandomForestClassifier
# 설명: Lasso, LinearRegression, LogisticRegression, Ridge를(을) 선형 회귀·로지스틱 회귀 등 선형 모델 도구를 불러와요.
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
# 설명: KMeans를(을) K-Means 등 비지도 군집화 도구를 불러와요.
from sklearn.cluster import KMeans
# 설명: PCA를(을) PCA 등 차원 축소 도구를 불러와요.
from sklearn.decomposition import PCA
# 설명: accuracy_score, f1_score, mean_squared_error, precision_score, recall_score, roc_auc_score를(을) 정확도·F1·MSE 등 모델 평가 지표 계산 도구를 불러와요.
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, precision_score, recall_score, roc_auc_score
# 설명: KFold, cross_val_score, train_test_split를(을) 데이터 분리·교차검증 등 모델 선택 도구를 불러와요.
from sklearn.model_selection import KFold, cross_val_score, train_test_split
# 설명: Pipeline를(을) 전처리와 모델을 하나로 묶는 Pipeline 도구를 불러와요.
from sklearn.pipeline import Pipeline
# 설명: OneHotEncoder, StandardScaler를(을) 표준화·인코딩 등 데이터 전처리 도구를 불러와요.
from sklearn.preprocessing import OneHotEncoder, StandardScaler
# 설명: ColumnTransformer를(을) 컬럼별 다른 전처리를 조합하는 ColumnTransformer 도구를 불러와요.
from sklearn.compose import ColumnTransformer
# 설명: DecisionTreeClassifier를(을) 결정 트리 모델 도구를 불러와요.
from sklearn.tree import DecisionTreeClassifier
# 설명: 모델 저장·병렬 처리를 위한 joblib 라이브러리를 불러와요.
import joblib


# 설명: 'run' 함수를 정의해요.
def run() -> dict:
    # 설명: 난수 생성 시드를 고정해요 — 같은 시드이면 항상 같은 결과가 나와요.
    np.random.seed(42)
    # 설명: 챕터·주제 정보와 실습 결과를 담을 딕셔너리를 초기화해요.
    result = {"chapter": "chapter02", "topic": "Pandas 데이터프레임"}

    # 설명: 조건 ("pandas" == "numpy")이 참인지 확인해요.
    if "pandas" == "numpy":
        # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
        arr = np.array([1, 2, 3, 4, 5])
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["mean"] = float(arr.mean())
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["std"] = float(arr.std())

    # 설명: 앞 조건이 거짓이면, ("pandas" == "pandas") 조건을 확인해요.
    elif "pandas" == "pandas":
        # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
        df = pd.DataFrame({"feature": [1, 2, np.nan, 4], "target": [10, 15, 14, 20]})
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["missing_before"] = int(df["feature"].isna().sum())
        # 설명: 결측값(NaN)을 지정한 값으로 채워요.
        df["feature"] = df["feature"].fillna(df["feature"].mean())
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["missing_after"] = int(df["feature"].isna().sum())

    # 설명: 앞 조건이 거짓이면, ("pandas" == "probability") 조건을 확인해요.
    elif "pandas" == "probability":
        # 설명: 이항분포를 따르는 난수를 생성해요.
        toss = np.random.binomial(1, 0.6, size=1000)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["estimated_p"] = float(toss.mean())

    # 설명: 앞 조건이 거짓이면, ("pandas" == "linear_algebra") 조건을 확인해요.
    elif "pandas" == "linear_algebra":
        # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
        A = np.array([[2, 1], [1, 3]])
        # 설명: 파이썬 리스트·시퀀스를 NumPy 배열로 변환해요.
        b = np.array([1, 2])
        # 설명: 선형 방정식 Ax = b를 풀어 해 벡터 x를 구해요.
        x = np.linalg.solve(A, b)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["solution"] = x.round(4).tolist()

    # 설명: 앞 조건이 거짓이면, ("pandas" == "linear_regression") 조건을 확인해요.
    elif "pandas" == "linear_regression":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_regression(n_samples=120, n_features=3, noise=7, random_state=42)
        # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = LinearRegression().fit(X_train, y_train)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = model.predict(X_test)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["mse"] = float(mean_squared_error(y_test, pred))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "logistic_regression") 조건을 확인해요.
    elif "pandas" == "logistic_regression":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_classification(n_samples=180, n_features=5, n_informative=3, random_state=42)
        # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = LogisticRegression(max_iter=500).fit(X_train, y_train)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = model.predict(X_test)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["accuracy"] = float(accuracy_score(y_test, pred))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "decision_tree") 조건을 확인해요.
    elif "pandas" == "decision_tree":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_classification(n_samples=180, n_features=6, n_informative=4, random_state=42)
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X, y)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["feature_importance_sum"] = float(model.feature_importances_.sum())

    # 설명: 앞 조건이 거짓이면, ("pandas" == "random_forest") 조건을 확인해요.
    elif "pandas" == "random_forest":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_classification(n_samples=220, n_features=6, n_informative=4, random_state=42)
        # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = RandomForestClassifier(n_estimators=120, random_state=42).fit(X_train, y_train)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = model.predict(X_test)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["f1"] = float(f1_score(y_test, pred))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "kmeans") 조건을 확인해요.
    elif "pandas" == "kmeans":
        # 설명: 정규분포(평균·표준편차 지정)를 따르는 난수 배열을 생성해요.
        X = np.vstack([np.random.normal(0, 1, (40, 2)), np.random.normal(4, 1, (40, 2))])
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = KMeans(n_clusters=2, random_state=42, n_init='auto').fit(X)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["cluster_count"] = int(len(np.unique(model.labels_)))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "metrics") 조건을 확인해요.
    elif "pandas" == "metrics":
        # 설명: 실제 정답 레이블 배열을 정의해요.
        y_true = np.array([0, 1, 1, 0, 1, 0, 1, 1])
        # 설명: 모델이 예측한 레이블 배열을 정의해요.
        y_pred = np.array([0, 1, 0, 0, 1, 0, 1, 1])
        # 설명: 모델이 각 클래스에 대해 예측한 확률 배열을 정의해요.
        y_prob = np.array([0.1, 0.9, 0.4, 0.2, 0.8, 0.3, 0.7, 0.95])
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["precision"] = float(precision_score(y_true, y_pred))
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["recall"] = float(recall_score(y_true, y_pred))
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["roc_auc"] = float(roc_auc_score(y_true, y_prob))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "validation") 조건을 확인해요.
    elif "pandas" == "validation":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_classification(n_samples=200, n_features=8, n_informative=5, random_state=42)
        # 설명: K-폴드 교차검증 분할기를 생성해요.
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        # 설명: 평가 점수를 계산해서 저장해요.
        scores = cross_val_score(LogisticRegression(max_iter=500), X, y, cv=cv)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["cv_mean"] = float(scores.mean())

    # 설명: 앞 조건이 거짓이면, ("pandas" == "feature_engineering") 조건을 확인해요.
    elif "pandas" == "feature_engineering":
        # 설명: 표(DataFrame) 형태의 데이터를 df 변수에 저장해요.
        df = pd.DataFrame({
            # 설명: 이 코드를 실행해요.
            "age": [25, 30, 35, 40],
            # 설명: 이 코드를 실행해요.
            "salary": [3000, 4000, 5000, 6000],
            # 설명: 이 코드를 실행해요.
            "city": ["Seoul", "Busan", "Seoul", "Daegu"],
        # 설명: 이 코드를 실행해요.
        })
        # 설명: 컬럼 종류(수치형·범주형)별로 다른 전처리를 적용해요.
        pre = ColumnTransformer([
            # 설명: 데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요.
            ("num", StandardScaler(), ["age", "salary"]),
            # 설명: 범주형 값을 0/1 이진 벡터로 변환하는 인코더를 생성해요.
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
        # 설명: 이 코드를 실행해요.
        ])
        # 설명: 전처리 변환이 완료된 데이터를 저장해요.
        transformed = pre.fit_transform(df)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["transformed_shape"] = list(transformed.shape)

    # 설명: 앞 조건이 거짓이면, ("pandas" == "regularization") 조건을 확인해요.
    elif "pandas" == "regularization":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_regression(n_samples=100, n_features=10, noise=15, random_state=42)
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        ridge = Ridge(alpha=1.0).fit(X, y)
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        lasso = Lasso(alpha=0.1).fit(X, y)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["ridge_coef_norm"] = float(np.linalg.norm(ridge.coef_))
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["lasso_non_zero"] = int(np.count_nonzero(lasso.coef_))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "dimensionality_reduction") 조건을 확인해요.
    elif "pandas" == "dimensionality_reduction":
        # 설명: 표준 정규분포(평균 0, 표준편차 1) 난수 배열을 생성해요.
        X = np.random.randn(150, 10)
        # 설명: PCA(주성분 분석) 변환기를 생성해요.
        pca = PCA(n_components=2, random_state=42)
        # 설명: PCA로 차원을 축소한 데이터를 저장해요.
        reduced = pca.fit_transform(X)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["reduced_shape"] = list(reduced.shape)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["explained"] = float(pca.explained_variance_ratio_.sum())

    # 설명: 앞 조건이 거짓이면, ("pandas" == "outlier_detection") 조건을 확인해요.
    elif "pandas" == "outlier_detection":
        # 설명: 정규분포(평균·표준편차 지정)를 따르는 난수 배열을 생성해요.
        X = np.vstack([np.random.normal(0, 1, (100, 2)), np.array([[8, 8], [9, 9], [10, 10]])])
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = IsolationForest(contamination=0.03, random_state=42).fit(X)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = model.predict(X)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["outliers_detected"] = int((pred == -1).sum())

    # 설명: 앞 조건이 거짓이면, ("pandas" == "time_series") 조건을 확인해요.
    elif "pandas" == "time_series":
        # 설명: 1차원 시계열 데이터를 Series 형태로 저장해요.
        series = pd.Series(np.sin(np.linspace(0, 6, 60)) + np.random.normal(0, 0.1, 60))
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["ma_5_last"] = float(series.rolling(5).mean().iloc[-1])
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["lag_1_last"] = float(series.shift(1).iloc[-1])

    # 설명: 앞 조건이 거짓이면, ("pandas" == "pipeline") 조건을 확인해요.
    elif "pandas" == "pipeline":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_classification(n_samples=180, n_features=6, n_informative=4, random_state=42)
        # 설명: 전처리와 모델을 하나로 묶은 Pipeline 객체를 생성해요.
        pipe = Pipeline([
            # 설명: 데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요.
            ("scaler", StandardScaler()),
            # 설명: 로지스틱 회귀 분류 모델을 생성해요.
            ("model", LogisticRegression(max_iter=500, random_state=42)),
        # 설명: 이 코드를 실행해요.
        ])
        # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        pipe.fit(X_train, y_train)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = pipe.predict(X_test)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["accuracy"] = float(accuracy_score(y_test, pred))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "model_persistence") 조건을 확인해요.
    elif "pandas" == "model_persistence":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_regression(n_samples=100, n_features=4, noise=3, random_state=42)
        # 설명: 모델 객체를 생성하거나 학습 결과를 model 변수에 저장해요.
        model = LinearRegression().fit(X, y)
        # 설명: 모델 파일을 저장할 경로를 지정해요.
        model_path = Path(__file__).with_name("linear_model.joblib")
        # 설명: 학습된 모델을 파일에 저장해요 — 나중에 다시 불러올 수 있어요.
        joblib.dump(model, model_path)
        # 설명: 저장된 모델 파일을 불러와 loaded 변수에 저장해요.
        loaded = joblib.load(model_path)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["coef_match"] = bool(np.allclose(model.coef_, loaded.coef_))

    # 설명: 앞 조건이 거짓이면, ("pandas" == "serving") 조건을 확인해요.
    elif "pandas" == "serving":
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["message"] = "FastAPI 백엔드(app/main.py)의 /api/chapters 엔드포인트를 확인하세요."

    # 설명: 앞 조건이 거짓이면, ("pandas" == "mini_project") 조건을 확인해요.
    elif "pandas" == "mini_project":
        # 설명: 특성 행렬 X와 레이블 벡터 y를 함께 생성(또는 할당)해요.
        X, y = make_classification(n_samples=250, n_features=7, n_informative=4, random_state=42)
        # 설명: 데이터를 학습용(X_train, y_train)과 테스트용(X_test, y_test)으로 분리해요.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 설명: 전처리와 모델을 하나로 묶은 Pipeline 객체를 생성해요.
        pipe = Pipeline([
            # 설명: 데이터를 평균 0·표준편차 1로 표준화하는 스케일러를 생성해요.
            ("scaler", StandardScaler()),
            # 설명: 여러 결정 트리를 앙상블한 랜덤 포레스트 분류 모델을 생성해요.
            ("model", RandomForestClassifier(n_estimators=150, random_state=42)),
        # 설명: 이 코드를 실행해요.
        ])
        # 설명: 모델 또는 변환기를 학습 데이터로 훈련시켜요.
        pipe.fit(X_train, y_train)
        # 설명: 모델의 예측값을 pred 변수에 저장해요.
        pred = pipe.predict(X_test)
        # 설명: 계산 결과를 result 딕셔너리에 저장해요.
        result["final_accuracy"] = float(accuracy_score(y_test, pred))

    # 설명: 'result'을(를) 함수 호출 측에 반환해요.
    return result


# 설명: 이 파일을 직접 실행했을 때만 아래 코드를 수행해요.
if __name__ == "__main__":
    # 설명: 값을 정수형으로 변환해요.
    print(run())
