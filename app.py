import streamlit as st

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d2e 0%, #12151f 100%);
        border-right: 1px solid #2d3748;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e2235 0%, #252a3d 100%);
        border: 1px solid #3d4a6b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-2px); }
    .kpi-title { color: #8892b0; font-size: 13px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px; }
    .kpi-value { color: #e2e8f0; font-size: 32px; font-weight: 700; line-height: 1; }
    .kpi-delta { font-size: 13px; margin-top: 6px; }
    .delta-pos { color: #68d391; }
    .delta-neg { color: #fc8181; }

    /* Segment badges */
    .badge-hv  { background:#1a4731; color:#68d391; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-lm  { background:#1a3a6e; color:#63b3ed; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-bs  { background:#3d2c1a; color:#f6ad55; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600; }
    .badge-ar  { background:#3d1a1a; color:#fc8181; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600; }

    /* Section headers */
    .section-header {
        color: #a0aec0;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 20px 0 8px 0;
        padding-left: 4px;
        border-left: 3px solid #4c6ef5;
    }

    /* Prediction result box */
    .pred-box {
        background: linear-gradient(135deg, #1e2235, #252a3d);
        border: 2px solid #4c6ef5;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }
    .pred-segment { font-size: 28px; font-weight: 800; color: #7f9cf5; }
    .pred-label   { color: #8892b0; font-size: 14px; margin-bottom: 8px; }

    /* Streamlit overrides */
    h1, h2, h3 { color: #e2e8f0 !important; }
    .stMarkdown p { color: #a0aec0; }
    [data-testid="stMetricValue"] { color: #e2e8f0; }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stNumberInput"] label { color: #a0aec0 !important; }
    .stButton > button {
        background: linear-gradient(135deg, #4c6ef5, #7048e8);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
    }
    .stButton > button:hover { opacity: 0.9; }
    .stDownloadButton > button {
        background: #1a4731;
        color: #68d391;
        border: 1px solid #68d391;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size:36px;'>🎯</div>
        <div style='color:#e2e8f0; font-size:16px; font-weight:700; margin-top:6px;'>SegmentIQ</div>
        <div style='color:#4c6ef5; font-size:11px; letter-spacing:2px;'>ML DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Navigate</div>", unsafe_allow_html=True)

    pages = {
        "📊  Overview":          "Overview",
        "👥  Customer Explorer": "Customer Explorer",
        "🤖  Predict Segment":   "Predict Segment",
        "📈  Segment Analysis":  "Segment Analysis",
        "💡  Recommendations":   "Recommendations",
        "📋  QA Report":         "QA Report",
        "📄  Documentation":     "Documentation",
    }

    if "page" not in st.session_state:
        st.session_state.page = "Overview"

    for label, key in pages.items():
        active = st.session_state.page == key
        if st.button(label, use_container_width=True, key=f"nav_{key}",
                     type="primary" if active else "secondary"):
            st.session_state.page = key

    st.markdown("---")
    st.markdown("<div style='color:#4a5568; font-size:11px; text-align:center;'>ML Internship · Day 1–5<br/>Streamlit + KMeans</div>", unsafe_allow_html=True)

# ── Page Router ─────────────────────────────────────────────────
page = st.session_state.page

if page == "Overview":
    from pages.overview import show; show()
elif page == "Customer Explorer":
    from pages.explorer import show; show()
elif page == "Predict Segment":
    from pages.predict import show; show()
elif page == "Segment Analysis":
    from pages.analysis import show; show()
elif page == "Recommendations":
    from pages.recommendations import show; show()
elif page == "QA Report":
    from pages.qa import show; show()
elif page == "Documentation":
    from pages.documentation import show; show()
