from __future__ import annotations

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import learning_curve
from sklearn.tree import DecisionTreeClassifier

def run_learning_curve_diagnostics(X_train, y_train) -> pd.DataFrame:
    models = {
        "Árbol de Decisión (max_depth=5)": DecisionTreeClassifier(max_depth=5, random_state=42, class_weight="balanced"),
        "Random Forest (Propuesto)": RandomForestClassifier(n_estimators=200, max_depth=12, class_weight="balanced", random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=200, max_depth=6, random_state=42, learning_rate=0.1),
        "Regresión Logística": LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced", multi_class="multinomial"),
    }
    rows = []
    for name, model in models.items():
        train_sizes_abs, train_scores, val_scores = learning_curve(
            model,
            X_train,
            y_train,
            train_sizes=[0.1, 0.3, 0.5, 0.7, 1.0],
            cv=5,
            scoring="f1_macro",
            n_jobs=-1,
        )
        rows.append({
            "Modelo": name,
            "Train Final": train_scores.mean(axis=1)[-1],
            "Val Final": val_scores.mean(axis=1)[-1],
            "Gap": train_scores.mean(axis=1)[-1] - val_scores.mean(axis=1)[-1],
        })
    return pd.DataFrame(rows)

def evaluate_depth_sweep(X_train, y_train, X_val, y_val) -> pd.DataFrame:
    rows = []
    for depth in range(2, 25, 2):
        model = RandomForestClassifier(n_estimators=100, max_depth=depth, class_weight="balanced", random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        train_f1 = f1_score(y_train, model.predict(X_train), average="macro")
        val_f1 = f1_score(y_val, model.predict(X_val), average="macro")
        rows.append({
            "depth": depth,
            "train_f1": train_f1,
            "val_f1": val_f1,
            "gap": train_f1 - val_f1,
        })
    return pd.DataFrame(rows)
