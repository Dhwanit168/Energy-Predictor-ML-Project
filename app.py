import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import plotly.graph_objects as go

# ── Load model ─────────────────────────────────────────────
model        = joblib.load('energy_model_rf.joblib')
feature_cols = joblib.load('feature_columns.joblib')

st.set_page_config(page_title="Energy Predictor", page_icon="⚡", layout="wide")

# ── Title ────────────────────────────────────────────────
st.title("⚡ Building Energy Consumption Predictor")
st.caption("Adjust inputs → see predicted energy, gauge, & effect of temperature")

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
    'Temperature': temp,
    'Humidity': humidity,
    'SquareFootage': sq_ft,
    'Occupancy': occupancy,
    'HVACUsage': hvac_on,
    'LightingUsage': lights_on,
    'RenewableEnergy': renewable,
    'Holiday': holiday_on,
    'hour_sin': hour_sin,
    'hour_cos': hour_cos,
    'month_sin': month_sin,
    'month_cos': month_cos,
    'day_sin': day_sin,
    'day_cos': day_cos,
    'HVAC_Occupancy': hvac_occupancy,
    'HVAC_SqFt': hvac_sqft,
    'Temp_Occupancy': temp_occupancy,
    'Renewable_per_SqFt': renewable_per_sqft,
    'Temp_squared': temp_squared,
    'Occupancy_squared': occupancy_squared,
    'DayOfWeek_Monday': day_monday,
    'DayOfWeek_Saturday': day_saturday,
    'DayOfWeek_Sunday': day_sunday,
    'DayOfWeek_Thursday': day_thursday,
    'DayOfWeek_Tuesday': day_tuesday,
    'DayOfWeek_Wednesday': day_wednesday,
}])
input_data = input_data[feature_cols]

# ── Helpers ────────────────────────────────────────────────
def bar_color(val):
    if val >= 90:   return "#c0392b"
    elif val >= 80: return "#e67e22"
    elif val >= 70: return "#f1c40f"
    else:           return "#2471a3"

def build_gauge(current_val, target_val):
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=current_val,
            number={
                'suffix': " kWh",
                'font': {'size': 36, 'color': bar_color(current_val)}
            },
            title={'text': "Energy Usage (kWh)", 'font': {'size': 16, 'color': "#555"}},
            gauge={
                'axis': {
                    'range': [0, 120],
                    'tickwidth': 1,
                    'tickcolor': "#aaa",
                    'tickvals': [0, 20, 40, 60, 70, 80, 90, 100, 120],
                    'tickfont': {'size': 11}
                },
                'bar': {'color': bar_color(current_val), 'thickness': 0.28},
                'bgcolor': "white",
                'borderwidth': 1,
                'bordercolor': "#ddd",
                'steps': [
                    {'range': [0,  70],  'color': "#d5f5e3"},
                    {'range': [70, 80],  'color': "#fef9e7"},
                    {'range': [80, 90],  'color': "#fdebd0"},
                    {'range': [90, 120], 'color': "#fadbd8"},
                ],
                'threshold': {
                    'line': {'color': bar_color(target_val), 'width': 3},
                    'thickness': 0.75,
                    'value': target_val
                }
            }
        ),
        layout=go.Layout(
            height=360,
            margin=dict(t=60, b=20, l=40, r=40),
            paper_bgcolor="white",
        )
    )

# ── Predict Button ─────────────────────────────────────────
predict = st.button("⚡ Predict Energy")

if predict:
    with st.spinner("Calculating energy..."):
        time.sleep(0.4)
        prediction = model.predict(input_data)[0]

    # ── Prediction badge ───────────────────────────────────
    st.markdown("## ⚡ Predicted Energy")
    # st.metric("Energy Consumption (kWh)", f"{prediction:.2f}")

    # if prediction > 90:
    #     st.error(f"🔴 Very High energy demand: {prediction:.2f} kWh — Consider reducing HVAC or occupancy.")
    # elif prediction > 80:
    #     st.warning(f"🟡 High energy demand: {prediction:.2f} kWh — Monitor usage closely.")
    # elif prediction > 70:
    #     st.success(f"🟢 Normal energy demand: {prediction:.2f} kWh — Within expected range.")
    # else:
    #     st.info(f"🔵 Low energy demand: {prediction:.2f} kWh — Efficient usage.")

    # # ── Smooth Animated Gauge ──────────────────────────────
    # st.markdown("## 🏁 Energy Gauge")

    gauge_slot = st.empty()

    # Cubic ease-in-out
    n_frames = 28
    t_vals   = np.linspace(0, 1, n_frames)
    eased    = np.where(
        t_vals < 0.5,
        4 * t_vals ** 3,
        1 - (-2 * t_vals + 2) ** 3 / 2
    )
    frame_values = eased * prediction

    for i, v in enumerate(frame_values):
        with gauge_slot:
            st.plotly_chart(
                build_gauge(round(v, 1), prediction),
                use_container_width=True,
                config={"displayModeBar": False},
                key=f"gauge_frame_{i}"   # ← unique key per frame
            )
        time.sleep(0.035)

    # Final frame locked on exact prediction value
    with gauge_slot:
        st.plotly_chart(
            build_gauge(round(prediction, 2), prediction),
            use_container_width=True,
            config={"displayModeBar": False},
            key="gauge_final"            # ← unique key for final frame
        )

    # ── Temperature vs Energy Line Chart ──────────────────
    st.markdown("## 📈 Temperature vs Predicted Energy (What-if Simulation)")

    temps = list(range(-10, 51))
    energy_preds = []

    for t in temps:
        temp_row = input_data.copy()
        temp_row['Temperature']    = t
        temp_row['Temp_Occupancy'] = t * occupancy
        temp_row['Temp_squared']   = t ** 2
        energy_preds.append(model.predict(temp_row)[0])

    y_min = max(0, min(energy_preds) - 5)
    y_max = max(energy_preds) + 10

    fig_line = go.Figure()

    fig_line.add_shape(type="rect", x0=-10, x1=51, y0=0,  y1=70,    fillcolor="lightblue", opacity=0.2, line_width=0)
    fig_line.add_shape(type="rect", x0=-10, x1=51, y0=70, y1=80,    fillcolor="green",     opacity=0.2, line_width=0)
    fig_line.add_shape(type="rect", x0=-10, x1=51, y0=80, y1=90,    fillcolor="yellow",    opacity=0.2, line_width=0)
    fig_line.add_shape(type="rect", x0=-10, x1=51, y0=90, y1=y_max, fillcolor="red",       opacity=0.2, line_width=0)

    fig_line.add_trace(go.Scatter(
        x=temps,
        y=energy_preds,
        mode='lines+markers',
        name='Predicted Energy',
        line=dict(color='blue', width=3, shape='spline'),
        marker=dict(size=6),
        hovertemplate='Temp: %{x}°C<br>Energy: %{y:.2f} kWh'
    ))

    fig_line.add_trace(go.Scatter(
        x=[temp],
        y=[prediction],
        mode='markers+text',
        name='Current Temp',
        marker=dict(color='black', size=14),
        text=[f"{prediction:.1f} kWh"],
        textposition="top center",
        hoverinfo="skip"
    ))

    fig_line.update_layout(
        xaxis_title="Temperature (°C)",
        yaxis_title="Predicted Energy (kWh)",
        yaxis=dict(range=[y_min, y_max]),
        height=450,
        hovermode="x unified",
        margin=dict(r=150),
        legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgrey",
            borderwidth=1
        )
    )

    st.plotly_chart(fig_line, use_container_width=True, key="line_chart")