# Configuration settings and constant values for the project

import os

# Base project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
DATASET_PATH = os.path.join(DATA_DIR, "Rupa_dataset.csv")

# Model paths
ML_DIR = os.path.join(BASE_DIR, "ml")
MODEL_PATH = os.path.join(ML_DIR, "model_pipeline.joblib")

# Database path
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "candidates.db")

# Target column name
TARGET_COLUMN = "Final Decision"

# Columns excluded from model training
EXCLUDED_COLUMNS = [
    "Resume_ID",
    "Name",
    "Primary Skill",
    "Skill Match Score",
    "Role Match Score",
    "LinkedIn Score",
    "Final Decision",
]

# Model feature definitions
TEXT_FEATURES = ["Skills"]

NUMERICAL_FEATURES = [
    "Experience (Years)",
    "CGPA",
    "Certifications Count",
    "Project Count",
    "Internship Experience",
    "Years Since Graduation",
]

CATEGORICAL_FEATURES = [
    "Education Level",
    "Previous Job Title",
    "Job Role",
    "Job Type",
]

# All input features expected by the model
FEATURE_COLUMNS = TEXT_FEATURES + NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# Fixed categories matching the dataset exactly
JOB_ROLES = [
    "Product Manager",
    "HR Generalist",
    "Data Scientist",
    "Software Engineer",
    "Marketing Analyst",
]

JOB_TYPES = [
    "Internship",
    "Full-time",
    "Contract",
    "Part-time",
]

EDUCATION_LEVELS = [
    "Bachelor's",
    "Master's",
    "PhD",
]

