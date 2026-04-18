from __future__ import annotations

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

def compute_group_metrics(y_true, y_pred, groups, group_name: str) -> pd.DataFrame:
    rows = []
    group_series = pd.Series(groups)
    for group in sorted(group_series.dropna().unique()):
        mask = group_series == group
        if mask.sum() < 5:
            continue
        rows.append({
            "Variable": group_name,
            "Grupo": group,
            "N": int(mask.sum()),
            "Accuracy": accuracy_score(pd.Series(y_true)[mask].values, pd.Series(y_pred)[mask].values),
            "F1 Macro": f1_score(pd.Series(y_true)[mask].values, pd.Series(y_pred)[mask].values, average="macro", zero_division=0),
        })
    return pd.DataFrame(rows)

def summarize_fairness(df_metrics: pd.DataFrame) -> dict:
    if df_metrics.empty:
        return {"disparate_impact": None, "equalized_odds_gap": None}
    max_acc = df_metrics["Accuracy"].max()
    min_acc = df_metrics["Accuracy"].min()
    return {
        "disparate_impact": min_acc / max_acc if max_acc else 0.0,
        "equalized_odds_gap": max_acc - min_acc,
        "max_accuracy": max_acc,
        "min_accuracy": min_acc,
    }
