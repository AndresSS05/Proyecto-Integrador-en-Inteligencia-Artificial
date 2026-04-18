from __future__ import annotations

DIFF_MAP = {"easy": 0, "medium": 1, "hard": 2, "extra": 3}
DIFF_MAP_INV = {v: k for k, v in DIFF_MAP.items()}

NUMERIC_FEATURES = [
    "nl_word_count", "nl_unique_words", "nl_lexical_diversity",
    "nl_non_stop_ratio", "nl_avg_word_length", "nl_has_number",
    "nl_has_wh_word", "nl_has_agg_word", "nl_has_comparison_word",
    "nl_has_order_word", "nl_has_join_signal",
    "sql_token_count", "sql_length", "clause_count", "join_count",
    "sql_nesting_depth", "sql_tables_referenced", "sql_where_conditions",
    "sql_total_keywords", "complexity_score",
    "has_join", "has_subquery", "has_group_by", "has_order_by",
    "has_having", "has_where", "has_distinct", "has_union",
    "has_count", "has_avg", "has_sum", "has_max_min",
    "ratio_nl_sql_length", "interaction_score", "sql_complexity_per_word",
]

SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN",
    "OUTER JOIN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "UNION",
    "INTERSECT", "EXCEPT", "DISTINCT", "COUNT", "SUM", "AVG", "MAX", "MIN",
    "NOT IN", "IN", "EXISTS", "BETWEEN", "LIKE", "IS NULL", "IS NOT NULL",
    "ASC", "DESC"
]
