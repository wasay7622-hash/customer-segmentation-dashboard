# 🎯 Customer Segmentation ML Dashboard

> **ML Internship Project — Day 1 through Day 5**  
> Built with Streamlit + Scikit-learn + Plotly

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate data + train model (first time only)
python3 -c "exec(open('generate_data.py').read())"

# 3. Launch dashboard
streamlit run app.py
```

## Project Structure
```
ml_dashboard/
├── app.py                 ← Main app + navigation
├── data/customers.csv     ← Dataset (500 customers)
├── models/
│   ├── pipeline.pkl       ← Trained KMeans pipeline
│   ├── segment_map.pkl    ← Cluster → label mapping
│   └── features.pkl       ← Feature list
├── pages/
│   ├── overview.py        ← KPI + charts dashboard
│   ├── explorer.py        ← Customer search & filter
│   ├── predict.py         ← Live segment prediction
│   ├── analysis.py        ← Segment deep-dive
│   ├── recommendations.py ← Business strategies
│   ├── qa.py              ← QA checks (Day 4)
│   └── documentation.py  ← Full report (Day 5)
└── utils/loader.py        ← Data + model loaders
```

## Dashboard Pages
| Page | Purpose |
|------|---------|
| Overview | KPI cards, segment pie, income vs spending charts |
| Customer Explorer | Search customers, filter by segment/region/income |
| Predict Segment | Enter customer data → model assigns segment live |
| Segment Analysis | Radar chart, box plots, deep dive stats |
| Recommendations | Marketing strategies per segment |
| QA Report | 12 automated quality checks |
| Documentation | Full project write-up and methodology |

## Segments
- 💎 **High Value** — Top spenders, high CLV, brand champions
- 🌟 **Loyal Mid-Tier** — Consistent, growth potential
- 🛍️ **Budget Shoppers** — Price-sensitive, volume buyers
- ⚠️ **At-Risk** — Disengaged, needs reactivation
