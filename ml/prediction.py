# Candidate prediction using the trained Random Forest pipeline

import os
import sys
import joblib
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import MODEL_PATH, FEATURE_COLUMNS


def load_model(model_path=MODEL_PATH):
    # Load the saved model pipeline
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at {model_path}. Please train the model first by running: python -m ml.train_model"
        )
    model = joblib.load(model_path)
    return model


def get_hire_class_index(model):
    # Dynamically find the index corresponding to 'Hire' in model.classes_
    classes = list(model.classes_)
    if "Hire" in classes:
        return classes.index("Hire")
    return 0


def predict_candidate(model_features, model):
    # Predict hire probability for a single candidate feature dictionary
    # 1) Build a 1-row DataFrame with the exact training feature columns
    row_data = {}
    for col in FEATURE_COLUMNS:
        row_data[col] = [model_features.get(col, None)]

    df_sample = pd.DataFrame(row_data)

    # 2) Predict probability and class
    hire_idx = get_hire_class_index(model)
    probabilities = model.predict_proba(df_sample)[0]
    hire_probability = float(probabilities[hire_idx]) * 100.0
    predicted_label = model.predict(df_sample)[0]

    return {
        "predicted_label": predicted_label,
        "hire_probability": round(hire_probability, 2),
    }


def predict_all_candidates(candidates_list, model=None):
    # Generate predictions for all candidates in the list
    if model is None:
        model = load_model()

    predicted_candidates = []
    for candidate in candidates_list:
        model_input = candidate.get("model_features", {})
        pred_result = predict_candidate(model_input, model)

        # Merge prediction into candidate record
        cand_copy = dict(candidate)
        cand_copy["predicted_label"] = pred_result["predicted_label"]
        cand_copy["hire_probability"] = pred_result["hire_probability"]
        predicted_candidates.append(cand_copy)

    return predicted_candidates
