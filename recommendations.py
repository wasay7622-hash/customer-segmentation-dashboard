import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.loader import load_data, SEGMENT_COLORS, SEGMENT_ICONS

RECS = {
    "High Value": {
        "icon": "💎",
        "color": "#68d391",
        "subtitle": "Protect, Deepen, Reward",
        "profile": "Top-tier customers with high income, spending, and engagement. These are your brand champions.",
        "strategic": [
            ("VIP Program", "Launch an exclusive tier with concierge support, early product launches, and premium packaging."),
            ("Upsell Premium Lines", "Introduce curated bundles, limited editions, or premium subscriptions specifically for this tier."),
            ("Referral Incentives", "Leverage their networks — offer referral bonuses to bring in similar high-value customers."),
            ("Dedicated CRM Flows", "Assign personalized account managers and automate anniversary / milestone outreach."),
        ],
        "kpis": ["Retention Rate > 90%", "CLV Growth > 15% YoY", "NPS Score > 70"],
        "channel": "Email (personalized) · Direct sales rep · Exclusive events"
    },
    "Loyal Mid-Tier": {
        "icon": "🌟",
        "color": "#63b3ed",
        "subtitle": "Nurture, Upgrade, Grow",
        "profile": "Reliable, engaged customers with consistent purchase patterns. Strong growth potential with the right nudge.",
        "strategic": [
            ("Tier Upgrade Campaigns", "Show them exactly how close they are to VIP status and what they'd unlock."),
            ("Cross-Sell Automation", "Use purchase history to recommend complementary products via email triggers."),
            ("Gamified Loyalty", "Introduce point multipliers, streak rewards, and milestone badges to increase frequency."),
            ("Community Building", "Invite to beta testing groups or product feedback panels to deepen brand attachment."),
        ],
        "kpis": ["Spend Increase > 20%", "Purchase Frequency +2/yr", "Upgrade Rate to High Value > 10%"],
        "channel": "Email nurture sequences · Push notifications · Loyalty app"
    },
    "Budget Shoppers": {
        "icon": "🛍️",
        "color": "#f6ad55",
        "subtitle": "Value, Volume, Habit",
        "profile": "Price-sensitive customers who respond strongly to deals. High potential for volume-driven revenue.",
        "strategic": [
            ("Flash Sale Targeting", "Run 48-hour flash sales with personalized discount codes for this segment."),
            ("Bundle & Save Offers", "Package popular products at a perceived value to increase average order size."),
            ("Free Shipping Thresholds", "Set basket minimums just above their typical order value to encourage larger carts."),
            ("Entry Loyalty Points", "Offer points on every purchase to build habit and reduce price-based switching."),
        ],
        "kpis": ["Avg Order Value +15%", "Purchase Frequency +30%", "Churn Rate < 25%"],
        "channel": "SMS campaigns · Social media ads · Promotional email blasts"
    },
    "At-Risk": {
        "icon": "⚠️",
        "color": "#fc8181",
        "subtitle": "Reactivate, Resolve, Retain",
        "profile": "Disengaged customers with declining activity and high return rates. Immediate intervention needed.",
        "strategic": [
            ("Win-Back Campaigns", "Send a 3-email series: empathy → incentive (20% off) → urgency (offer expiring soon)."),
            ("Return Root Cause Analysis", "Survey at-risk customers to identify product quality or service pain points."),
            ("Proactive Support Outreach", "Trigger a personal call or chat from the support team for high-value at-risk accounts."),
            ("Re-Engagement Offers", "Provide time-limited 'We Miss You' discounts with easy one-click return to purchase."),
        ],
        "kpis": ["Reactivation Rate > 15%", "Return Rate Reduction > 20%", "NPS Recovery > +10 points"],
        "channel": "Direct email (win-back) · Phone outreach · SMS reactivation"
    },
}

def show():
    df = load_data()

    st.markdown("## 💡 Business Recommendations")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Data-driven marketing strategies derived from KMeans segmentation — ready to present to stakeholders.</div>", unsafe_allow_html=True)

    # ── Segment selector ─────────────────────────────────────────
    seg_options = list(RECS.keys())
    tabs = st.tabs([f"{RECS[s]['icon']} {s}" for s in seg_options])

    for tab, seg in zip(tabs, seg_options):
        with tab:
            r = RECS[seg]
            color = r["color"]
            seg_df = df[df["Segment_Label"] == seg]

            # Header
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#1e2235,#252a3d);
                        border-left:4px solid {color};
                        border-radius:0 12px 12px 0;
                        padding:20px 24px; margin-bottom:20px;'>
                <div style='color:{color}; font-size:13px; font-weight:700;
                            letter-spacing:2px; text-transform:uppercase;'>{r["subtitle"]}</div>
                <div style='color:#a0aec0; margin-top:8px;'>{r["profile"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Customers", f"{len(seg_df):,}")
            m2.metric("Avg CLV Score", f"{seg_df['CLV_Score'].mean():.0f}")
            m3.metric("Avg Spending Score", f"{seg_df['Spending_Score'].mean():.1f}")
            m4.metric("Avg Return Rate", f"{seg_df['Return_Rate'].mean():.2f}")

            st.markdown("### 🎯 Strategic Recommendations")
            for title, body in r["strategic"]:
                st.markdown(f"""
                <div style='background:#1a1d2e; border:1px solid #2d3748;
                            border-radius:10px; padding:16px; margin-bottom:10px;'>
                    <div style='color:{color}; font-weight:700; margin-bottom:6px;'>📌 {title}</div>
                    <div style='color:#a0aec0;'>{body}</div>
                </div>
                """, unsafe_allow_html=True)

            col_kpi, col_ch = st.columns(2)
            with col_kpi:
                st.markdown("### 📏 Target KPIs")
                for kpi in r["kpis"]:
                    st.markdown(f"<div style='color:#a0aec0; padding:4px 0;'>✅ {kpi}</div>", unsafe_allow_html=True)
            with col_ch:
                st.markdown("### 📡 Recommended Channels")
                st.markdown(f"<div style='color:#a0aec0;'>{r['channel']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    # ── Master recommendations download ──────────────────────────
    rows = []
    for seg, r in RECS.items():
        for title, body in r["strategic"]:
            rows.append({"Segment": seg, "Strategy": title, "Detail": body,
                         "Target KPIs": " | ".join(r["kpis"]), "Channels": r["channel"]})
    rec_df = pd.DataFrame(rows)
    csv = rec_df.to_csv(index=False).encode()
    st.download_button("⬇️ Export All Recommendations (CSV)", csv, "recommendations.csv", "text/csv")
