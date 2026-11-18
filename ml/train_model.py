# Random Forest Model Training Pipeline

import os
import sys
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    DATASET_PATH,
    MODEL_PATH,
    TARGET_COLUMN,
    TEXT_FEATURES,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    FEATURE_COLUMNS,
)


def load_dataset():
    # 1) Load the dataset from CSV
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    return df


def select_features(df):
    # 2) Select the features and separate the target variable
    X = df[FEATURE_COLUMNS].copy()
    X["Skills"] = X["Skills"].fillna("")
    y = df[TARGET_COLUMN].copy()
    return X, y


def split_dataset(X, y):
    # 3) Split dataset: exactly 70% Train (2100), 15% Val (450), 15% Test (450) with stratification
    # First split off 450 rows for test set
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X,
        y,
        test_size=450,
        random_state=42,
        stratify=y,
    )

    # Split remaining 2550 rows into exactly 2100 train and 450 val
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=450,
        random_state=42,
        stratify=y_train_val,
    )

    return X_train, X_val, X_test, y_train, y_val, y_test, X_train_val, y_train_val


def build_pipeline():
    # 4) Build ColumnTransformer and Random Forest pipeline
    # Numerical preprocessor
    numerical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    # Categorical preprocessor
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    # Text preprocessor for Skills (TfidfVectorizer works directly on 1D series / column name)
    text_transformer = TfidfVectorizer(
        max_features=150,
        token_pattern=r"(?u)\b\w+[\w\+\#\-\/]*\b"
    )

    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, NUMERICAL_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
            ("text", text_transformer, "Skills"),
        ]
    )

    # Single Random Forest Classifier with tuned hyperparameters
    full_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    max_features=0.3,
                    random_state=42,
                ),
            ),
        ]
    )

    return full_pipeline


def evaluate_model(model, X_eval, y_eval, dataset_name="Validation"):
    # 5) Evaluate the model performance
    predictions = model.predict(X_eval)
    acc = accuracy_score(y_eval, predictions)
    report = classification_report(y_eval, predictions)
    matrix = confusion_matrix(y_eval, predictions)

    print(f"=== {dataset_name} Evaluation ===")
    print(f"Accuracy: {acc:.4f}\n")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(matrix)
    print("===============================\n")

    return acc, report, matrix


def save_model(model):
    # 6) Save fitted model pipeline with joblib
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model pipeline successfully saved to {MODEL_PATH}")


def train_model():
    # Execute complete training workflow
    print("Loading dataset...")
    df = load_dataset()
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    X, y = select_features(df)
    X_train, X_val, X_test, y_train, y_val, y_test, X_train_val, y_train_val = split_dataset(X, y)

    print(f"Training set:   {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set:       {X_test.shape[0]} samples")

    # Step A: Build pipeline and fit on training data
    print("\nBuilding pipeline and fitting on Training set...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    # Step B: Evaluate on validation set
    evaluate_model(pipeline, X_val, y_val, dataset_name="Validation")

    # Step C: Retrain on combined Train + Validation (2,550 samples)
    print("Retraining final pipeline on combined Training + Validation data...")
    final_pipeline = build_pipeline()
    final_pipeline.fit(X_train_val, y_train_val)

    # Step D: Final evaluation once on untouched Test set
    print("Performing final evaluation on untouched Test data...")
    evaluate_model(final_pipeline, X_test, y_test, dataset_name="Test (Final)")

    # Step E: Save model pipeline
    save_model(final_pipeline)

    return final_pipeline


if __name__ == "__main__":
    train_model()
