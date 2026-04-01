import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# ── Load model ─────────────────────────────────────────────
model        = joblib.load('energy_model_rf.joblib')
feature_cols = joblib.load('feature_columns.joblib')

st.set_page_config(page_title="Energy Predictor", page_icon="⚡", layout="wide")
st.title("⚡ Building Energy Consumption Predictor")
st.caption("Adjust inputs → see predicted energy & gauge")

# ── Inputs ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    temp      = st.number_input("Temperature (°C)", value=25.0)
    humidity  = st.number_input("Humidity (%)", value=45.0)
    renewable = st.number_input("Renewable Energy (kWh)", value=10.0)
    sq_ft     = st.number_input("Square Footage", value=1500.0)
    occupancy = st.number_input("Occupancy", value=5)
    holiday   = st.selectbox("Holiday", ["No", "Yes"])

with col2:
    hvac    = st.selectbox("HVAC Status", ["Off", "On"])
    lights  = st.selectbox("Lighting Status", ["Off", "On"])
    day     = st.selectbox("Day of Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    hour    = st.slider("Hour of Day", 0, 23, 12)
    month   = st.slider("Month", 1, 12, 6)
    day_num = st.slider("Day of Month", 1, 31, 15)

# ── Feature Engineering ───────────────────────────────────
hvac_on    = 1 if hvac == "On" else 0
lights_on  = 1 if lights == "On" else 0
holiday_on = 1 if holiday == "Yes" else 0

hour_sin  = np.sin(2 * np.pi * hour / 24)
hour_cos  = np.cos(2 * np.pi * hour / 24)
month_sin = np.sin(2 * np.pi * month / 12)
month_cos = np.cos(2 * np.pi * month / 12)
day_sin   = np.sin(2 * np.pi * day_num / 31)
day_cos   = np.cos(2 * np.pi * day_num / 31)

hvac_occupancy     = hvac_on * occupancy
hvac_sqft          = hvac_on * sq_ft
temp_occupancy     = temp * occupancy
renewable_per_sqft = renewable / sq_ft
temp_squared       = temp ** 2
occupancy_squared  = occupancy ** 2

day_monday    = 1 if day == "Monday" else 0
day_saturday  = 1 if day == "Saturday" else 0
day_sunday    = 1 if day == "Sunday" else 0
day_thursday  = 1 if day == "Thursday" else 0
day_tuesday   = 1 if day == "Tuesday" else 0
day_wednesday = 1 if day == "Wednesday" else 0

input_data = pd.DataFrame([{
    'Temperature': temp, 'Humidity': humidity, 'SquareFootage': sq_ft,
    'Occupancy': occupancy, 'HVACUsage': hvac_on, 'LightingUsage': lights_on,
    'RenewableEnergy': renewable, 'Holiday': holiday_on, 'hour_sin': hour_sin,
    'hour_cos': hour_cos, 'month_sin': month_sin, 'month_cos': month_cos,
    'day_sin': day_sin, 'day_cos': day_cos, 'HVAC_Occupancy': hvac_occupancy,
    'HVAC_SqFt': hvac_sqft, 'Temp_Occupancy': temp_occupancy,
    'Renewable_per_SqFt': renewable_per_sqft, 'Temp_squared': temp_squared,
    'Occupancy_squared': occupancy_squared, 'DayOfWeek_Monday': day_monday,
    'DayOfWeek_Saturday': day_saturday, 'DayOfWeek_Sunday': day_sunday,
    'DayOfWeek_Thursday': day_thursday, 'DayOfWeek_Tuesday': day_tuesday,
    'DayOfWeek_Wednesday': day_wednesday,
}])

input_data = input_data[feature_cols]

# ── Gauge Helpers ─────────────────────────────────────────
def category_color(val):
    if val <= 70:
        return "green"
    elif val <= 85:
        return "orange"
    else:
        return "red"

def bar_color(val):
    if val <= 70:
        return "#66bb6a"   # light green
    elif val <= 85:
        return "#ffb74d"   # light orange
    else:
        return "#ef5350"   # light red

def build_gauge(value):

    gauge_max = 100
    display_val = min(value, gauge_max)

    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=display_val,
            number={
                'suffix': " kWh",
                'font': {
                    'size': 38,
                    'color': category_color(value)
                }
            },
            title={
                'text': "<b>Energy Usage (kWh)</b>",
                'font': {'size': 18, 'color': "white"}
            },
            gauge={
                'axis': {
                    'range': [0, gauge_max],
                    'tickvals': list(range(0, 101, 10)),
                    'tickfont': {'color': "white", 'size': 12}
                },
                'bar': {
                    'color': bar_color(value),
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.28
                },
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 70],  'color': "#1b5e20"},  # dark green
                    {'range': [70, 85], 'color': "#e65100"},  # dark orange
                    {'range': [85, 100],'color': "#b71c1c"}   # dark red
                ]
            }
        ),
        layout=go.Layout(
            height=360,
            margin=dict(t=60, b=20, l=40, r=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
    )

# ── Predict ───────────────────────────────────────────────
predict = st.button("⚡ Predict Energy")

if predict:
    with st.spinner("Calculating energy..."):
        prediction = model.predict(input_data)[0]

    st.plotly_chart(
        build_gauge(prediction),
        config={"displayModeBar": False},
        use_container_width=True
    )