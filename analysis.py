import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.loader import load_data, SEGMENT_COLORS, SEGMENT_ICONS

DARK_BG  = "rgba(0,0,0,0)"
GRID_CLR = "#2d3748"
TEXT_CLR = "#a0aec0"

def dark(fig):
    fig.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
                      font_color=TEXT_CLR, margin=dict(l=10,r=10,t=30,b=10))
    fig.update_xaxes(gridcolor=GRID_CLR, linecolor=GRID_CLR)
    fig.update_yaxes(gridcolor=GRID_CLR, linecolor=GRID_CLR)
    return fig

def show():
    df = load_data()

    st.markdown("## 📈 Segment Deep-Dive Analysis")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Drill into any segment to understand its demographics, behaviour patterns, and financial characteristics.</div>", unsafe_allow_html=True)

    # ── Segment selector ─────────────────────────────────────────
    selected = st.selectbox("Select a Segment to Analyse",
                            ["All Segments"] + list(df["Segment_Label"].unique()))
    dff = df if selected == "All Segments" else df[df["Segment_Label"] == selected]

    # ── Summary stats table ──────────────────────────────────────
    st.markdown("### 📊 Segment Summary Statistics")
    agg = df.groupby("Segment_Label").agg(
        Customers=("CustomerID","count"),
        Avg_Age=("Age","mean"),
        Avg_Income=("Annual_Income_K","mean"),
        Avg_Spending=("Spending_Score","mean"),
        Avg_Freq=("Purchase_Frequency","mean"),
        Avg_CLV=("CLV_Score","mean"),
        Avg_Engagement=("Engagement_Score","mean"),
        Avg_ReturnRate=("Return_Rate","mean"),
    ).round(1).reset_index()
    agg.columns = ["Segment","Customers","Avg Age","Avg Income(K)","Avg Spending",
                   "Avg Freq/yr","Avg CLV","Avg Engagement","Avg Return Rate"]
    st.dataframe(agg, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Charts ───────────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Age Distribution**")
        fig = px.histogram(dff, x="Age", color="Segment_Label",
                           color_discrete_map=SEGMENT_COLORS, nbins=20, opacity=0.8)
        fig.update_layout(legend=dict(font_color=TEXT_CLR))
        st.plotly_chart(dark(fig), use_container_width=True)

    with c2:
        st.markdown("**CLV Score Distribution**")
        fig2 = px.box(df, x="Segment_Label", y="CLV_Score",
                      color="Segment_Label", color_discrete_map=SEGMENT_COLORS,
                      points="outliers")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(dark(fig2), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("**Income vs CLV (coloured by Segment)**")
        fig3 = px.scatter(dff, x="Annual_Income_K", y="CLV_Score",
                          color="Segment_Label", color_discrete_map=SEGMENT_COLORS,
                          size="Spending_Score", opacity=0.7,
                          hover_data=["CustomerID","Age"])
        fig3.update_layout(legend=dict(font_color=TEXT_CLR))
        st.plotly_chart(dark(fig3), use_container_width=True)

    with c4:
        st.markdown("**Engagement vs Return Rate**")
        fig4 = px.scatter(dff, x="Engagement_Score", y="Return_Rate",
                          color="Segment_Label", color_discrete_map=SEGMENT_COLORS,
                          opacity=0.7, hover_data=["CustomerID"])
        fig4.update_layout(legend=dict(font_color=TEXT_CLR))
        st.plotly_chart(dark(fig4), use_container_width=True)

    # ── Radar chart ──────────────────────────────────────────────
    st.markdown("### 🕸️ Segment Radar (Normalized Profiles)")
    metrics = ["Annual_Income_K","Spending_Score","Purchase_Frequency",
               "CLV_Score","Engagement_Score","Avg_Order_Value"]
    agg_r = df.groupby("Segment_Label")[metrics].mean()
    agg_norm = (agg_r - agg_r.min()) / (agg_r.max() - agg_r.min() + 1e-6)

    fig5 = go.Figure()
    for seg in agg_norm.index:
        vals = list(agg_norm.loc[seg]) + [agg_norm.loc[seg][0]]
        cats = metrics + [metrics[0]]
        fig5.add_trace(go.Scatterpolar(
            r=vals, theta=cats, fill="toself",
            name=seg, line_color=SEGMENT_COLORS.get(seg,"#fff"),
            opacity=0.6
        ))
    fig5.update_layout(
        polar=dict(bgcolor="rgba(30,34,53,0.8)",
                   radialaxis=dict(visible=True, color=TEXT_CLR, gridcolor=GRID_CLR),
                   angularaxis=dict(color=TEXT_CLR)),
        paper_bgcolor=DARK_BG, font_color=TEXT_CLR,
        legend=dict(font_color=TEXT_CLR)
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Download
    csv = dff.to_csv(index=False).encode()
    st.download_button("⬇️ Export Segment Data", csv, f"{selected.replace(' ','_')}_data.csv", "text/csv")
