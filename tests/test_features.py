# Unit tests for text preprocessor, skill extractor and candidate feature extraction

import os
import sys

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.text_preprocessor import clean_text, tokenize_text, remove_stopwords, normalize_text
from backend.skill_extractor import extract_skills, match_skills, find_missing_skills
from backend.candidate_features import extract_candidate_features, calculate_requirement_checks


def test_text_preprocessing():
    # Test cleaning text and removing stopwords
    raw_text = "Experienced with Python, Machine Learning at https://example.com and C++!"
    cleaned = clean_text(raw_text)
    assert "https" not in cleaned
    assert "python" in cleaned
    assert "c++" in cleaned

    tokens = tokenize_text(cleaned)
    no_stops = remove_stopwords(tokens)
    assert "with" not in no_stops
    assert "python" in no_stops


def test_skill_extraction():
    # Test skill dictionary extraction and boundary matching
    sample_text = "Proficient in Python, SQL, Docker, C++, Machine Learning and Scikit-Learn. Also handled basic customer support."
    skills = extract_skills(sample_text)
    assert "Python" in skills
    assert "SQL" in skills
    assert "Docker" in skills
    assert "C++" in skills
    assert "Machine Learning" in skills
    assert "Scikit-Learn" in skills
    # Ensure 'c' or 'r' alone is not falsely matched from 'customer'
    assert "C" not in skills

    # Test matching and missing
    req_skills = ["Python", "Docker", "Kubernetes"]
    matched = match_skills(skills, req_skills)
    missing = find_missing_skills(skills, req_skills)

    assert "Python" in matched
    assert "Docker" in matched
    assert "Kubernetes" in missing


def test_candidate_features_and_checks():
    # Test feature extraction and requirements checking
    resume_sample = """
    Alice Johnson
    Email: alice@example.com
    Experience: 5 years of experience in Software Engineering
    Education: Master's in Computer Science, CGPA: 8.5
    Skills: Python, Java, Docker, Git, SQL
    Projects: Project 1: E-commerce platform, Project 2: Search engine
    Graduated in 2021
    """

    features = extract_candidate_features(resume_sample, "alice_resume.pdf")
    assert features["Name"] == "Alice Johnson"
    assert features["Experience (Years)"] == 5
    assert features["Education Level"] == "Master's"
    assert features["CGPA"] == 8.5

    job_req = {
        "min_experience": 3,
        "education_requirement": "Bachelor's",
        "required_skills": "Python, Docker, AWS",
    }

    checks = calculate_requirement_checks(features, job_req)
    assert checks["experience_met"] is True
    assert checks["education_met"] is True
    assert "Python" in checks["matched_skills"]
    assert "Docker" in checks["matched_skills"]
    assert "AWS" in checks["missing_skills"]


if __name__ == "__main__":
    test_text_preprocessing()
    test_skill_extraction()
    test_candidate_features_and_checks()
    print("All NLP and candidate feature tests passed successfully!")
