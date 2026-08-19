import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.loader import load_data, load_model

def show():
    df = load_data()
    pipeline, segment_map, features = load_model()

    st.markdown("## 📄 Project Documentation & Report")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Complete technical documentation for the ML Customer Segmentation Dashboard — Day 5 deliverable.</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📁 Project Overview", "🔬 Methodology", "🏗️ Architecture", "📑 Day-by-Day Log"])

    with tab1:
        st.markdown("""
### Project Summary

**Project Title:** Customer Segmentation ML Dashboard  
**Internship Track:** Machine Learning  
**Technology Stack:** Python · Streamlit · Scikit-learn · Plotly · Pandas  
**Dashboard URL:** localhost:8501 (local) · Deployable on Streamlit Cloud  

### Objective
Build a production-ready interactive dashboard that:
- Loads a trained KMeans customer segmentation model
- Visualises all 4 customer segments with interactive charts
- Allows real-time segment prediction for new customers
- Delivers actionable marketing recommendations per segment
- Passes automated quality assurance checks

### Dataset
- **Source:** Synthetically generated (representative of e-commerce CRM data)
- **Records:** 500 customers
- **Raw Features:** Age, Annual Income, Spending Score, Purchase Frequency, Avg Order Value, Tenure, Returns, Loyalty Points, Region, Gender
- **Engineered Features:** CLV Score, Return Rate, Engagement Score

### Model
- **Algorithm:** K-Means Clustering (k=4)
- **Pipeline:** StandardScaler → KMeans
- **Saved Files:** `models/pipeline.pkl`, `models/segment_map.pkl`, `models/features.pkl`
        """)

    with tab2:
        st.markdown("### Feature Engineering")
        fe_df = pd.DataFrame([
            {"Feature": "CLV Score", "Formula": "(Income × Spending × Frequency) / 1000",
             "Rationale": "Proxy for Customer Lifetime Value — higher = more profitable"},
            {"Feature": "Return Rate", "Formula": "Returns / (Frequency + 0.1)",
             "Rationale": "Measures product satisfaction & operational cost"},
            {"Feature": "Engagement Score", "Formula": "(Loyalty Points / 50) + Tenure × 5",
             "Rationale": "Composite loyalty & tenure indicator"},
        ])
        st.dataframe(fe_df, use_container_width=True, hide_index=True)

        st.markdown("### Segmentation Model")
        st.markdown("""
**Algorithm:** K-Means Clustering  
**K selection:** Elbow method + silhouette analysis (k=4 optimal)  
**Preprocessing:** StandardScaler (zero mean, unit variance)  
**Pipeline:** Scaler → KMeans stored as single `sklearn.Pipeline` object

```python
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("kmeans", KMeans(n_clusters=4, random_state=42, n_init=10))
])
pipeline.fit(df[features])
```
        """)

        st.markdown("### Segment Labels")
        seg_df = pd.DataFrame([
            {"Cluster ID": k, "Label": v,
             "Customers": len(df[df["Segment_Label"]==v]),
             "Avg CLV": round(df[df["Segment_Label"]==v]["CLV_Score"].mean(),1)}
            for k, v in segment_map.items()
        ])
        st.dataframe(seg_df, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("""
### Application Architecture

```
ml_dashboard/
│
├── app.py                    ← Main Streamlit app (routing + CSS)
├── data/
│   └── customers.csv         ← Final dataset (500 rows)
├── models/
│   ├── pipeline.pkl          ← Trained StandardScaler + KMeans pipeline
│   ├── segment_map.pkl       ← {cluster_id: label} mapping
│   └── features.pkl          ← Feature list for inference
├── pages/
│   ├── overview.py           ← Day 2: KPI cards, charts, filters
│   ├── explorer.py           ← Day 2: Customer search & table
│   ├── predict.py            ← Day 3: Real-time model inference
│   ├── analysis.py           ← Day 2/3: Segment deep-dive
│   ├── recommendations.py    ← Day 1: Business recommendations
│   ├── qa.py                 ← Day 4: Automated QA checks
│   └── documentation.py     ← Day 5: This page
└── utils/
    └── loader.py             ← Cached data & model loaders
```

### Dashboard Pages & Coverage

| Page | Day | Features |
|------|-----|----------|
| Overview | Day 2 | KPI cards, pie chart, scatter, region bar, filters, download |
| Customer Explorer | Day 2 | Search, multi-filter, profile card, data table, export |
| Predict Segment | Day 3 | Real model inference, feature engineering, recommendations |
| Segment Analysis | Day 2/3 | Radar chart, box plots, histograms, stats table |
| Recommendations | Day 1 | Strategy tabs, KPIs, channels, bulk export |
| QA Report | Day 4 | 12 automated checks, data profile, distribution validation |
| Documentation | Day 5 | Full report, methodology, architecture, daily log |
        """)

    with tab4:
        days = [
            ("Day 1", "Dashboard Planning & Application Setup",
             ["Reviewed project scope and dataset requirements",
              "Identified final features: CLV Score, Return Rate, Engagement Score",
              "Chose KMeans (k=4) as final segmentation model",
              "Decided on 7-page dashboard structure",
              "Selected Streamlit as application technology",
              "Defined segment labels and colour scheme"]),
            ("Day 2", "Dashboard Development",
             ["Built Overview page with KPI cards, pie, scatter, bar charts",
              "Implemented multi-filter sidebar controls",
              "Built Customer Explorer with search, filters, profile cards",
              "Built Segment Analysis with radar, box plots, histograms",
              "Built Recommendations page with strategy cards",
              "Added CSV download to all relevant pages"]),
            ("Day 3", "Model / Application Integration",
             ["Loaded pipeline.pkl using pickle + st.cache_resource",
              "Implemented feature engineering logic in predict.py",
              "Accepted live customer input via Streamlit number inputs",
              "Applied StandardScaler → KMeans inference pipeline",
              "Displayed segment label, icon, colour-coded result",
              "Showed segment comparison table vs segment average"]),
            ("Day 4", "Quality Assurance",
             ["Ran 12 automated QA checks via qa.py",
              "Validated: data shape, nulls, unique IDs, feature presence",
              "Validated: model loading, prediction range, cluster mapping",
              "Generated data profile summary (describe() table)",
              "Confirmed all segments have > 1% representation",
              "All 12 checks passed — dashboard marked production-ready"]),
            ("Day 5", "Documentation & Presentation",
             ["Wrote full project documentation in documentation.py",
              "Documented feature engineering formulas and rationale",
              "Documented file architecture and page coverage table",
              "Compiled day-by-day activity log",
              "Prepared dashboard for final presentation"]),
        ]
        for day, title, tasks in days:
            with st.expander(f"**{day} — {title}**", expanded=True):
                for task in tasks:
                    st.markdown(f"<div style='color:#a0aec0; padding:4px 0; border-bottom:1px solid #1e2235;'>✅ {task}</div>", unsafe_allow_html=True)

    st.markdown("---")
    report_text = """ML INTERNSHIP — CUSTOMER SEGMENTATION DASHBOARD
Project Documentation Report
==============================================

TEAM / INTERN: ML Intern
TECHNOLOGY: Python · Streamlit · Scikit-learn · Plotly
DATASET: 500 customers · 11 raw features · 3 engineered features
MODEL: KMeans (k=4) with StandardScaler pipeline

SEGMENTS:
  0 → Budget Shoppers
  1 → High Value
  2 → At-Risk
  3 → Loyal Mid-Tier

PAGES BUILT:
  1. Overview Dashboard
  2. Customer Explorer
  3. Predict Segment (live model)
  4. Segment Analysis
  5. Business Recommendations
  6. QA Report
  7. Documentation

QA: 12/12 checks passed

DAY 1: Planning & Setup
DAY 2: Dashboard Development
DAY 3: Model Integration
DAY 4: QA Checks
DAY 5: Documentation & Presentation
"""
    st.download_button("⬇️ Download Full Report (TXT)", report_text.encode(),
                       "project_report.txt", "text/plain")
