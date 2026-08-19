import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.loader import load_data, SEGMENT_COLORS, BADGE_CLASS, SEGMENT_ICONS

def show():
    df = load_data()

    st.markdown("## 👥 Customer Explorer")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Search, filter, and explore individual customer profiles.</div>", unsafe_allow_html=True)

    # ── Search + Filters ─────────────────────────────────────────
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    with col1:
        search = st.text_input("🔍 Search by Customer ID", placeholder="e.g. CUST1042")
    with col2:
        seg_filter = st.selectbox("Segment", ["All"] + list(df["Segment_Label"].unique()))
    with col3:
        region_filter = st.selectbox("Region", ["All"] + list(df["Region"].unique()))
    with col4:
        gender_filter = st.selectbox("Gender", ["All", "Male", "Female"])

    col5, col6 = st.columns(2)
    with col5:
        income_range = st.slider("Annual Income (K)", int(df["Annual_Income_K"].min()),
                                  int(df["Annual_Income_K"].max()),
                                  (int(df["Annual_Income_K"].min()), int(df["Annual_Income_K"].max())))
    with col6:
        spending_range = st.slider("Spending Score", 1, 100, (1, 100))

    dff = df.copy()
    if search:
        dff = dff[dff["CustomerID"].str.contains(search.upper())]
    if seg_filter != "All":
        dff = dff[dff["Segment_Label"] == seg_filter]
    if region_filter != "All":
        dff = dff[dff["Region"] == region_filter]
    if gender_filter != "All":
        dff = dff[dff["Gender"] == gender_filter]
    dff = dff[
        (dff["Annual_Income_K"] >= income_range[0]) &
        (dff["Annual_Income_K"] <= income_range[1]) &
        (dff["Spending_Score"] >= spending_range[0]) &
        (dff["Spending_Score"] <= spending_range[1])
    ]

    st.markdown(f"<div style='color:#a0aec0; margin-bottom:12px;'>Showing <b style='color:#e2e8f0;'>{len(dff)}</b> customers</div>", unsafe_allow_html=True)

    # ── Customer Profile Card (if exact match) ───────────────────
    if search and len(dff) == 1:
        c = dff.iloc[0]
        icon = SEGMENT_ICONS.get(c["Segment_Label"], "👤")
        color = SEGMENT_COLORS.get(c["Segment_Label"], "#a0aec0")
        st.markdown(f"""
        <div style='background:#1e2235; border:1px solid {color}; border-radius:16px; padding:24px; margin-bottom:20px;'>
            <div style='display:flex; align-items:center; gap:16px; margin-bottom:20px;'>
                <div style='font-size:40px;'>{icon}</div>
                <div>
                    <div style='color:#e2e8f0; font-size:22px; font-weight:700;'>{c["CustomerID"]}</div>
                    <div style='color:{color}; font-size:13px; font-weight:600;'>{c["Segment_Label"]}</div>
                </div>
            </div>
            <div style='display:grid; grid-template-columns: repeat(4,1fr); gap:12px;'>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Age</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>{c["Age"]}</div>
                </div>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Income</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>${c["Annual_Income_K"]}K</div>
                </div>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Spending Score</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>{c["Spending_Score"]}</div>
                </div>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>CLV Score</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>{c["CLV_Score"]:.0f}</div>
                </div>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Region</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>{c["Region"]}</div>
                </div>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Tenure</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>{c["Tenure_Years"]}y</div>
                </div>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Loyalty Pts</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>{int(c["Loyalty_Points"]):,}</div>
                </div>
                <div style='background:#252a3d; padding:12px; border-radius:8px;'>
                    <div style='color:#8892b0; font-size:11px; text-transform:uppercase; letter-spacing:1px;'>Returns</div>
                    <div style='color:#e2e8f0; font-size:18px; font-weight:700;'>{int(c["Returns_Count"])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Data Table ───────────────────────────────────────────────
    show_cols = ["CustomerID","Age","Gender","Region","Annual_Income_K",
                 "Spending_Score","Purchase_Frequency","Avg_Order_Value",
                 "CLV_Score","Tenure_Years","Loyalty_Points","Segment_Label"]

    st.dataframe(
        dff[show_cols].sort_values("CLV_Score", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=400
    )

    # ── Download ─────────────────────────────────────────────────
    csv = dff[show_cols].to_csv(index=False).encode()
    st.download_button("⬇️ Export Table (CSV)", csv, "customer_search_results.csv", "text/csv")
