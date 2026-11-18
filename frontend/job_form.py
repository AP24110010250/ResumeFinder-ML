# Job requirements form for HR recruiters

import streamlit as st
from utils.config import JOB_ROLES, JOB_TYPES, EDUCATION_LEVELS


def validate_job_requirements(job_data):
    # Validate job requirements entered by HR
    errors = []

    if not job_data.get("job_title", "").strip():
        errors.append("Job Title is required.")

    if not job_data.get("job_role", "").strip():
        errors.append("Job Role Category is required.")

    if not job_data.get("job_description", "").strip():
        errors.append("Job Description is required.")

    if not job_data.get("required_skills", "").strip():
        errors.append("Required Technical Skills are required.")

    min_exp = job_data.get("min_experience")
    if min_exp is None or min_exp < 0:
        errors.append("Minimum Experience must be 0 or greater.")

    if not job_data.get("education_requirement", "").strip():
        errors.append("Education Requirement is required.")

    if not job_data.get("job_type", "").strip():
        errors.append("Job Type is required.")

    return errors


def render_job_form():
    # Render the HR job requirements form
    st.markdown(
        """
        <div class="editorial-header">
            <div class="editorial-header-top">
                <span class="live-system-badge">
                    <span class="live-dot-pulse"></span>
                    Job Configuration
                </span>
            </div>
            <h1 class="editorial-title">HR Job Requirements Specification</h1>
            <p class="editorial-subtitle">Define target role attributes, essential skills, and candidate eligibility criteria.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Retrieve existing requirements from session state if available
    saved_data = st.session_state.get("job_requirements") or {}

    with st.form("job_requirements_form"):
        # Job Title
        job_title = st.text_input(
            "Job Title *",
            value=saved_data.get("job_title", ""),
            placeholder="e.g. Senior Python Developer / Data Scientist",
        )

        # Job Role Category from dataset categories
        current_role = saved_data.get("job_role", JOB_ROLES[0])
        role_index = JOB_ROLES.index(current_role) if current_role in JOB_ROLES else 0
        job_role = st.selectbox(
            "Job Role Category * (From Dataset Categories)",
            options=JOB_ROLES,
            index=role_index,
            help="Category matching the dataset classes for candidate alignment.",
        )

        # Job Type from dataset categories
        current_type = saved_data.get("job_type", JOB_TYPES[1])
        type_index = JOB_TYPES.index(current_type) if current_type in JOB_TYPES else 0
        job_type = st.selectbox(
            "Job Type *",
            options=JOB_TYPES,
            index=type_index,
        )

        # Education Requirement from dataset categories
        current_edu = saved_data.get("education_requirement", EDUCATION_LEVELS[0])
        edu_index = EDUCATION_LEVELS.index(current_edu) if current_edu in EDUCATION_LEVELS else 0
        education_requirement = st.selectbox(
            "Minimum Education Requirement *",
            options=EDUCATION_LEVELS,
            index=edu_index,
        )

        # Minimum Experience
        min_experience = st.number_input(
            "Minimum Experience (Years) *",
            min_value=0,
            max_value=40,
            value=int(saved_data.get("min_experience", 2)),
            step=1,
        )

        # Required Technical Skills
        required_skills = st.text_area(
            "Required Technical Skills (Comma-separated) *",
            value=saved_data.get("required_skills", "Python, Machine Learning, SQL, Scikit-learn"),
            placeholder="e.g. Python, Machine Learning, Pandas, SQL",
            help="Enter specific skills needed for this role, separated by commas.",
        )

        # Job Description
        job_description = st.text_area(
            "Job Description *",
            value=saved_data.get("job_description", ""),
            placeholder="Enter the full job description and responsibilities...",
            height=120,
        )

        # Submit button
        submit_button = st.form_submit_button("Save Job Requirements")

    if submit_button:
        # 1) Collect form inputs
        candidate_job_data = {
            "job_title": job_title,
            "job_role": job_role,
            "job_type": job_type,
            "education_requirement": education_requirement,
            "min_experience": min_experience,
            "required_skills": required_skills,
            "job_description": job_description,
        }

        # 2) Validate form inputs
        validation_errors = validate_job_requirements(candidate_job_data)

        if validation_errors:
            for error in validation_errors:
                st.error(error)
        else:
            st.session_state["job_requirements"] = candidate_job_data
            st.success("Job requirements successfully saved and validated!")

    # Display current saved requirements if available
    if st.session_state.get("job_requirements"):
        st.subheader("Current Active Job Requirements")
        current_req = st.session_state["job_requirements"]
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Job Title:** {current_req.get('job_title')}")
            st.write(f"**Job Role Category:** {current_req.get('job_role')}")
            st.write(f"**Job Type:** {current_req.get('job_type')}")
        with col2:
            st.write(f"**Min Education:** {current_req.get('education_requirement')}")
            st.write(f"**Min Experience:** {current_req.get('min_experience')} years")
            st.write(f"**Required Skills:** {current_req.get('required_skills')}")

