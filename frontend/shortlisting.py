# Candidate shortlisting and Excel export page for HR recruiters

import io
import streamlit as st
import pandas as pd
from backend.database import save_job_details, save_candidate, update_candidate_status


def render_shortlisting():
    # Render shortlisting interface, status modification and Excel export
    st.markdown(
        """
        <div class="editorial-header">
            <div class="editorial-header-top">
                <span class="live-system-badge">
                    <span class="live-dot-pulse"></span>
                    Decision Governance
                </span>
            </div>
            <h1 class="editorial-title">Candidate Shortlisting & Export</h1>
            <p class="editorial-subtitle">Record recruiter hiring decisions, persist records to SQLite database, and download Excel reports.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    candidates = st.session_state.get("candidates", [])
    if not candidates:
        st.info("No candidates available. Please upload resumes and analyze them first.")
        return

    # Status modification table
    st.subheader("Candidate Decision Management")

    status_options = ["Pending", "Shortlisted", "Not Shortlisted"]

    for idx, c in enumerate(candidates):
        c_name = c.get("name", f"Candidate {idx+1}")
        c_prob = c.get("hire_probability", 0)
        c_status = c.get("status", "Pending")

        col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
        with col1:
            st.write(f"**#{c.get('rank', idx+1)}**")
        with col2:
            st.write(f"**{c_name}** ({c.get('filename', '')})")
        with col3:
            st.write(f"Hire Prob: **{c_prob}%** | Decision: `{c.get('predicted_label')}`")
        with col4:
            new_status = st.selectbox(
                f"Status for {c_name}",
                options=status_options,
                index=status_options.index(c_status) if c_status in status_options else 0,
                key=f"status_select_{idx}",
                label_visibility="collapsed",
            )
            if new_status != c_status:
                c["status"] = new_status
                st.session_state["candidates"][idx]["status"] = new_status
                # If candidate has a database ID, update in SQLite
                if "db_id" in c:
                    update_candidate_status(c["db_id"], new_status)

    st.divider()

    # Save to SQLite Database
    col_db, col_exp = st.columns(2)
    with col_db:
        if st.button("Save All to SQLite Database", type="secondary"):
            job_req = st.session_state.get("job_requirements", {})
            job_id = save_job_details(job_req)
            for c in candidates:
                cand_db_id = save_candidate(c, job_id=job_id)
                c["db_id"] = cand_db_id
            st.success(f"Saved {len(candidates)} candidates and job details to SQLite database!")

    # Export to Excel using openpyxl
    with col_exp:
        # Prepare export dataframe
        export_records = []
        for c in candidates:
            ext = c.get("extracted_features", {})
            export_records.append({
                "Rank": c.get("rank"),
                "Candidate Name": c.get("name"),
                "Filename": c.get("filename"),
                "Shortlist Status": c.get("status"),
                "Predicted Hire Probability (%)": c.get("hire_probability"),
                "Random Forest Prediction": c.get("predicted_label"),
                "Experience (Years)": ext.get("Experience (Years)", 0),
                "Education Level": ext.get("Education Level", ""),
                "CGPA": ext.get("CGPA"),
                "Skill Match (%)": c.get("skill_match_pct"),
                "Matched Skills": ", ".join(c.get("matched_skills", [])),
                "Missing Skills": ", ".join(c.get("missing_skills", [])),
                "Experience Met": "Yes" if c.get("experience_met") else "No",
                "Education Met": "Yes" if c.get("education_met") else "No",
            })

        df_export = pd.DataFrame(export_records)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Candidate_Rankings")

        st.download_button(
            label="Export to Excel (.xlsx)",
            data=buffer.getvalue(),
            file_name="candidate_screening_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )

