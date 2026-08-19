import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.loader import load_data, load_model, SEGMENT_COLORS, SEGMENT_ICONS, kpi

DARK_BG   = "#0f1117"
CARD_BG   = "#1e2235"
GRID_CLR  = "#2d3748"
TEXT_CLR  = "#a0aec0"

def make_dark(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=TEXT_CLR,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    fig.update_xaxes(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickfont_color=TEXT_CLR)
    fig.update_yaxes(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickfont_color=TEXT_CLR)
    return fig

def show():
    df = load_data()

    st.markdown("## 📊 Overview Dashboard")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Real-time summary of your customer segmentation model — 500 customers, 4 segments.</div>", unsafe_allow_html=True)

    # ── Filters ─────────────────────────────────────────────────
    with st.expander("🔧 Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            regions = st.multiselect("Region", df["Region"].unique(), default=list(df["Region"].unique()))
        with col2:
            genders = st.multiselect("Gender", df["Gender"].unique(), default=list(df["Gender"].unique()))
        with col3:
            segments = st.multiselect("Segment", df["Segment_Label"].unique(), default=list(df["Segment_Label"].unique()))

    mask = (
        df["Region"].isin(regions) &
        df["Gender"].isin(genders) &
        df["Segment_Label"].isin(segments)
    )
    dff = df[mask]

    # ── KPI Row ──────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(kpi("Total Customers", f"{len(dff):,}", "Filtered view"), unsafe_allow_html=True)
    with k2: st.markdown(kpi("Avg Income (K)", f"${dff['Annual_Income_K'].mean():.0f}K", "+3.2% vs last period"), unsafe_allow_html=True)
    with k3: st.markdown(kpi("Avg Spending Score", f"{dff['Spending_Score'].mean():.1f}", None), unsafe_allow_html=True)
    with k4: st.markdown(kpi("Avg CLV Score", f"{dff['CLV_Score'].mean():.0f}", "+8.1%"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Pie + Bar ─────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Segment Distribution**")
        seg_counts = dff["Segment_Label"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        colors = [SEGMENT_COLORS.get(s, "#a0aec0") for s in seg_counts["Segment"]]
        fig = px.pie(seg_counts, values="Count", names="Segment",
                     color_discrete_sequence=colors, hole=0.5)
        fig.update_traces(textfont_color="white", textfont_size=12)
        st.plotly_chart(make_dark(fig), use_container_width=True)

    with c2:
        st.markdown("**Avg Income vs Spending by Segment**")
        agg = dff.groupby("Segment_Label").agg(
            Income=("Annual_Income_K","mean"),
            Spending=("Spending_Score","mean")
        ).reset_index()
        fig2 = go.Figure()
        for col_name, color in [("Income","#4c6ef5"),("Spending","#68d391")]:
            fig2.add_trace(go.Bar(
                x=agg["Segment_Label"], y=agg[col_name],
                name=col_name, marker_color=color, opacity=0.85
            ))
        fig2.update_layout(barmode="group", legend=dict(font_color=TEXT_CLR))
        st.plotly_chart(make_dark(fig2), use_container_width=True)

    # ── Row 2: Scatter + Region ──────────────────────────────────
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("**Income vs Spending Score (Scatter)**")
        fig3 = px.scatter(
            dff, x="Annual_Income_K", y="Spending_Score",
            color="Segment_Label",
            color_discrete_map=SEGMENT_COLORS,
            hover_data=["CustomerID","Age"],
            opacity=0.7, size_max=8
        )
        st.plotly_chart(make_dark(fig3), use_container_width=True)

    with c4:
        st.markdown("**Customers by Region & Segment**")
        reg_seg = dff.groupby(["Region","Segment_Label"]).size().reset_index(name="Count")
        fig4 = px.bar(reg_seg, x="Region", y="Count", color="Segment_Label",
                      color_discrete_map=SEGMENT_COLORS)
        fig4.update_layout(legend=dict(font_color=TEXT_CLR))
        st.plotly_chart(make_dark(fig4), use_container_width=True)

    # ── Download ─────────────────────────────────────────────────
    st.markdown("---")
    csv = dff.to_csv(index=False).encode()
    st.download_button("⬇️ Download Filtered Data (CSV)", csv, "filtered_customers.csv", "text/csv")
