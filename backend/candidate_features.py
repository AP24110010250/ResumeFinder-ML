# Candidate feature extraction from resume text and metadata

import re
import datetime
from backend.skill_extractor import extract_skills

# Predefined job title patterns matching dataset categories
KNOWN_JOB_TITLES = [
    "Business Analyst",
    "HR Assistant",
    "Junior Data Scientist",
    "Data Analyst",
    "Project Manager",
    "Administrative Assistant",
    "Junior Developer",
    "Social Media Specialist",
    "Research Assistant",
    "HR Generalist",
    "Operations Coordinator",
    "Backend Developer",
    "Marketing Coordinator",
    "SEO Analyst",
    "Data Engineer",
    "Associate Product Manager",
    "Recruiting Coordinator",
    "Digital Marketer",
    "Software Engineer",
    "Frontend Developer",
]


def extract_candidate_name(text, filename=""):
    # Extract candidate name from resume text or filename
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # First attempt: First non-empty line of the resume
    if lines:
        first_line = lines[0]
        # Check if first line looks like a name (2 to 4 words, alphabetic)
        words = first_line.split()
        if 2 <= len(words) <= 4 and all(re.match(r"^[A-Za-z\.\'-]+$", w) for w in words):
            return first_line

    # Second attempt: Derive from filename if available (e.g. John_Doe_Resume.pdf)
    if filename:
        clean_name = re.sub(r"(\.pdf|_resume|resume)", "", filename, flags=re.IGNORECASE)
        clean_name = clean_name.replace("_", " ").replace("-", " ").strip()
        if clean_name:
            return clean_name.title()

    return "Candidate"


def extract_experience_years(text):
    # Extract total years of professional experience
    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)",
        r"(?:experience|exp)\s*:\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:in|as|working)",
    ]

    for pat in patterns:
        match = re.search(pat, text, flags=re.IGNORECASE)
        if match:
            try:
                val = float(match.group(1))
                return int(round(val))
            except ValueError:
                pass

    return 0


def extract_education_level(text):
    # Identify education level: PhD, Master's, or Bachelor's
    lower_text = text.lower()

    if re.search(r"\b(ph\.?d|doctorate|doctor of philosophy)\b", lower_text):
        return "PhD"
    elif re.search(r"\b(master|master's|m\.?s|m\.?tech|m\.?sc|mba)\b", lower_text):
        return "Master's"
    elif re.search(r"\b(bachelor|bachelor's|b\.?e|b\.?tech|b\.?s|b\.?sc|bba)\b", lower_text):
        return "Bachelor's"

    return "Bachelor's"


def extract_cgpa(text):
    # Extract CGPA or GPA score out of 10 or 4
    patterns = [
        r"(?:cgpa|gpa)\s*[:=]?\s*(\d+\.?\d*)\s*(?:/\s*(?:10|4))?",
        r"(\d\.\d{1,2})\s*(?:/\s*10|/\s*4\.0)?\s*(?:cgpa|gpa)",
    ]

    for pat in patterns:
        match = re.search(pat, text, flags=re.IGNORECASE)
        if match:
            try:
                val = float(match.group(1))
                if 0.0 <= val <= 10.0:
                    return val
            except ValueError:
                pass

    return None


def extract_certifications_count(text):
    # Count identifiable certifications in resume text
    cert_matches = re.findall(
        r"(?:certified|certification|certificate|credential|license)\b",
        text,
        flags=re.IGNORECASE,
    )
    # Estimate count bounded realistically
    return min(len(cert_matches), 10)


def extract_project_count(text):
    # Count identifiable project mentions
    proj_matches = re.findall(
        r"(?:project\s*\d+|project\s*title|academic project|key projects?)\b",
        text,
        flags=re.IGNORECASE,
    )
    if proj_matches:
        return min(len(proj_matches), 10)

    # Secondary check: search for bullet points under a projects section
    if re.search(r"\bprojects?\b", text, flags=re.IGNORECASE):
        return 2

    return 0


def extract_internship_experience(text):
    # Extract number or duration of internships
    intern_matches = re.findall(r"\bintern(?:ship)?\b", text, flags=re.IGNORECASE)
    return min(len(intern_matches), 5)


def extract_previous_job_title(text):
    # Identify previous job title matching known dataset categories
    lower_text = text.lower()
    for title in KNOWN_JOB_TITLES:
        if re.search(r"\b" + re.escape(title.lower()) + r"\b", lower_text):
            return title

    return None


