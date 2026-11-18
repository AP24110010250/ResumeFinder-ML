# Results and candidate ranking view for HR recruiters

import streamlit as st


def render_results():
    # Render candidate ranking and detailed results
    st.markdown(
        """
        <div class="editorial-header">
            <div class="editorial-header-top">
                <span class="live-system-badge">
                    <span class="live-dot-pulse"></span>
                    Random Forest Inferred
                </span>
            </div>
            <h1 class="editorial-title">Candidate Screening & Ranking Leaderboard</h1>
            <p class="editorial-subtitle">Candidates ranked strictly by Random Forest Hire probability with transparent eligibility checks.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    candidates = st.session_state.get("candidates", [])
    if not candidates:
        st.info("No analyzed candidates yet. Please upload resumes and click 'Analyze Resumes' in the Resume Upload tab.")
        return

    st.write(
        "Candidates are ranked strictly by the **Random Forest predicted Hire probability**. "
        "Rule-based requirement checks and missing skills are displayed separately to assist your hiring decision."
    )
    st.caption("Note: Predicted probability indicates statistical alignment with historical hires and does not guarantee candidate success.")

    # Top summary metrics
    col1, col2, col3 = st.columns(3)
    avg_hire_prob = sum(c.get("hire_probability", 0) for c in candidates) / len(candidates)
    with col1:
        st.metric("Total Candidates Ranked", len(candidates))
    with col2:
        st.metric("Average Hire Probability", f"{avg_hire_prob:.1f}%")
    with col3:
        top_cand = candidates[0]
        st.metric("Top Candidate", f"{top_cand.get('name', 'N/A')} ({top_cand.get('hire_probability', 0)}%)")

    st.divider()

    # Display each candidate card
    for c in candidates:
        rank = c.get("rank", 1)
        name = c.get("name", "Candidate")
        filename = c.get("filename", "")
        hire_prob = c.get("hire_probability", 0.0)
        skill_pct = c.get("skill_match_pct", 0.0)
        status = c.get("status", "Pending")

        # Visual color for hire probability
        color_badge = "🟢" if hire_prob >= 70 else ("🟡" if hire_prob >= 50 else "🔴")

        with st.expander(f"**Rank #{rank}: {name}** | Hire Probability: **{hire_prob}%** {color_badge} | Status: **{status}**", expanded=(rank <= 2)):
            col_a, col_b = st.columns([1, 1])

            with col_a:
                st.markdown("##### Candidate Profile & ML Prediction")
                st.write(f"- **Resume File:** `{filename}`")
                st.write(f"- **Random Forest Predicted Decision:** `{c.get('predicted_label', 'N/A')}`")
                st.write(f"- **Predicted Hire Probability:** **{hire_prob}%**")
                st.write(f"- **Total Experience:** {c.get('extracted_features', {}).get('Experience (Years)', 0)} years")
                st.write(f"- **Education Level:** {c.get('extracted_features', {}).get('Education Level', 'N/A')}")
                cgpa_val = c.get('extracted_features', {}).get('CGPA')
                st.write(f"- **CGPA:** {cgpa_val if cgpa_val is not None else 'Not Specified'}")
                st.write(f"- **Identified Certifications:** {c.get('extracted_features', {}).get('Certifications Count', 0)}")
                st.write(f"- **Projects:** {c.get('extracted_features', {}).get('Project Count', 0)}")

                # Completeness warning if below threshold
                completeness = c.get("completeness_score", 100)
                if completeness < 70:
                    st.warning(f"Information Completeness: {completeness}%. Some fields were missing and handled via imputation.")
                else:
                    st.caption(f"Information Completeness: {completeness}%")

            with col_b:
                st.markdown("##### HR Requirement Comparison (Rule-Based)")
                exp_status = "Meets Requirement" if c.get("experience_met") else "Does Not Meet Requirement"
                edu_status = "Meets Requirement" if c.get("education_met") else "Does Not Meet Requirement"

                st.write(f"- **Experience Check:** `{exp_status}`")
                st.write(f"- **Education Check:** `{edu_status}`")
                st.write(f"- **Skill Match Percentage:** **{skill_pct}%**")

                matched = c.get("matched_skills", [])
                missing = c.get("missing_skills", [])

                if matched:
                    st.write(f"- **Matched Skills ({len(matched)}):** {', '.join(matched)}")
                else:
                    st.write("- **Matched Skills:** None")

                if missing:
                    st.error(f"Missing Required Skills ({len(missing)}): {', '.join(missing)}")
                else:
                    st.success("All required skills matched!")

                cand_all_skills = c.get("extracted_features", {}).get("Skills_List", [])
                if cand_all_skills:
                    st.caption(f"All Extracted Resume Skills: {', '.join(cand_all_skills)}")

