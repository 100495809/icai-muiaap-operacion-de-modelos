"""Run the week 1 Wine Quality experiment locally, without MLflow.

This is a small diagnostic harness for the teaching notebook. It uses the same
70/15/15 stratified split and reports validation/test metrics for candidate
pipelines, including the ExtraTrees configuration used by the notebook and an
XGBoost candidate. Test is printed only for the best validation candidate.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import xgboost
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "semana1" / "data" / "raw" / "WineQT.csv"
FEATURES = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
]
RANDOM_STATE = 42
TRAIN_SIZE = 0.70
VALIDATION_SIZE = 0.15
TEST_SIZE = 0.15
MIN_VALIDATION_F1_MACRO = 0.70


def metrics(model: Pipeline, features: pd.DataFrame, labels: pd.Series) -> dict[str, float]:
    predictions = model.predict(features)
    return {
        "f1_macro": float(f1_score(labels, predictions, average="macro", zero_division=0)),
        "f1_weighted": float(f1_score(labels, predictions, average="weighted", zero_division=0)),
        "precision_macro": float(
            precision_score(labels, predictions, average="macro", zero_division=0)
        ),
        "recall_macro": float(recall_score(labels, predictions, average="macro", zero_division=0)),
        "accuracy": float(accuracy_score(labels, predictions)),
    }


def tree_pipeline(classifier) -> Pipeline:
    return Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("model", classifier),
        ]
    )


def candidates() -> list[tuple[str, str, Pipeline]]:
    result: list[tuple[str, str, Pipeline]] = []
    for n_estimators in (300, 600):
        for min_samples_leaf in (1, 2, 3):
            result.append(
                (
                    f"extra_trees_{n_estimators}_leaf_{min_samples_leaf}",
                    "extra_trees",
                    tree_pipeline(
                        ExtraTreesClassifier(
                            n_estimators=n_estimators,
                            max_features=1.0,
                            min_samples_leaf=min_samples_leaf,
                            class_weight=None,
                            random_state=RANDOM_STATE,
                            n_jobs=-1,
                        )
                    ),
                )
            )
    result.append(
        (
            "xgboost_hist",
            "xgboost",
            tree_pipeline(
                XGBClassifier(
                    n_estimators=250,
                    max_depth=4,
                    learning_rate=0.05,
                    min_child_weight=1,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    reg_lambda=1.0,
                    objective="binary:logistic",
                    eval_metric="logloss",
                    tree_method="hist",
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                    verbosity=0,
                )
            ),
        )
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument(
        "--positive-at-least",
        type=int,
        default=6,
        help="Collapse quality into 0/1: 1 when quality is at least this value (default: 6).",
    )
    args = parser.parse_args()

    data = pd.read_csv(args.dataset)
    X = data[FEATURES]
    y = (data["quality"] >= args.positive_at_least).astype(int)
    target_description = f"quality >= {args.positive_at_least}"
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train_full,
        y_train_full,
        test_size=VALIDATION_SIZE / (TRAIN_SIZE + VALIDATION_SIZE),
        random_state=RANDOM_STATE,
        stratify=y_train_full,
    )

    rows = []
    fitted = {}
    for name, model_type, model in candidates():
        model.fit(X_train, y_train)
        validation = metrics(model, X_valid, y_valid)
        rows.append({"candidate": name, "model_type": model_type, **validation})
        fitted[name] = model

    comparison = pd.DataFrame(rows).sort_values(
        ["f1_macro", "f1_weighted", "accuracy"], ascending=False
    )
    reference_f1 = float(
        comparison.loc[comparison["candidate"] == "extra_trees_300_leaf_1", "f1_macro"].iloc[0]
    )
    assert reference_f1 >= MIN_VALIDATION_F1_MACRO, (
        "El candidato de referencia no supera el gate; revisa el split, el dataset o las versiones."
    )
    print("LOCAL RUN (MLflow disabled)")
    print(f"dataset={args.dataset}")
    print(f"target={target_description}")
    print(f"xgboost={xgboost.__version__}")
    print(
        f"split={TRAIN_SIZE:.0%}/{VALIDATION_SIZE:.0%}/{TEST_SIZE:.0%} "
        f"train:{len(X_train)} validation:{len(X_valid)} test:{len(X_test)}"
    )
    print(comparison.head(15).to_string(index=False, float_format=lambda value: f"{value:.4f}"))

    best_name = str(comparison.iloc[0]["candidate"])
    best_model = fitted[best_name]
    test_metrics = metrics(best_model, X_test, y_test)
    print(f"\nBEST VALIDATION CANDIDATE: {best_name}")
    print("TEST (opened after selecting on validation):")
    for key, value in test_metrics.items():
        print(f"{key}={value:.4f}")


if __name__ == "__main__":
    main()
