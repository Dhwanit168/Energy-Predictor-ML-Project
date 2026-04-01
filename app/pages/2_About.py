import streamlit as st
from pathlib import Path

st.set_page_config(page_title="About", page_icon="ℹ️")

st.title("ℹ️ About This Project")
st.markdown("---")

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

# ── Project Objective ─────────────────────────
st.subheader("Project Objective")

st.markdown("""
Buildings consume a large portion of global electricity.  
This project demonstrates how **machine learning can predict building energy consumption (kWh)** using environmental conditions, building characteristics, and usage patterns.

The goal is to support **better energy planning and efficient building management**.
""")

st.markdown("---")

# ── Machine Learning Model ────────────────────
st.subheader("Machine Learning Model")

st.markdown("""
The application uses a **Random Forest Regressor**.

Random Forest is an ensemble model that builds multiple decision trees and averages their predictions.  
It performs well for energy prediction because it can capture **non-linear relationships between variables**.
""")

st.markdown("---")

# ── Feature Engineering ───────────────────────
st.subheader("Feature Engineering")

st.markdown("""
Several engineered variables were created to improve prediction accuracy.

Examples include:

- HVAC × Occupancy  
- HVAC × Square Footage  
- Temperature × Occupancy  
- Renewable Energy per SqFt  
- Temperature² and Occupancy²
""")

st.markdown("---")

# ── Dataset Insights ──────────────────────────
st.subheader("Dataset Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Energy Consumption Distribution")
    st.image(ASSETS / "graph1.png", use_container_width=True)
    st.caption("Shows how energy values are distributed across the dataset.")

with col2:
    st.markdown("#### Occupancy vs Energy Consumption")
    st.image(ASSETS / "graph5.png", use_container_width=True)
    st.caption("Buildings with higher occupancy generally consume more energy.")

st.markdown("---")

# ── Model Analysis ────────────────────────────
st.subheader("Model Analysis")

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Feature Importance")
    st.image(ASSETS / "graph3.png", use_container_width=True)
    st.caption("Highlights which variables influence the prediction the most.")

with col4:
    st.markdown("#### Actual vs Predicted Energy")
    st.image(ASSETS / "graph4.png", use_container_width=True)
    st.caption("Compares real energy values with the model's predictions.")

st.markdown("---")

# ── Gauge Explanation ─────────────────────────
st.subheader("Energy Gauge Interpretation")

st.markdown("""
🟢 **Green (≤ 70 kWh)** — Efficient energy usage  
🟠 **Orange (70 – 85 kWh)** — Moderate consumption  
🔴 **Red (> 85 kWh)** — High energy consumption
""")

st.markdown("---")

# ── Tech Stack ────────────────────────────────
st.subheader("Technology Stack")

st.markdown("""
- **Streamlit** – Web application framework  
- **Pandas & NumPy** – Data processing  
- **Scikit-learn** – Machine learning model  
- **Plotly** – Interactive visualizations
""")

st.markdown("---")

# ── Team ──────────────────────────────────────
st.subheader("Project Team")

st.markdown("""
Dhwanit Vibhani  
Kashyap Galiya  
Smit Desai
""")