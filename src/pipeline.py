from __future__ import annotations

import nltk
import numpy as np
import pandas as pd
from datasets import load_dataset
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from src.config import NUMERIC_FEATURES
from src.features import build_feature_dataframe

def load_spider_dataset() -> pd.DataFrame:
    for package in [
        "punkt",
        "punkt_tab",
        "stopwords",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng",
    ]:
        nltk.download(package, quiet=True)

    dataset = load_dataset("xlangai/spider", trust_remote_code=True)
    df_train = dataset["train"].to_pandas()
    df_val = dataset["validation"].to_pandas()
    df_all = pd.concat([df_train, df_val], ignore_index=True)
    df_all["split"] = ["train"] * len(df_train) + ["validation"] * len(df_val)
    return df_all

def build_train_validation_matrices(df_all: pd.DataFrame):
    numeric_features = [f for f in NUMERIC_FEATURES if f in df_all.columns]
    df_train = df_all[df_all["split"] == "train"].copy()
    df_val = df_all[df_all["split"] == "validation"].copy()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )

    text_transformer = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(max_features=500, ngram_range=(1, 2), min_df=3, max_df=0.95, sublinear_tf=True, strip_accents="unicode", lowercase=True)),
            ("pca_text", PCA(n_components=50, random_state=42)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("text", text_transformer, "question"),
        ],
        remainder="drop",
    )

    y_train = df_train["difficulty_encoded"]
    y_val = df_val["difficulty_encoded"]

    X_train = preprocessor.fit_transform(df_train)
    X_val = preprocessor.transform(df_val)

    if hasattr(X_train, "toarray"):
        X_train = X_train.toarray()
        X_val = X_val.toarray()

    X_train = np.nan_to_num(X_train, nan=0.0, posinf=0.0, neginf=0.0)
    X_val = np.nan_to_num(X_val, nan=0.0, posinf=0.0, neginf=0.0)
    return X_train, X_val, y_train, y_val, df_train, df_val, preprocessor

def build_feature_dataframe_from_source() -> pd.DataFrame:
    return build_feature_dataframe(load_spider_dataset())
