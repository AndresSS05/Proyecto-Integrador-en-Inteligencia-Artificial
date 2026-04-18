from src.benchmark import get_benchmark_models
from src.fairness import compute_group_metrics, summarize_fairness
from src.features import extract_sql_features, infer_difficulty_from_sql

def test_sql_feature_extraction():
    row = extract_sql_features("SELECT * FROM tabla WHERE id = 1")
    assert "has_where" in row
    assert row["has_where"] == 1

def test_infer_difficulty():
    level = infer_difficulty_from_sql("SELECT nombre FROM clientes")
    assert level in {"easy", "medium", "hard", "extra"}

def test_models_exist():
    models = get_benchmark_models()
    assert "Random Forest (Propuesto)" in models

def test_fairness_summary_keys():
    df = compute_group_metrics([0, 1, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0], ["a", "a", "a", "b", "b", "b"], "grupo")
    summary = summarize_fairness(df)
    assert "disparate_impact" in summary
    assert "equalized_odds_gap" in summary
