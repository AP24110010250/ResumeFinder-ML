# End-to-end integration test script

import os
import sys
import fitz

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.resume_parser import extract_pdf_text
from backend.candidate_features import (
    extract_candidate_features,
    map_candidate_features,
    calculate_requirement_checks,
)
from ml.prediction import load_model, predict_candidate
from ml.ranking import rank_candidates
from backend.database import save_job_details, save_candidate, fetch_candidates


def run_e2e_test():
    # 1. Create sample test resumes as digital PDFs
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_resumes")
    os.makedirs(sample_dir, exist_ok=True)

    resumes = [
        {
            "filename": os.path.join(sample_dir, "John_Doe_Developer.pdf"),
            "text": """John Doe
Software Engineer
Email: john.doe@email.com
Experience: 6 years of experience in software development.
Education: Bachelor's in Computer Science, CGPA: 8.4
Skills: Python, Machine Learning, Scikit-Learn, SQL, Docker, Git, Algorithms
Projects: Project 1: Built candidate ranking system; Project 2: Microservices backend
Certifications: AWS Certified Solutions Architect, Certified Kubernetes Administrator
Graduated in 2020
Previous Job Title: Software Engineer
""",
        },
        {
            "filename": os.path.join(sample_dir, "Jane_Smith_Fresher.pdf"),
            "text": """Jane Smith
Data Science Graduate
Email: jane.smith@email.com
Experience: 1 year of experience as an intern.
Education: Master's in Data Science, CGPA: 7.9
Skills: Python, Pandas, NumPy, Data Visualization, Excel, Communication
Projects: Project 1: Customer churn analysis
Certifications: None
Graduated in 2024
Previous Job Title: Junior Data Scientist
""",
        },
    ]

    for r in resumes:
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 72), r["text"])
        doc.save(r["filename"])
        doc.close()

    # 2. Simulate HR requirements
    job_req = {
        "job_title": "Senior Python ML Engineer",
        "job_role": "Data Scientist",
        "job_type": "Full-time",
        "education_requirement": "Bachelor's",
        "min_experience": 3,
        "required_skills": "Python, Machine Learning, Scikit-Learn, Docker",
        "job_description": "Looking for an experienced Python and Machine Learning engineer.",
    }

    # 3. Process resumes end-to-end
    model = load_model()
    candidates_processed = []

    for r in resumes:
        with open(r["filename"], "rb") as f:
            pdf_bytes = f.read()
        text, msg = extract_pdf_text(pdf_bytes)
        assert msg == "Success"

        ext = extract_candidate_features(text, os.path.basename(r["filename"]))
        model_feats = map_candidate_features(ext, job_req)
        pred = predict_candidate(model_feats, model)
        req_checks = calculate_requirement_checks(ext, job_req)

        cand_record = {
            "name": ext["Name"],
            "filename": os.path.basename(r["filename"]),
            "extracted_features": ext,
            "model_features": model_feats,
            "predicted_label": pred["predicted_label"],
            "hire_probability": pred["hire_probability"],
            "experience_met": req_checks["experience_met"],
            "education_met": req_checks["education_met"],
            "matched_skills": req_checks["matched_skills"],
            "missing_skills": req_checks["missing_skills"],
            "skill_match_pct": req_checks["skill_match_pct"],
            "completeness_score": req_checks["completeness_score"],
            "status": "Pending",
        }
        candidates_processed.append(cand_record)

    ranked = rank_candidates(candidates_processed)
    print("--- E2E Candidate Ranking Results ---")
    for c in ranked:
        print(
            f"Rank #{c['rank']}: {c['name']} | Hire Prob: {c['hire_probability']}% | "
            f"Decision: {c['predicted_label']} | Exp Met: {c['experience_met']} | "
            f"Skill Match: {c['skill_match_pct']}% | Missing: {c['missing_skills']}"
        )

    # 4. Test Database storage
    job_id = save_job_details(job_req)
    for c in ranked:
        save_candidate(c, job_id=job_id)

    db_candidates = fetch_candidates(job_id=job_id)
    print(f"Database successfully saved and fetched {len(db_candidates)} candidate records.")
    print("All end-to-end integration workflows passed!")


if __name__ == "__main__":
    run_e2e_test()