def extract_years_since_graduation(text):
    # Extract graduation year and calculate years since graduation
    current_year = datetime.datetime.now().year
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)

    grad_years = [int(y) for y in years if 1980 <= int(y) <= current_year]
    if grad_years:
        latest_year = max(grad_years)
        diff = current_year - latest_year
        return max(0, diff)

    return 2


def extract_candidate_features(resume_text, filename=""):
    # Extract all candidate attributes from resume text into a structured dictionary
    skills = extract_skills(resume_text)
    candidate_name = extract_candidate_name(resume_text, filename)
    exp_years = extract_experience_years(resume_text)
    education = extract_education_level(resume_text)
    cgpa = extract_cgpa(resume_text)
    cert_count = extract_certifications_count(resume_text)
    proj_count = extract_project_count(resume_text)
    intern_exp = extract_internship_experience(resume_text)
    prev_title = extract_previous_job_title(resume_text)
    years_grad = extract_years_since_graduation(resume_text)

    features = {
        "Name": candidate_name,
        "Filename": filename,
        "Skills": ", ".join(skills) if skills else "",
        "Skills_List": skills,
        "Experience (Years)": exp_years,
        "Education Level": education,
        "CGPA": cgpa,
        "Certifications Count": cert_count,
        "Project Count": proj_count,
        "Internship Experience": intern_exp,
        "Previous Job Title": prev_title,
        "Years Since Graduation": years_grad,
    }

    return features


def map_candidate_features(extracted_data, job_requirements):
    # Map extracted resume data and HR job requirements into exact ML training schema
    job_req = job_requirements or {}

    model_features = {
        "Skills": extracted_data.get("Skills", ""),
        "Experience (Years)": extracted_data.get("Experience (Years)", 0),
        "CGPA": extracted_data.get("CGPA", None),
        "Certifications Count": extracted_data.get("Certifications Count", 0),
        "Project Count": extracted_data.get("Project Count", 0),
        "Internship Experience": extracted_data.get("Internship Experience", 0),
        "Years Since Graduation": extracted_data.get("Years Since Graduation", 2),
        "Education Level": extracted_data.get("Education Level", "Bachelor's"),
        "Previous Job Title": extracted_data.get("Previous Job Title", None),
        "Job Role": job_req.get("job_role", "Software Engineer"),
        "Job Type": job_req.get("job_type", "Full-time"),
    }

    return model_features


def calculate_requirement_checks(extracted_data, job_requirements):
    # Perform separate, transparent rule-based requirement checks
    if not job_requirements:
        return {
            "experience_met": True,
            "education_met": True,
            "matched_skills": [],
            "missing_skills": [],
            "skill_match_pct": 0.0,
            "completeness_score": 100,
        }

    # 1) Experience check
    min_exp = job_requirements.get("min_experience", 0)
    cand_exp = extracted_data.get("Experience (Years)", 0)
    experience_met = cand_exp >= min_exp

    # 2) Education check
    edu_ranking = {"Bachelor's": 1, "Master's": 2, "PhD": 3}
    req_edu = job_requirements.get("education_requirement", "Bachelor's")
    cand_edu = extracted_data.get("Education Level", "Bachelor's")
    education_met = edu_ranking.get(cand_edu, 1) >= edu_ranking.get(req_edu, 1)

    # 3) Skills check
    req_skills_raw = job_requirements.get("required_skills", "")
    req_skills = [s.strip() for s in req_skills_raw.split(",") if s.strip()]

    cand_skills = extracted_data.get("Skills_List", [])
    cand_skills_lower = {s.lower() for s in cand_skills}

    matched_skills = [s for s in req_skills if s.lower() in cand_skills_lower]
    missing_skills = [s for s in req_skills if s.lower() not in cand_skills_lower]

    skill_match_pct = (len(matched_skills) / len(req_skills) * 100) if req_skills else 0.0

    # 4) Completeness score
    checks = [
        bool(extracted_data.get("Skills")),
        extracted_data.get("CGPA") is not None,
        extracted_data.get("Previous Job Title") is not None,
        bool(extracted_data.get("Experience (Years)") is not None),
        bool(extracted_data.get("Education Level")),
    ]
    completeness_score = int((sum(checks) / len(checks)) * 100)

    return {
        "experience_met": experience_met,
        "education_met": education_met,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_pct": round(skill_match_pct, 1),
        "completeness_score": completeness_score,
    }

