# Candidate comparison page for HR recruiters

import streamlit as st
import pandas as pd


def render_candidate_comparison():
    # Allow HR to select 2 or 3 candidates and compare their profiles side-by-side
    st.markdown(
        """
        <div class="editorial-header">
            <div class="editorial-header-top">
                <span class="live-system-badge">
                    <span class="live-dot-pulse"></span>
                    Side-by-Side Matrix
                </span>
            </div>
            <h1 class="editorial-title">Candidate Comparative Evaluation</h1>
            <p class="editorial-subtitle">Direct evaluation of skills, experience, and predicted probabilities for selected candidates.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    candidates = st.session_state.get("candidates", [])
    if len(candidates) < 2:
        st.info("At least 2 analyzed candidates are required for comparison. Please analyze resumes first.")
        return

    candidate_options = [f"{c.get('name', 'Candidate')} (Rank #{c.get('rank', 1)})" for c in candidates]
    cand_lookup = {opt: candidates[idx] for idx, opt in enumerate(candidate_options)}

    selected_options = st.multiselect(
        "Choose 2 or 3 Candidates to Compare",
        options=candidate_options,
        default=candidate_options[: min(2, len(candidate_options))],
        max_selections=3,
    )

    if len(selected_options) < 2:
        st.warning("Please select at least 2 candidates to view comparison.")
        return

    selected_cands = [cand_lookup[opt] for opt in selected_options]

    # Build comparison summary table
    comparison_rows = [
        {"Attribute": "Candidate Name", **{c["name"]: c["name"] for c in selected_cands}},
        {"Attribute": "Ranking", **{c["name"]: f"#{c.get('rank')}" for c in selected_cands}},
        {"Attribute": "Predicted Hire Probability", **{c["name"]: f"{c.get('hire_probability')}%" for c in selected_cands}},
        {"Attribute": "Random Forest Decision", **{c["name"]: c.get("predicted_label") for c in selected_cands}},
        {"Attribute": "Total Experience (Years)", **{c["name"]: f"{c.get('extracted_features', {}).get('Experience (Years)', 0)} yrs" for c in selected_cands}},
        {"Attribute": "Education Level", **{c["name"]: c.get("extracted_features", {}).get("Education Level", "N/A") for c in selected_cands}},
        {"Attribute": "CGPA", **{c["name"]: str(c.get("extracted_features", {}).get("CGPA", "Not specified")) for c in selected_cands}},
        {"Attribute": "Identified Projects", **{c["name"]: c.get("extracted_features", {}).get("Project Count", 0) for c in selected_cands}},
        {"Attribute": "Certifications Count", **{c["name"]: c.get("extracted_features", {}).get("Certifications Count", 0) for c in selected_cands}},
        {"Attribute": "Skill Match Percentage", **{c["name"]: f"{c.get('skill_match_pct')}%" for c in selected_cands}},
        {"Attribute": "Experience Requirement Met?", **{c["name"]: "Yes" if c.get("experience_met") else "No" for c in selected_cands}},
        {"Attribute": "Education Requirement Met?", **{c["name"]: "Yes" if c.get("education_met") else "No" for c in selected_cands}},
        {"Attribute": "Matched Skills", **{c["name"]: ", ".join(c.get("matched_skills", [])) or "None" for c in selected_cands}},
        {"Attribute": "Missing Skills", **{c["name"]: ", ".join(c.get("missing_skills", [])) or "None" for c in selected_cands}},
        {"Attribute": "Current HR Status", **{c["name"]: c.get("status", "Pending") for c in selected_cands}},
    ]

    df_comp = pd.DataFrame(comparison_rows).astype(str)
    st.dataframe(df_comp, hide_index=True)

