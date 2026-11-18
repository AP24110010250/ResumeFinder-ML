# Skill extraction and matching module

import re

# Canonical skill dictionary including all 60 dataset skills and standard industry skills
SKILL_DICTIONARY = {
    "a/b testing": "A/B Testing",
    "aws": "AWS",
    "amazon web services": "AWS",
    "agile": "Agile",
    "algorithms": "Algorithms",
    "big data": "Big Data",
    "c++": "C++",
    "cpp": "C++",
    "ci/cd": "CI/CD",
    "continuous integration": "CI/CD",
    "css": "CSS",
    "communication": "Communication",
    "conflict resolution": "Conflict Resolution",
    "content strategy": "Content Strategy",
    "copywriting": "Copywriting",
    "data analytics": "Data Analytics",
    "data structures": "Data Structures",
    "data visualization": "Data Visualization",
    "deep learning": "Deep Learning",
    "docker": "Docker",
    "email marketing": "Email Marketing",
    "employee relations": "Employee Relations",
    "excel": "Excel",
    "git": "Git",
    "github": "Git",
    "google analytics": "Google Analytics",
    "hr analytics": "HR Analytics",
    "hris": "HRIS",
    "html": "HTML",
    "java": "Java",
    "jira": "Jira",
    "kubernetes": "Kubernetes",
    "labor laws": "Labor Laws",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "market research": "Market Research",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "numpy": "NumPy",
    "onboarding": "Onboarding",
    "pandas": "Pandas",
    "performance management": "Performance Management",
    "product lifecycle": "Product Lifecycle",
    "product strategy": "Product Strategy",
    "python": "Python",
    "r": "R",
    "react": "React",
    "reactjs": "React",
    "recruiting": "Recruiting",
    "roadmapping": "Roadmapping",
    "sem": "SEM",
    "seo": "SEO",
    "sql": "SQL",
    "scikit-learn": "Scikit-Learn",
    "scikit learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "scrum": "Scrum",
    "social media marketing": "Social Media Marketing",
    "sourcing": "Sourcing",
    "spark": "Spark",
    "apache spark": "Spark",
    "stakeholder management": "Stakeholder Management",
    "statistics": "Statistics",
    "system design": "System Design",
    "tableau": "Tableau",
    "talent management": "Talent Management",
    "tensorflow": "TensorFlow",
    "typescript": "TypeScript",
    "ui/ux design": "UI/UX Design",
    "ui/ux": "UI/UX Design",
}


def normalize_skills(skills_list):
    # Normalize list of skills to canonical casing and names
    normalized = []
    for skill in skills_list:
        clean_skill = skill.strip().lower()
        if clean_skill in SKILL_DICTIONARY:
            canonical = SKILL_DICTIONARY[clean_skill]
            if canonical not in normalized:
                normalized.append(canonical)
        elif skill.strip():
            # Keep original title-cased if not in dictionary
            title_skill = skill.strip().title()
            if title_skill not in normalized:
                normalized.append(title_skill)
    return normalized


def extract_skills(text):
    # Extract recognized skills from resume text using word boundaries and pattern matching
    if not text:
        return []

    found_skills = set()
    lower_text = " " + text.lower() + " "

    # Sort dictionary keys by length descending to match multi-word phrases first
    sorted_skills = sorted(SKILL_DICTIONARY.keys(), key=lambda s: len(s), reverse=True)

    for skill_key in sorted_skills:
        # Build regex with boundary checking
        # Handle special characters in keys like c++, ci/cd, node.js
        escaped_key = re.escape(skill_key)

        # Use non-alphanumeric boundaries
        pattern = r"(?<![a-zA-Z0-9])" + escaped_key + r"(?![a-zA-Z0-9])"

        if re.search(pattern, lower_text):
            canonical_name = SKILL_DICTIONARY[skill_key]
            found_skills.add(canonical_name)

    return sorted(list(found_skills))


def match_skills(candidate_skills, required_skills):
    # Calculate matched skills between candidate and required skills
    if not candidate_skills or not required_skills:
        return []

    candidate_set = {s.lower() for s in candidate_skills}
    matched = []

    for req in required_skills:
        if req.lower() in candidate_set:
            matched.append(req)

    return matched


def find_missing_skills(candidate_skills, required_skills):
    # Identify required skills that the candidate lacks
    if not required_skills:
        return []

    if not candidate_skills:
        return list(required_skills)

    candidate_set = {s.lower() for s in candidate_skills}
    missing = []

    for req in required_skills:
        if req.lower() not in candidate_set:
            missing.append(req)

    return missing

