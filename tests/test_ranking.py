# Unit tests for prediction and candidate ranking logic

import os
import sys

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.prediction import load_model, predict_candidate, predict_all_candidates
from ml.ranking import rank_candidates, calculate_candidate_score


def test_prediction_and_ranking():
    # Load model
    model = load_model()
    assert model is not None

    # Sample candidate features
    sample_candidate_a = {
        "Skills": "Python, Machine Learning, Scikit-Learn, SQL",
        "Experience (Years)": 4,
        "CGPA": 8.2,
        "Certifications Count": 3,
        "Project Count": 4,
        "Internship Experience": 1,
        "Years Since Graduation": 3,
        "Education Level": "Master's",
        "Previous Job Title": "Data Analyst",
        "Job Role": "Data Scientist",
        "Job Type": "Full-time",
    }

    sample_candidate_b = {
        "Skills": "Communication, Excel",
        "Experience (Years)": 0,
        "CGPA": 5.5,
        "Certifications Count": 0,
        "Project Count": 0,
        "Internship Experience": 0,
        "Years Since Graduation": 1,
        "Education Level": "Bachelor's",
        "Previous Job Title": None,
        "Job Role": "Software Engineer",
        "Job Type": "Internship",
    }

    pred_a = predict_candidate(sample_candidate_a, model)
    pred_b = predict_candidate(sample_candidate_b, model)

    assert "predicted_label" in pred_a
    assert "hire_probability" in pred_a
    assert 0.0 <= pred_a["hire_probability"] <= 100.0
    assert 0.0 <= pred_b["hire_probability"] <= 100.0

    cand_list = [
        {"name": "Candidate A", "hire_probability": pred_a["hire_probability"]},
        {"name": "Candidate B", "hire_probability": pred_b["hire_probability"]},
    ]

    ranked = rank_candidates(cand_list)
    assert ranked[0]["hire_probability"] >= ranked[1]["hire_probability"]
    assert ranked[0]["rank"] == 1
    assert ranked[1]["rank"] == 2


if __name__ == "__main__":
    test_prediction_and_ranking()
    print("Prediction and ranking unit tests passed successfully!")

