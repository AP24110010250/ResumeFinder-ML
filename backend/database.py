# SQLite database operations for candidates and job requirements

import sqlite3
import os
import json
from utils.config import DATABASE_PATH


def connect_db():
    # Connect to the SQLite database
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    # Create jobs and candidates tables if they do not exist
    conn = connect_db()
    cursor = conn.cursor()

    # 1) Jobs table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            job_role TEXT NOT NULL,
            job_type TEXT NOT NULL,
            education_requirement TEXT NOT NULL,
            min_experience INTEGER NOT NULL,
            required_skills TEXT NOT NULL,
            job_description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # 2) Candidates table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            name TEXT NOT NULL,
            filename TEXT NOT NULL,
            hire_probability REAL NOT NULL,
            predicted_label TEXT NOT NULL,
            ranking INTEGER,
            status TEXT DEFAULT 'Pending',
            skills TEXT,
            experience_years INTEGER,
            education_level TEXT,
            cgpa REAL,
            certifications_count INTEGER,
            project_count INTEGER,
            matched_skills TEXT,
            missing_skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        )
        """
    )

    conn.commit()
    conn.close()


def save_job_details(job_data):
    # Save active job requirements and return inserted job_id
    create_tables()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (
            job_title, job_role, job_type, education_requirement,
            min_experience, required_skills, job_description
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_data.get("job_title", ""),
            job_data.get("job_role", ""),
            job_data.get("job_type", ""),
            job_data.get("education_requirement", ""),
            int(job_data.get("min_experience", 0)),
            job_data.get("required_skills", ""),
            job_data.get("job_description", ""),
        ),
    )

    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return job_id


def save_candidate(candidate_record, job_id=None):
    # Save a candidate screening record
    create_tables()
    conn = connect_db()
    cursor = conn.cursor()

    ext = candidate_record.get("extracted_features", {})

    cursor.execute(
        """
        INSERT INTO candidates (
            job_id, name, filename, hire_probability, predicted_label,
            ranking, status, skills, experience_years, education_level,
            cgpa, certifications_count, project_count, matched_skills, missing_skills
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job_id,
            candidate_record.get("name", "Candidate"),
            candidate_record.get("filename", ""),
            float(candidate_record.get("hire_probability", 0.0)),
            candidate_record.get("predicted_label", ""),
            int(candidate_record.get("rank", 0)),
            candidate_record.get("status", "Pending"),
            ext.get("Skills", ""),
            int(ext.get("Experience (Years)", 0)),
            ext.get("Education Level", ""),
            ext.get("CGPA"),
            int(ext.get("Certifications Count", 0)),
            int(ext.get("Project Count", 0)),
            ", ".join(candidate_record.get("matched_skills", [])),
            ", ".join(candidate_record.get("missing_skills", [])),
        ),
    )

    cand_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return cand_id


def fetch_candidates(job_id=None):
    # Fetch all stored candidates from database
    create_tables()
    conn = connect_db()
    cursor = conn.cursor()

    if job_id:
        cursor.execute("SELECT * FROM candidates WHERE job_id = ? ORDER BY ranking ASC", (job_id,))
    else:
        cursor.execute("SELECT * FROM candidates ORDER BY ranking ASC")

    rows = cursor.fetchall()
    candidates = [dict(row) for row in rows]
    conn.close()
    return candidates


def update_candidate_status(candidate_id, new_status):
    # Update candidate shortlisting status (Pending, Shortlisted, Not Shortlisted)
    create_tables()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE candidates SET status = ? WHERE id = ?",
        (new_status, candidate_id),
    )
    conn.commit()
    conn.close()

