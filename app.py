import streamlit as st
import math

# Page setup
st.set_page_config(page_title="Wire Sizing Helper", page_icon="⚡", layout="centered")

# Custom CSS for colorful civil-engineering themed background
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #004d40, #00796b, #26a69a, #80cbc4);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .main-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #ffeb3b;
        text-shadow: 2px 2px 4px #000000;
    }
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #ffffff;
    }
    .footer {
        font-size: 16px;
        text-align: center;
        color: #ffccbc;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">👷 Welcome to Ateeq Problem Solving</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pipe Sizing Helper ⚡</div>', unsafe_allow_html=True)

# Inputs
current = st.number_input("Enter Current (Amps)", min_value=0.0, step=0.1)
voltage = st.number_input("Enter Voltage (Volts)", min_value=0.0, step=0.1)
resistance = st.number_input("Enter Resistance (Ohms)", min_value=0.0, step=0.01)

# Ohm’s Law Calculations
power = current * voltage
calculated_voltage = current * resistance if resistance > 0 else None

# Wire sizing logic (simplified)
# Assume copper wire, safe current density ~5 A/mm²
if current > 0:
    area_mm2 = current / 5
    diameter_mm = math.sqrt((4 * area_mm2) / math.pi)
else:
    diameter_mm = None

# Results
if st.button("Calculate Wire Size"):
    st.write(f"🔌 Power through wire: **{power:.2f} W**")
    if calculated_voltage:
        st.write(f"⚡ Voltage drop across resistance: **{calculated_voltage:.2f} V**")
    if diameter_mm:
        st.success(f"Recommended Wire Diameter: **{diameter_mm:.2f} mm**")
    else:
        st.warning("Please enter valid current values.")

    st.markdown('<div class="footer">✨ Be with us for your Queries 😊🔧📐</div>', unsafe_allow_html=True)
