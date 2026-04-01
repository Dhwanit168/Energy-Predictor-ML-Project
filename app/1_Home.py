import streamlit as st

st.set_page_config(page_title="Energy Predictor", page_icon="⚡", layout="wide")

st.title("⚡ Building Energy Consumption Predictor")
st.markdown("---")

st.markdown("""
### Smart Energy Prediction for Buildings

This application predicts **building energy consumption (kWh)** using a trained **Random Forest machine learning model**.

Users can enter environmental and building parameters to instantly estimate energy usage.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model Type", "Random Forest")

with col2:
    st.metric("Prediction Output", "Energy (kWh)")

with col3:
    st.metric("Status", "Ready")

st.markdown("---")

st.subheader("Application Features")

st.markdown("""
**Interactive Prediction**

Users can adjust temperature, occupancy, HVAC usage, and other parameters to estimate energy consumption.

**Visual Energy Gauge**

Predictions are displayed using a gauge that categorizes consumption into **Green, Orange, and Red zones**.

**Machine Learning Powered**

The model learns complex relationships between environmental and operational variables affecting energy usage.
""")

st.markdown("---")

st.subheader("Key Factors Affecting Energy")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
**Environmental Factors**
- Temperature
- Humidity
- Seasonal patterns
""")

with col2:
    st.markdown("""
**Building Factors**
- Square Footage
- Occupancy
- HVAC Usage
- Lighting Usage
- Renewable Energy
""")

st.info("Use the **Prediction** page from the sidebar to estimate building energy consumption.")