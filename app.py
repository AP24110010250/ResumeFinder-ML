import sys
import os

# Add project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from utils.config import MODEL_PATH
from frontend.dashboard import render_dashboard
from frontend.job_form import render_job_form
from frontend.resume_upload import render_resume_upload
from frontend.results import render_results
from frontend.comparison import render_candidate_comparison
from frontend.shortlisting import render_shortlisting

# Configure Streamlit page
st.set_page_config(
    page_title="Resume Screening & Candidate Ranking System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom clean editorial styling inspired by professional design standards
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@700;800&family=Bebas+Neue&display=swap');

    /* Collapse & Hide sidebar entirely */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Global typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
    }

    /* Subtle fine noise grain */
    .grain-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 99999;
        opacity: 0.015;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    /* Editorial Executive Header */
    .editorial-header {
        background-color: #FFFFFF;
        border: 1px solid rgba(15, 23, 42, 0.09);
        border-radius: 10px;
        padding: 22px 28px;
        margin-bottom: 24px;
        position: relative;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .editorial-header-top {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
    }
    .live-system-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #2563EB;
        background: rgba(37, 99, 235, 0.07);
        padding: 3px 10px;
        border-radius: 999px;
        border: 1px solid rgba(37, 99, 235, 0.2);
    }
    .live-dot-pulse {
        width: 7px;
        height: 7px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
    }
    .editorial-title {
        font-family: 'Syne', sans-serif;
        color: #0F172A;
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .editorial-subtitle {
        color: #475569;
        font-size: 0.95rem;
        margin: 6px 0 0 0;
        font-weight: 400;
    }

    /* Professional Metric Cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(15, 23, 42, 0.08) !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06) !important;
        border-color: rgba(37, 99, 235, 0.3) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Syne', sans-serif !important;
        color: #2563EB !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }

    /* Sidebar Refinements */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid rgba(15, 23, 42, 0.08) !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: -0.01em !important;
    }

    /* Inputs, Selectboxes, and Text Areas */
    input, textarea, [data-baseweb="select"] {
        border-radius: 6px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    input:focus, textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
    }

    /* Primary and Secondary Buttons */
    button[kind="primary"] {
        background-color: #2563EB !important;
        border-color: #2563EB !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.5rem 1.25rem !important;
        transition: background-color 0.2s ease, transform 0.15s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        transform: translateY(-1px) !important;
    }
    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(15, 23, 42, 0.15) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        transition: border-color 0.2s ease, background-color 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        background-color: #F8FAFC !important;
        border-color: #2563EB !important;
        color: #2563EB !important;
    }

    /* Top Navbar Segmented Controller */
    .top-nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        border: 1px solid rgba(15, 23, 42, 0.09);
        border-radius: 12px;
        padding: 8px 18px;
        margin-bottom: 22px;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
    }
    .brand-badge {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-logo-icon {
        width: 32px;
        height: 32px;
        background: #2563EB;
        color: #FFFFFF;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1rem;
    }
    .brand-title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.05rem;
        color: #0F172A;
        letter-spacing: -0.01em;
        line-height: 1.1;
    }
    .brand-sub {
        font-size: 0.72rem;
        color: #64748B;
        font-weight: 500;
        letter-spacing: 0.02em;
    }

    /* Style Streamlit radio horizontally as modern segmented pill tabs */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        gap: 6px;
        background-color: #F1F5F9;
        padding: 5px;
        border-radius: 10px;
        border: 1px solid rgba(15, 23, 42, 0.06);
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background-color: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.8) !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label span[data-testid="stMarkdownContainer"] p {
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #334155 !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) span[data-testid="stMarkdownContainer"] p {
        color: #2563EB !important;
        font-weight: 700 !important;
    }
    /* Hide the default radio circle */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    /* System Status Pill */
    .system-status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 12px;
        border-radius: 8px;
        background: #F8FAFC;
        border: 1px solid rgba(15, 23, 42, 0.08);
        font-size: 0.78rem;
        font-weight: 600;
        color: #334155;
    }
    </style>
    <div class="grain-overlay" aria-hidden="true"></div>
    """,
    unsafe_allow_html=True,
)

# Initialize session state keys
if "job_requirements" not in st.session_state:
    st.session_state["job_requirements"] = None

if "uploaded_resumes" not in st.session_state:
    st.session_state["uploaded_resumes"] = []

if "candidates" not in st.session_state:
    st.session_state["candidates"] = []

# Check model availability status
model_exists = os.path.exists(MODEL_PATH)
status_dot_color = "#10B981" if model_exists else "#F59E0B"
status_text = "Random Forest Ready" if model_exists else "Model Missing"

# Innovative Header & Navigation Bar
nav_col_brand, nav_col_menu, nav_col_status = st.columns([2.2, 5.2, 2.0])

with nav_col_brand:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; padding: 4px 0;">
            <div style="width: 36px; height: 36px; background: #2563EB; color: #FFFFFF; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.1rem; box-shadow: 0 2px 8px rgba(37,99,235,0.3);">
                RS
            </div>
            <div>
                <div style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.05rem; color: #0F172A; line-height: 1.1;">RESUME SCREENER</div>
                <div style="font-size: 0.72rem; color: #64748B; font-weight: 500;">ML CANDIDATE RANKING SYSTEM</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col_menu:
    # Modern Horizontal Segmented Pill Navigation
    nav_options = [
        "📊 Dashboard",
        "⚙️ Requirements",
        "📂 Upload",
        "🏆 Results",
        "⚖️ Compare",
        "🎯 Shortlist",
    ]
    selected_nav = st.radio(
        "Navigation",
        options=nav_options,
        horizontal=True,
        label_visibility="collapsed",
    )

with nav_col_status:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; padding: 6px 0;">
            <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; border-radius: 999px; background: #FFFFFF; border: 1px solid rgba(15,23,42,0.08); font-size: 0.75rem; font-weight: 600; color: #334155; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <span style="width: 8px; height: 8px; border-radius: 50%; background-color: {status_dot_color}; box-shadow: 0 0 8px {status_dot_color};"></span>
                <span>{status_text}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Map selected tab to page view
if "Dashboard" in selected_nav:
    render_dashboard()
elif "Requirements" in selected_nav:
    render_job_form()
elif "Upload" in selected_nav:
    render_resume_upload()
elif "Results" in selected_nav:
    render_results()
elif "Compare" in selected_nav:
    render_candidate_comparison()
elif "Shortlist" in selected_nav:
    render_shortlisting()
