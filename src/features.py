from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

from src.config import DIFF_MAP, SQL_KEYWORDS

WH_WORDS = {"what", "which", "who", "where", "when", "how", "whose"}
AGG_WORDS = {"many", "much", "average", "total", "sum", "count", "maximum", "minimum", "highest", "lowest", "most", "least"}
COMP_WORDS = {"more", "less", "greater", "smaller", "between", "except", "not", "without", "other", "different", "same"}
ORDER_WORDS = {"order", "sort", "rank", "list", "top", "bottom", "first", "last"}

def extract_sql_features(sql: str) -> dict[str, Any]:
    sql_upper = str(sql).upper()
    return {
        "has_join": int("JOIN" in sql_upper),
        "has_subquery": int("SELECT" in sql_upper[sql_upper.find("FROM"):] if "FROM" in sql_upper else False),
        "has_group_by": int("GROUP BY" in sql_upper),
        "has_order_by": int("ORDER BY" in sql_upper),
        "has_having": int("HAVING" in sql_upper),
        "has_where": int("WHERE" in sql_upper),
        "has_distinct": int("DISTINCT" in sql_upper),
        "has_limit": int("LIMIT" in sql_upper),
        "has_union": int("UNION" in sql_upper),
        "has_intersect": int("INTERSECT" in sql_upper),
        "has_except": int("EXCEPT" in sql_upper),
        "has_count": int("COUNT(" in sql_upper),
        "has_avg": int("AVG(" in sql_upper),
        "has_sum": int("SUM(" in sql_upper),
        "has_max_min": int("MAX(" in sql_upper or "MIN(" in sql_upper),
        "join_count": sql_upper.count("JOIN"),
        "sql_length": len(sql_upper),
        "sql_token_count": len(sql_upper.split()),
        "clause_count": sum(1 for kw in ["SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "HAVING", "LIMIT"] if kw in sql_upper),
    }

def infer_difficulty_from_sql(sql: str) -> str:
    sql_u = str(sql).upper()
    joins = sql_u.count("JOIN")
    subq = sql_u.count("SELECT") - 1
    has_gb = "GROUP BY" in sql_u
    has_hav = "HAVING" in sql_u
    has_set = any(op in sql_u for op in ["UNION", "INTERSECT", "EXCEPT"])
    has_nest = subq > 0
    if has_set or (has_nest and has_hav) or (joins >= 2 and has_nest):
        return "extra"
    if has_nest or (joins >= 2 and has_gb) or has_hav:
        return "hard"
    if joins >= 1 or has_gb or "ORDER BY" in sql_u:
        return "medium"
    return "easy"

def extract_linguistic_features(question: str) -> dict[str, Any]:
    if pd.isna(question):
        return {}
    q_lower = str(question).lower()
    tokens = word_tokenize(q_lower)
    words = [t for t in tokens if t.isalpha()]
    stop_words_en = set(stopwords.words("english"))
    non_stop = [w for w in words if w not in stop_words_en]
    return {
        "nl_word_count": len(words),
        "nl_unique_words": len(set(words)),
        "nl_lexical_diversity": len(set(words)) / max(len(words), 1),
        "nl_non_stop_ratio": len(non_stop) / max(len(words), 1),
        "nl_avg_word_length": float(np.mean([len(w) for w in words])) if words else 0.0,
        "nl_has_number": int(any(t.isdigit() for t in tokens)),
        "nl_has_wh_word": int(any(w in WH_WORDS for w in words)),
        "nl_has_agg_word": int(any(w in AGG_WORDS for w in words)),
        "nl_has_comparison_word": int(any(w in COMP_WORDS for w in words)),
        "nl_has_order_word": int(any(w in ORDER_WORDS for w in words)),
        "nl_has_join_signal": int(any(w in {"across", "between", "with", "related", "linked"} for w in words)),
        "nl_comma_count": q_lower.count(","),
        "nl_and_count": q_lower.count(" and "),
        "nl_or_count": q_lower.count(" or "),
    }

def extract_advanced_sql_features(sql: str) -> dict[str, Any]:
    sql_u = str(sql).upper()
    from_matches = re.findall(r"FROM\\s+(\\w+)", sql_u)
    join_matches = re.findall(r"JOIN\\s+(\\w+)", sql_u)
    tables_referenced = len(set(from_matches + join_matches))
    where_conditions = 0
    if "WHERE" in sql_u:
        where_part = sql_u.split("WHERE")[1].split("GROUP BY")[0].split("ORDER BY")[0]
        where_conditions = where_part.count(" AND ") + where_part.count(" OR ") + 1
    nesting_depth = sql_u.count("(SELECT")
    total_keywords = sum(sql_u.count(keyword) for keyword in SQL_KEYWORDS)
    return {
        "sql_nesting_depth": nesting_depth,
        "sql_tables_referenced": tables_referenced,
        "sql_where_conditions": where_conditions,
        "sql_total_keywords": total_keywords,
    }

def build_feature_dataframe(df_all: pd.DataFrame) -> pd.DataFrame:
    tqdm.pandas(desc="Extrayendo features SQL")
    sql_features = df_all["query"].progress_apply(extract_sql_features)
    df_sql = pd.DataFrame(sql_features.tolist())

    tqdm.pandas(desc="Extrayendo features lingüísticas")
    ling_features = df_all["question"].progress_apply(extract_linguistic_features)
    df_ling = pd.DataFrame(ling_features.tolist())

    tqdm.pandas(desc="Extrayendo features SQL avanzadas")
    adv_features = df_all["query"].progress_apply(extract_advanced_sql_features)
    df_adv = pd.DataFrame(adv_features.tolist())

    df = pd.concat([df_all.reset_index(drop=True), df_sql, df_ling, df_adv], axis=1)
    df["question_length"] = df["question"].astype(str).apply(len)
    df["question_word_count"] = df["question"].astype(str).apply(lambda x: len(x.split()))
    df["complexity_score"] = (
        df["has_join"] * 2
        + df["has_subquery"] * 3
        + df["has_group_by"] * 1.5
        + df["has_having"] * 2
        + df["has_union"] * 2.5
        + df["has_intersect"] * 2.5
        + df["has_except"] * 2.5
        + df["has_distinct"] * 1
        + df["join_count"] * 1
    )
    df["ratio_nl_sql_length"] = df["question_length"] / df["sql_length"].replace(0, np.nan)
    df["interaction_score"] = df["nl_word_count"] * (1 + df["has_join"] + df["has_subquery"])
    df["sql_complexity_per_word"] = df["complexity_score"] / df["question_word_count"].replace(0, np.nan)
    df["difficulty"] = df["query"].apply(infer_difficulty_from_sql)
    df["difficulty_encoded"] = df["difficulty"].map(DIFF_MAP)
    df["length_group"] = pd.cut(df["question_word_count"], bins=[-1, 10, 15, float("inf")], labels=["corta", "media", "larga"])
    return df.fillna(0)
