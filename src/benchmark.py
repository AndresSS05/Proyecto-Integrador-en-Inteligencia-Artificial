from __future__ import annotations

import time
from typing import Dict, Tuple

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

def get_benchmark_models() -> Dict[str, object]:
    models = {
        "Baseline: Aleatorio (Stratified)": DummyClassifier(strategy="stratified", random_state=42),
        "Baseline: Más Frecuente": DummyClassifier(strategy="most_frequent"),
        "Baseline: Árbol de Decisión": DecisionTreeClassifier(max_depth=5, random_state=42, class_weight="balanced"),
        "Regresión Logística": LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced", multi_class="multinomial"),
        "K-NN (k=7)": KNeighborsClassifier(n_neighbors=7),
        "SVM (RBF)": SVC(kernel="rbf", class_weight="balanced", random_state=42, probability=True),
        "Random Forest (Propuesto)": RandomForestClassifier(n_estimators=200, max_depth=12, class_weight="balanced", random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, max_depth=6, random_state=42, learning_rate=0.1),
    }
    try:
        from xgboost import XGBClassifier
        models["XGBoost"] = XGBClassifier(n_estimators=200, max_depth=6, random_state=42, use_label_encoder=False, eval_metric="mlogloss", n_jobs=-1)
    except Exception:
        pass
    try:
        from lightgbm import LGBMClassifier
        models["LightGBM"] = LGBMClassifier(n_estimators=200, max_depth=6, random_state=42, class_weight="balanced", verbose=-1, n_jobs=-1)
    except Exception:
        pass
    return models

def evaluate_models(models: Dict[str, object], X_train, y_train, X_val, y_val) -> Tuple[pd.DataFrame, Dict[str, object]]:
    rows = []
    fitted = {}
    for name, model in models.items():
        start = time.time()
        model.fit(X_train, y_train)
        elapsed = time.time() - start
        pred_train = model.predict(X_train)
        pred_val = model.predict(X_val)
        rows.append({
            "Modelo": name,
            "Acc Train": accuracy_score(y_train, pred_train),
            "Acc Val": accuracy_score(y_val, pred_val),
            "F1 Macro": f1_score(y_val, pred_val, average="macro"),
            "F1 Weighted": f1_score(y_val, pred_val, average="weighted"),
            "Precision Macro": precision_score(y_val, pred_val, average="macro", zero_division=0),
            "Recall Macro": recall_score(y_val, pred_val, average="macro", zero_division=0),
            "Overfit Gap": accuracy_score(y_train, pred_train) - accuracy_score(y_val, pred_val),
            "Tiempo (s)": elapsed,
        })
        fitted[name] = model
    return pd.DataFrame(rows).sort_values("F1 Macro", ascending=False).reset_index(drop=True), fitted
