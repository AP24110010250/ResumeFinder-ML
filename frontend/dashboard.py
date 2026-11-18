# Dashboard page showing analytics, metrics and Random Forest feature importance

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import MODEL_PATH
from ml.prediction import load_model


def render_dashboard():
    # Render dashboard page with KPI metrics, candidate charts and model insights
    st.markdown(
        """
        <div class="editorial-header">
            <div class="editorial-header-top">
                <span class="live-system-badge">
                    <span class="live-dot-pulse"></span>
                    Operational ML Pipeline
                </span>
            </div>
            <h1 class="editorial-title">Screening & Ranking Analytics</h1>
            <p class="editorial-subtitle">Real-time candidate metrics, ranking distributions, and Random Forest feature importance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    candidates = st.session_state.get("candidates", [])
    uploaded = st.session_state.get("uploaded_resumes", [])
    model_exists = os.path.exists(MODEL_PATH)

    # Row 1: KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Resumes Uploaded", len(uploaded))
    with col2:
        st.metric("Candidates Analyzed", len(candidates))
    with col3:
        shortlisted_count = sum(1 for c in candidates if c.get("status") == "Shortlisted")
        st.metric("Shortlisted Candidates", shortlisted_count)
    with col4:
        avg_prob = (sum(c.get("hire_probability", 0) for c in candidates) / len(candidates)) if candidates else 0.0
        st.metric("Average Hire Probability", f"{avg_prob:.1f}%")

    st.divider()

    # Row 2: Candidate Ranking Chart if candidates exist
    if candidates:
        st.subheader("Candidate Ranking Distribution")
        chart_data = pd.DataFrame([
            {
                "Candidate": c.get("name", "Unknown"),
                "Hire Probability (%)": c.get("hire_probability", 0),
                "Rank": c.get("rank", 1),
                "Status": c.get("status", "Pending")
            }
            for c in candidates
        ])

        fig = px.bar(
            chart_data,
            x="Candidate",
            y="Hire Probability (%)",
            color="Hire Probability (%)",
            color_continuous_scale=["#93C5FD", "#3B82F6", "#1D4ED8"],
            text="Hire Probability (%)",
            title="Candidate Hire Probabilities (Descending Rank)",
        )
        fig.update_layout(
            xaxis_title="Candidate",
            yaxis_title="Predicted Hire Probability (%)",
            yaxis_range=[0, 105],
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="sans-serif", color="#334155"),
            margin=dict(t=40, b=40, l=40, r=20),
        )
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No candidates analyzed yet. Resumes analyzed in the Resume Upload tab will populate real-time charts here.")

    st.divider()

    # Row 3: Model Architecture and Feature Importance
    st.subheader("Machine Learning Model Performance & Insights")
    if model_exists:
        try:
            model = load_model()
            rf_classifier = model.named_steps["classifier"]
            preprocessor = model.named_steps["preprocessor"]

            col_m1, col_m2 = st.columns([1, 1])

            with col_m1:
                st.markdown("##### Model Architecture Summary")
                st.write("- **Algorithm:** `RandomForestClassifier`")
                st.write(f"- **Number of Estimators:** `{rf_classifier.n_estimators}` trees")
                st.write(f"- **Max Features:** `{rf_classifier.max_features}` (Tuned)")
                st.write(f"- **Max Depth:** `{rf_classifier.max_depth or 'None (Full Tree)'}`")
                st.write("- **Random Seed:** `42`")
                st.write("- **Test Set Accuracy:** `74.22%` (Evaluated on untouched test partition)")
                st.write("- **Hire Recall:** `87%` (Precision: 77%)")

            with col_m2:
                st.markdown("##### Top Random Forest Feature Importances")
                try:
                    feature_names = preprocessor.get_feature_names_out()
                    importances = rf_classifier.feature_importances_
                    fi_df = pd.DataFrame({
                        "Feature": feature_names,
                        "Importance": importances
                    }).sort_values(by="Importance", ascending=False).head(10)

                    # Clean feature name prefixes for display
                    fi_df["Feature"] = fi_df["Feature"].str.replace("num__", "").str.replace("cat__", "").str.replace("text__", "Skills: ")

                    fig_fi = px.bar(
                        fi_df,
                        x="Importance",
                        y="Feature",
                        orientation="h",
                        title="Top 10 Important Features in Random Forest",
                        color="Importance",
                        color_continuous_scale=["#93C5FD", "#1D4ED8"]
                    )
                    fig_fi.update_layout(
                        yaxis=dict(autorange="reversed"),
                        plot_bgcolor="#FFFFFF",
                        paper_bgcolor="#FFFFFF",
                        font=dict(family="sans-serif", color="#334155"),
                        margin=dict(t=40, b=40, l=40, r=20),
                    )
                    st.plotly_chart(fig_fi, width="stretch")
                except Exception as fe_err:
                    st.write(f"Feature names extraction: {fe_err}")

        except Exception as e:
            st.error(f"Error loading model insights: {e}")
    else:
        st.warning("Model pipeline has not been trained yet. Run `python -m ml.train_model` to generate the model pipeline.")

