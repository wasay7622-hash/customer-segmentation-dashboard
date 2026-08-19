import pandas as pd
import pickle
import streamlit as st
import os

BASE = os.path.dirname(os.path.dirname(__file__))

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE, "data", "customers.csv"))
    return df

@st.cache_resource
def load_model():
    with open(os.path.join(BASE, "models", "pipeline.pkl"), "rb") as f:
        pipeline = pickle.load(f)
    with open(os.path.join(BASE, "models", "segment_map.pkl"), "rb") as f:
        segment_map = pickle.load(f)
    with open(os.path.join(BASE, "models", "features.pkl"), "rb") as f:
        features = pickle.load(f)
    return pipeline, segment_map, features

SEGMENT_COLORS = {
    "High Value":      "#68d391",
    "Loyal Mid-Tier":  "#63b3ed",
    "Budget Shoppers": "#f6ad55",
    "At-Risk":         "#fc8181",
}

SEGMENT_ICONS = {
    "High Value":      "💎",
    "Loyal Mid-Tier":  "🌟",
    "Budget Shoppers": "🛍️",
    "At-Risk":         "⚠️",
}

BADGE_CLASS = {
    "High Value":      "badge-hv",
    "Loyal Mid-Tier":  "badge-lm",
    "Budget Shoppers": "badge-bs",
    "At-Risk":         "badge-ar",
}

def kpi(title, value, delta=None, delta_pos=True):
    delta_html = ""
    if delta:
        cls = "delta-pos" if delta_pos else "delta-neg"
        arrow = "▲" if delta_pos else "▼"
        delta_html = f"<div class='kpi-delta {cls}'>{arrow} {delta}</div>"
    return f"""
    <div class='kpi-card'>
        <div class='kpi-title'>{title}</div>
        <div class='kpi-value'>{value}</div>
        {delta_html}
    </div>"""
