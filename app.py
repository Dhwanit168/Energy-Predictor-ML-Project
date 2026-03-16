import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and feature columns
model        = joblib.load('energy_model_rf.joblib')
feature_cols = joblib.load('feature_columns.joblib')

st.set_page_config(page_title="Energy Predictor", page_icon="⚡", layout="wide")

st.markdown("<h1 style='text-align:center;'>⚡ Building Energy Consumption Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; margin-bottom:40px;'>Enter building details to predict hourly energy usage.</p>", unsafe_allow_html=True)

# ── Inputs (2 columns) ────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    temp      = st.number_input("Temperature (°C)",       min_value=20.0, max_value=30.0, value=25.0, step=0.1)
    humidity  = st.number_input("Humidity (%)",            min_value=30.0, max_value=60.0, value=45.0, step=0.1)
    renewable = st.number_input("Renewable Energy (kWh)",  min_value=0.0,  max_value=30.0, value=10.0, step=0.1)
    sq_ft     = st.number_input("Square Footage",          min_value=1000.0, max_value=2000.0, value=1500.0, step=10.0)
    occupancy = st.number_input("Occupancy (People)",      min_value=0, max_value=9, value=5, step=1)
    holiday   = st.selectbox("Holiday", ["No", "Yes"])

with col2:
    hvac    = st.selectbox("HVAC Status",     ["Off", "On"])
    lights  = st.selectbox("Lighting Status", ["Off", "On"])
    day     = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    hour    = st.slider("Hour of Day",   0, 23, 12)
    month   = st.slider("Month",         1, 12,  6)
    day_num = st.slider("Day of Month",  1, 31, 15)

# ── Feature Engineering ───────────────────────────────────────────────────────
hvac_on    = 1 if hvac    == "On"  else 0
lights_on  = 1 if lights  == "On"  else 0
holiday_on = 1 if holiday == "Yes" else 0

hour_sin  = np.sin(2 * np.pi * hour    / 24)
hour_cos  = np.cos(2 * np.pi * hour    / 24)
month_sin = np.sin(2 * np.pi * month   / 12)
month_cos = np.cos(2 * np.pi * month   / 12)
day_sin   = np.sin(2 * np.pi * day_num / 31)
day_cos   = np.cos(2 * np.pi * day_num / 31)

hvac_occupancy     = hvac_on * occupancy
hvac_sqft          = hvac_on * sq_ft
temp_occupancy     = temp * occupancy
renewable_per_sqft = renewable / sq_ft
temp_squared       = temp ** 2
occupancy_squared  = occupancy ** 2

day_monday    = 1 if day == "Monday"    else 0
day_saturday  = 1 if day == "Saturday"  else 0
day_sunday    = 1 if day == "Sunday"    else 0
day_thursday  = 1 if day == "Thursday"  else 0
day_tuesday   = 1 if day == "Tuesday"   else 0
day_wednesday = 1 if day == "Wednesday" else 0

# ── Build Input DataFrame ─────────────────────────────────────────────────────
input_data = pd.DataFrame([{
    'Temperature'        : temp,
    'Humidity'           : humidity,
    'SquareFootage'      : sq_ft,
    'Occupancy'          : occupancy,
    'HVACUsage'          : hvac_on,
    'LightingUsage'      : lights_on,
    'RenewableEnergy'    : renewable,
    'Holiday'            : holiday_on,
    'hour_sin'           : hour_sin,
    'hour_cos'           : hour_cos,
    'month_sin'          : month_sin,
    'month_cos'          : month_cos,
    'day_sin'            : day_sin,
    'day_cos'            : day_cos,
    'HVAC_Occupancy'     : hvac_occupancy,
    'HVAC_SqFt'          : hvac_sqft,
    'Temp_Occupancy'     : temp_occupancy,
    'Renewable_per_SqFt' : renewable_per_sqft,
    'Temp_squared'       : temp_squared,
    'Occupancy_squared'  : occupancy_squared,
    'DayOfWeek_Monday'   : day_monday,
    'DayOfWeek_Saturday' : day_saturday,
    'DayOfWeek_Sunday'   : day_sunday,
    'DayOfWeek_Thursday' : day_thursday,
    'DayOfWeek_Tuesday'  : day_tuesday,
    'DayOfWeek_Wednesday': day_wednesday,
}])

input_data = input_data[feature_cols]

# ── Predict Button (small — centered) ────────────────────────────────────────
st.markdown("---")

_, btn_col, _ = st.columns([3, 1, 3])
with btn_col:
    predict = st.button("⚡ Predict", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────────────
if predict:
    prediction = model.predict(input_data)[0]

    st.markdown("### 📊 Prediction Result")
    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.metric("Predicted Energy (kWh)", f"{prediction:.2f}")
    with res_col2:
        st.metric("MAE (model error)", "± 4.01 kWh")
    with res_col3:
        st.metric("Model R² Score", "0.6269")

    st.markdown("### 🔔 Status")
    if prediction > 90:
        st.error(f"🔴 Very High energy demand: {prediction:.2f} kWh — Consider reducing HVAC or occupancy.")
    elif prediction > 80:
        st.warning(f"🟡 High energy demand: {prediction:.2f} kWh — Monitor usage closely.")
    elif prediction > 70:
        st.success(f"🟢 Normal energy demand: {prediction:.2f} kWh — Within expected range.")
    else:
        st.info(f"🔵 Low energy demand: {prediction:.2f} kWh — Efficient usage.")