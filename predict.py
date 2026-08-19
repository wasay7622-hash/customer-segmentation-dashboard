import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.loader import load_model, load_data, SEGMENT_COLORS, SEGMENT_ICONS

RECS = {
    "High Value": {
        "desc": "These customers generate the highest revenue. They shop frequently with high spending scores and strong CLV.",
        "actions": [
            "🎁  Offer VIP loyalty rewards and exclusive early access to new products",
            "💌  Assign dedicated account managers for personalized outreach",
            "📦  Provide premium subscription tiers with added perks",
            "🔁  Upsell premium product lines and bundles",
        ],
        "risk": "Low churn risk — high satisfaction and engagement.",
        "priority": "🔴 Top Priority"
    },
    "Loyal Mid-Tier": {
        "desc": "Consistent, reliable customers with moderate spending. They are engaged and have growth potential.",
        "actions": [
            "📈  Introduce tiered loyalty programs to encourage higher spend",
            "🎯  Cross-sell complementary product categories",
            "📬  Send personalized monthly newsletters and curated picks",
            "💰  Offer referral bonuses to leverage word-of-mouth",
        ],
        "risk": "Low churn risk — loyal but may plateau without incentive.",
        "priority": "🟡 Growth Focus"
    },
    "Budget Shoppers": {
        "desc": "Price-sensitive customers who respond well to discounts and value deals. High volume, lower order values.",
        "actions": [
            "🏷️  Target with flash sales, discount codes, and bundle deals",
            "📲  Engage via social media campaigns with value messaging",
            "🛒  Offer free-shipping thresholds to increase basket size",
            "⭐  Introduce entry-level loyalty points to drive repeat visits",
        ],
        "risk": "Moderate churn risk — sensitive to price changes.",
        "priority": "🟠 Value Retention"
    },
    "At-Risk": {
        "desc": "Customers showing signs of disengagement — declining purchase frequency, high returns, or low loyalty.",
        "actions": [
            "🚨  Launch immediate win-back email campaigns with incentives",
            "📞  Trigger proactive customer support outreach",
            "💬  Survey to identify pain points and reduce return rates",
            "🎫  Offer time-limited discounts to re-activate purchases",
        ],
        "risk": "High churn risk — immediate action recommended.",
        "priority": "🔴 Urgent Action"
    },
}

def show():
    pipeline, segment_map, features = load_model()
    df = load_data()

    st.markdown("## 🤖 Predict Customer Segment")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Enter customer details below to run the trained KMeans model and classify them into a segment in real time.</div>", unsafe_allow_html=True)

    st.markdown("### 📋 Customer Input Form")
    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input("Age", min_value=18, max_value=90, value=35)
        income = st.number_input("Annual Income (K $)", min_value=10, max_value=300, value=60)
        spending = st.slider("Spending Score (1–100)", 1, 100, 50)

    with c2:
        freq = st.number_input("Purchase Frequency (per year)", min_value=1, max_value=100, value=12)
        avg_order = st.number_input("Avg Order Value ($)", min_value=5.0, max_value=1000.0, value=120.0, step=5.0)
        tenure = st.number_input("Tenure (years)", min_value=0.1, max_value=20.0, value=2.5, step=0.5)

    with c3:
        returns = st.number_input("Returns Count", min_value=0, max_value=50, value=1)
        loyalty = st.number_input("Loyalty Points", min_value=0, max_value=10000, value=500)

    # ── Feature Engineering (same as training) ───────────────────
    clv_score       = (income * spending * freq) / 1000
    return_rate     = returns / (freq + 0.1)
    engagement_score = (loyalty / 50) + tenure * 5

    st.markdown("---")
    with st.expander("🔬 Engineered Features (auto-computed)", expanded=True):
        e1, e2, e3 = st.columns(3)
        e1.metric("CLV Score", f"{clv_score:.1f}")
        e2.metric("Return Rate", f"{return_rate:.3f}")
        e3.metric("Engagement Score", f"{engagement_score:.1f}")

    # ── Predict ──────────────────────────────────────────────────
    if st.button("🚀 Predict Segment", use_container_width=True):
        input_data = pd.DataFrame([{
            "Age": age,
            "Annual_Income_K": income,
            "Spending_Score": spending,
            "Purchase_Frequency": freq,
            "Avg_Order_Value": avg_order,
            "CLV_Score": clv_score,
            "Return_Rate": return_rate,
            "Engagement_Score": engagement_score,
        }])

        segment_id = pipeline.predict(input_data[features])[0]
        segment_label = segment_map[segment_id]
        color = SEGMENT_COLORS[segment_label]
        icon  = SEGMENT_ICONS[segment_label]
        info  = RECS[segment_label]

        st.markdown(f"""
        <div class='pred-box' style='border-color:{color}; margin-top:20px;'>
            <div style='font-size:48px; margin-bottom:8px;'>{icon}</div>
            <div class='pred-label'>This customer belongs to</div>
            <div class='pred-segment' style='color:{color};'>{segment_label}</div>
            <div style='color:#8892b0; font-size:13px; margin-top:10px;'>{info["priority"]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"#### Segment Profile")
            st.markdown(f"<div style='color:#a0aec0;'>{info['desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<br><div style='color:#fc8181;'><b>Risk:</b> {info['risk']}</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown(f"#### Recommended Actions")
            for action in info["actions"]:
                st.markdown(f"<div style='color:#a0aec0; padding:6px 0; border-bottom:1px solid #2d3748;'>{action}</div>", unsafe_allow_html=True)

        # ── Segment Stats comparison ──────────────────────────────
        st.markdown("#### How this customer compares to their segment")
        seg_df = df[df["Segment_Label"] == segment_label]
        stats = seg_df[["Annual_Income_K","Spending_Score","CLV_Score","Engagement_Score"]].mean()
        user_vals = {"Annual_Income_K": income, "Spending_Score": spending,
                     "CLV_Score": clv_score, "Engagement_Score": engagement_score}

        comp_df = pd.DataFrame({
            "Metric": ["Income (K$)", "Spending Score", "CLV Score", "Engagement Score"],
            "This Customer": [income, spending, round(clv_score,1), round(engagement_score,1)],
            "Segment Average": [round(stats["Annual_Income_K"],1), round(stats["Spending_Score"],1),
                                round(stats["CLV_Score"],1), round(stats["Engagement_Score"],1)]
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
