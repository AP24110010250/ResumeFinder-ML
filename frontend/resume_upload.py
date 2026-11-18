# Resume upload page for HR recruiters

import streamlit as st
from backend.resume_parser import extract_resume_text, validate_pdf


def render_resume_upload():
    # Render the resume upload interface
    st.markdown(
        """
        <div class="editorial-header">
            <div class="editorial-header-top">
                <span class="live-system-badge">
                    <span class="live-dot-pulse"></span>
                    PyMuPDF Extractor
                </span>
            </div>
            <h1 class="editorial-title">Candidate Resume Ingestion</h1>
            <p class="editorial-subtitle">Upload digital PDF resumes for automated feature extraction, NLP parsing, and ML inference.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Select PDF Resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload digital PDF files containing selectable text.",
    )

    if uploaded_files:
        st.subheader(f"Uploaded Files ({len(uploaded_files)})")

        valid_files = []
        invalid_files = []

        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.getvalue()
            is_valid, msg = validate_pdf(file_bytes)
            if is_valid:
                valid_files.append(uploaded_file)
            else:
                invalid_files.append((uploaded_file.name, msg))

        # Show valid and invalid files
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"{len(valid_files)} Valid PDF files ready for analysis.")
            for vf in valid_files:
                st.write(f"- {vf.name} ({len(vf.getvalue()) / 1024:.1f} KB)")
        with col2:
            if invalid_files:
                st.error(f"{len(invalid_files)} Invalid or unreadable files:")
                for name, err in invalid_files:
                    st.write(f"- {name}: {err}")

        # Store in session state
        st.session_state["uploaded_resumes"] = valid_files

        # Inform user to set job requirements if missing
        if not st.session_state.get("job_requirements"):
            st.warning("Please configure Job Requirements in the Job Requirements tab before analyzing resumes.")
        else:
            if st.button("Analyze Resumes", type="primary"):
                with st.spinner("Extracting resume features and predicting candidate hire probabilities..."):
                    from backend.resume_parser import extract_resume_text
                    from backend.candidate_features import (
                        extract_candidate_features,
                        map_candidate_features,
                        calculate_requirement_checks,
                    )
                    from ml.prediction import load_model, predict_candidate
                    from ml.ranking import rank_candidates

                    try:
                        model = load_model()
                    except Exception as err:
                        st.error(f"Cannot load ML model: {err}")
                        return

                    job_req = st.session_state["job_requirements"]
                    processed_candidates = []

                    for uf in valid_files:
                        resume_text, msg = extract_resume_text(uf)
                        if not resume_text:
                            st.warning(f"Could not extract text from {uf.name}: {msg}")
                            continue

                        # Extract features from text
                        extracted = extract_candidate_features(resume_text, uf.name)
                        # Map features to ML training schema
                        model_feats = map_candidate_features(extracted, job_req)
                        # Predict with Random Forest
                        pred_res = predict_candidate(model_feats, model)
                        # Evaluate transparent rule checks
                        rule_checks = calculate_requirement_checks(extracted, job_req)

                        cand_record = {
                            "name": extracted.get("Name", "Candidate"),
                            "filename": uf.name,
                            "extracted_features": extracted,
                            "model_features": model_feats,
                            "predicted_label": pred_res["predicted_label"],
                            "hire_probability": pred_res["hire_probability"],
                            "experience_met": rule_checks["experience_met"],
                            "education_met": rule_checks["education_met"],
                            "matched_skills": rule_checks["matched_skills"],
                            "missing_skills": rule_checks["missing_skills"],
                            "skill_match_pct": rule_checks["skill_match_pct"],
                            "completeness_score": rule_checks["completeness_score"],
                            "status": "Pending",
                        }
                        processed_candidates.append(cand_record)

                    # Rank candidates strictly by Random Forest Hire probability
                    ranked_candidates = rank_candidates(processed_candidates)
                    st.session_state["candidates"] = ranked_candidates
                    st.success(f"Successfully analyzed and ranked {len(ranked_candidates)} candidates! Navigate to 'Candidate Results' to view rankings.")
