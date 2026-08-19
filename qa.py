import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.loader import load_data, load_model

def show():
    df = load_data()
    pipeline, segment_map, features = load_model()

    st.markdown("## 📋 Quality Assurance Report")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Automated checks validating data quality, model integrity, and dashboard completeness — Day 4 deliverable.</div>", unsafe_allow_html=True)

    checks = []

    # 1. Data checks
    checks.append(("Dataset Loaded", len(df) > 0, f"{len(df)} rows found"))
    checks.append(("No Missing Values", df.isnull().sum().sum() == 0,
                   f"{df.isnull().sum().sum()} nulls detected"))
    checks.append(("CustomerID Unique", df["CustomerID"].is_unique,
                   f"{df['CustomerID'].nunique()} unique IDs"))
    checks.append(("All 4 Segments Present", df["Segment_Label"].nunique() == 4,
                   f"Segments found: {', '.join(df['Segment_Label'].unique())}"))
    checks.append(("Engineered Features Present",
                   all(c in df.columns for c in ["CLV_Score","Return_Rate","Engagement_Score"]),
                   "CLV_Score, Return_Rate, Engagement_Score all present"))
    checks.append(("Spending Score in Range (1–100)",
                   df["Spending_Score"].between(1,100).all(),
                   f"Min: {df['Spending_Score'].min()}, Max: {df['Spending_Score'].max()}"))
    checks.append(("Annual Income > 0",
                   (df["Annual_Income_K"] > 0).all(),
                   f"Min: {df['Annual_Income_K'].min()}K"))

    # 2. Model checks
    try:
        X = df[features]
        preds = pipeline.predict(X)
        checks.append(("Model Loads Successfully", True, "Pipeline loaded from pickle"))
        checks.append(("Model Predictions Match Labels",
                       set(preds) == set(segment_map.keys()),
                       f"Cluster IDs: {sorted(set(preds))}"))
        checks.append(("All Features Available for Prediction",
                       all(f in df.columns for f in features),
                       f"Features: {features}"))
    except Exception as e:
        checks.append(("Model Check Failed", False, str(e)))

    # 3. Segment distribution checks
    seg_counts = df["Segment_Label"].value_counts()
    checks.append(("No Segment < 1% of Total",
                   (seg_counts / len(df) > 0.01).all(),
                   "All segments have reasonable representation"))
    checks.append(("CLV Score Non-Negative",
                   (df["CLV_Score"] >= 0).all(),
                   f"Min CLV: {df['CLV_Score'].min():.2f}"))

    # ── Render checks ─────────────────────────────────────────────
    pass_count = sum(1 for _, ok, _ in checks if ok)
    fail_count = len(checks) - pass_count

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Checks", len(checks))
    col2.metric("✅ Passed", pass_count)
    col3.metric("❌ Failed", fail_count)

    if fail_count == 0:
        st.success("🎉 All QA checks passed! Dashboard is production-ready.")
    else:
        st.warning(f"⚠️ {fail_count} check(s) failed. Review below.")

    st.markdown("### Check Results")
    for name, ok, detail in checks:
        status  = "✅" if ok else "❌"
        bg      = "#1a4731" if ok else "#3d1a1a"
        border  = "#68d391" if ok else "#fc8181"
        st.markdown(f"""
        <div style='background:{bg}; border:1px solid {border}; border-radius:8px;
                    padding:12px 16px; margin-bottom:6px; display:flex; gap:12px; align-items:center;'>
            <span style='font-size:18px;'>{status}</span>
            <div>
                <div style='color:#e2e8f0; font-weight:600;'>{name}</div>
                <div style='color:#a0aec0; font-size:12px;'>{detail}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Data profiling ────────────────────────────────────────────
    st.markdown("### 📊 Data Profile Summary")
    numeric_cols = ["Age","Annual_Income_K","Spending_Score","Purchase_Frequency",
                    "Avg_Order_Value","CLV_Score","Return_Rate","Engagement_Score"]
    profile = df[numeric_cols].describe().round(2)
    st.dataframe(profile, use_container_width=True)

    # ── Segment size table ────────────────────────────────────────
    st.markdown("### Segment Distribution Check")
    dist = df["Segment_Label"].value_counts().reset_index()
    dist.columns = ["Segment", "Count"]
    dist["% of Total"] = (dist["Count"] / len(df) * 100).round(1)
    dist["Status"] = dist["% of Total"].apply(lambda x: "✅ OK" if x > 1 else "⚠️ Underrepresented")
    st.dataframe(dist, use_container_width=True, hide_index=True)
