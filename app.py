import streamlit as st
import math

st.set_page_config(
    page_title="Ateeq Wire Sizing Helper",
    page_icon="⚡",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap');

.stApp {
    background-color: #1a1a2e;
    background-image:
        linear-gradient(rgba(255,165,0,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,165,0,0.06) 1px, transparent 1px),
        linear-gradient(rgba(255,165,0,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,165,0,0.03) 1px, transparent 1px);
    background-size: 80px 80px, 80px 80px, 20px 20px, 20px 20px;
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top:1.5rem !important; padding-bottom:2rem !important; max-width:780px; }
* { font-family:'Libre Baskerville','Times New Roman',Georgia,serif !important; }

@keyframes scanLine {
    0%   { transform:translateY(-100%); opacity:0.3; }
    100% { transform:translateY(100vh); opacity:0; }
}
.scan-line {
    position:fixed; top:0; left:0; width:100%; height:2px;
    background:linear-gradient(90deg,transparent,rgba(255,165,0,0.4),transparent);
    animation:scanLine 6s linear infinite;
    pointer-events:none; z-index:0;
}
@keyframes shimmer { from{background-position:0% center;} to{background-position:200% center;} }
@keyframes fadeSlideUp { from{opacity:0;transform:translateY(16px);} to{opacity:1;transform:translateY(0);} }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.6;} }

/* Welcome */
.welcome-wrap {
    text-align:center;
    background:linear-gradient(160deg,#0d0d1e 0%,#1a1a3e 60%,#0d0d1e 100%);
    border:1px solid rgba(255,165,0,0.4);
    border-top:4px solid #ffa500;
    border-radius:8px; padding:2rem 1.5rem 1.5rem;
    margin-bottom:1.2rem;
    box-shadow:0 4px 24px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,165,0,0.15);
    position:relative; z-index:1;
}
.welcome-eyebrow {
    font-family:'Courier Prime',monospace !important;
    font-size:0.7rem; font-weight:700;
    letter-spacing:0.3em; text-transform:uppercase;
    color:#ffa500; margin-bottom:0.5rem;
}
.welcome-title {
    font-family:'Playfair Display',serif !important;
    font-size:clamp(1.6rem,4.5vw,2.8rem); font-weight:900; line-height:1.15;
    background:linear-gradient(90deg,#ffe0a0 0%,#ffa500 50%,#ffe0a0 100%);
    background-size:200% auto;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    animation:shimmer 3s linear infinite; margin:0 0 0.3rem;
}
.welcome-divider {
    display:flex; align-items:center; gap:10px;
    margin:0.7rem auto 0.6rem; max-width:300px;
}
.welcome-divider span { flex:1; height:1px; background:linear-gradient(90deg,transparent,#ffa500,transparent); }
.welcome-divider em   { font-style:normal; font-size:1rem; }
.wire-title {
    font-family:'Courier Prime',monospace !important;
    font-size:clamp(0.95rem,2.5vw,1.3rem); font-weight:700; color:#ffcc44;
    letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.3rem;
}
.welcome-sub {
    font-family:'Libre Baskerville',serif !important;
    font-size:0.78rem; font-style:italic; color:#aa8840; letter-spacing:0.05em;
}

/* Section heading */
.sec-head {
    font-family:'Courier Prime',monospace !important;
    font-size:0.68rem; font-weight:700;
    letter-spacing:0.25em; text-transform:uppercase;
    color:#ffa500; border-bottom:1px solid rgba(255,165,0,0.3);
    padding-bottom:0.3rem; margin:1.2rem 0 0.7rem;
}

/* Input card */
.input-card {
    background:rgba(10,10,30,0.85);
    border:1px solid rgba(255,165,0,0.25);
    border-radius:6px; padding:1.4rem 1.6rem;
    box-shadow:0 2px 16px rgba(0,0,0,0.5);
    margin-bottom:1rem; position:relative; z-index:1;
}

/* Info box */
.info-box {
    background:rgba(255,165,0,0.08);
    border-left:3px solid #ffa500;
    border-radius:3px; padding:0.6rem 0.9rem;
    font-family:'Libre Baskerville',serif !important;
    font-size:0.75rem; font-style:italic; color:#cc8800; margin:0.5rem 0;
}

/* Streamlit overrides */
label, .stSelectbox label, .stNumberInput label {
    font-family:'Libre Baskerville',serif !important;
    font-size:0.8rem !important; font-weight:700 !important;
    color:#e8d0a0 !important; letter-spacing:0.06em !important;
}
input[type="number"] {
    background:rgba(0,0,0,0.6) !important;
    border:1px solid rgba(255,165,0,0.4) !important;
    border-radius:4px !important; color:#fff8e0 !important;
    font-family:'Courier Prime',monospace !important;
    font-size:1rem !important; font-weight:700 !important;
}
input[type="number"]:focus {
    border-color:#ffa500 !important;
    box-shadow:0 0 0 2px rgba(255,165,0,0.2) !important;
}
.stSelectbox > div > div {
    background:rgba(0,0,0,0.6) !important;
    border:1px solid rgba(255,165,0,0.35) !important;
    border-radius:4px !important; color:#e8d0a0 !important;
}
.stButton > button {
    background:linear-gradient(135deg,#4a2a00,#8a5200) !important;
    border:1px solid #ffa500 !important;
    border-radius:5px !important; color:#ffe0a0 !important;
    font-family:'Courier Prime',monospace !important;
    font-weight:700 !important; font-size:0.9rem !important;
    letter-spacing:0.15em !important; text-transform:uppercase !important;
    padding:0.6rem 2rem !important; width:100% !important;
    transition:all .2s !important;
    box-shadow:0 4px 12px rgba(255,165,0,0.25) !important;
}
.stButton > button:hover {
    background:linear-gradient(135deg,#6a3a00,#aa6200) !important;
    box-shadow:0 6px 18px rgba(255,165,0,0.4) !important;
    transform:translateY(-1px) !important;
}

/* Result */
.result-panel {
    background:linear-gradient(160deg,#0a0a20,#0d0d30);
    border:1px solid rgba(255,165,0,0.4);
    border-top:3px solid #ffa500;
    border-radius:6px; padding:1.5rem 1.6rem;
    margin-top:1rem; position:relative; z-index:1;
    box-shadow:0 4px 24px rgba(0,0,0,0.6);
    animation:fadeSlideUp 0.5s ease both;
}
.result-label {
    font-family:'Courier Prime',monospace !important;
    font-size:0.65rem; font-weight:700;
    letter-spacing:0.25em; text-transform:uppercase;
    color:#ffa500; margin-bottom:0.4rem;
}
.result-value {
    font-family:'Playfair Display',serif !important;
    font-size:clamp(1.8rem,4.5vw,3rem); font-weight:900;
    color:#ffcc44; line-height:1.1;
}
.result-unit {
    font-family:'Courier Prime',monospace !important;
    font-size:0.9rem; color:#aa8840; margin-left:0.4rem;
}
.result-sub {
    font-family:'Libre Baskerville',serif !important;
    font-size:0.78rem; font-style:italic; color:#7a6030; margin-top:0.3rem;
}
.result-row {
    display:flex; gap:0.8rem; flex-wrap:wrap; margin-top:1.1rem;
}
.result-box {
    background:rgba(255,165,0,0.08);
    border:1px solid rgba(255,165,0,0.2);
    border-radius:4px; padding:0.6rem 0.9rem;
    flex:1; min-width:110px; text-align:center;
}
.result-box-val {
    font-family:'Courier Prime',monospace !important;
    font-size:1rem; font-weight:700; color:#ffe0a0;
}
.result-box-lbl {
    font-family:'Libre Baskerville',serif !important;
    font-size:0.58rem; text-transform:uppercase;
    letter-spacing:0.1em; color:#7a6030; margin-top:0.1rem;
}

/* Appliance table */
.app-table {
    background:rgba(10,10,30,0.85);
    border:1px solid rgba(255,165,0,0.25);
    border-radius:6px; overflow:hidden;
    margin-top:1rem; animation:fadeSlideUp 0.5s ease both;
}
.app-table-header {
    background:rgba(255,165,0,0.15);
    display:grid; grid-template-columns:2fr 1.2fr 1.2fr 1.5fr 2fr;
    padding:0.5rem 0.8rem;
    font-family:'Courier Prime',monospace !important;
    font-size:0.6rem; font-weight:700;
    letter-spacing:0.15em; text-transform:uppercase; color:#ffa500;
    border-bottom:1px solid rgba(255,165,0,0.2);
}
.app-table-row {
    display:grid; grid-template-columns:2fr 1.2fr 1.2fr 1.5fr 2fr;
    padding:0.55rem 0.8rem;
    border-bottom:1px solid rgba(255,165,0,0.08);
    font-family:'Libre Baskerville',serif !important;
    font-size:0.72rem; color:#c8b880;
    align-items:center;
}
.app-table-row:last-child { border-bottom:none; }
.app-table-row:hover { background:rgba(255,165,0,0.05); }
.badge {
    display:inline-block; border-radius:3px;
    padding:0.15rem 0.45rem; font-size:0.6rem;
    font-family:'Courier Prime',monospace !important;
    font-weight:700; letter-spacing:0.1em;
}
.badge-green  { background:rgba(0,200,100,0.15); color:#00c864; border:1px solid rgba(0,200,100,0.3); }
.badge-yellow { background:rgba(255,200,0,0.15); color:#ffc800; border:1px solid rgba(255,200,0,0.3); }
.badge-red    { background:rgba(255,80,80,0.15);  color:#ff5050; border:1px solid rgba(255,80,80,0.3); }
.badge-blue   { background:rgba(80,150,255,0.15); color:#5096ff; border:1px solid rgba(80,150,255,0.3); }

/* Home guide */
.home-guide {
    background:rgba(10,10,30,0.85);
    border:1px solid rgba(255,165,0,0.25);
    border-left:4px solid #ffa500;
    border-radius:6px; padding:1.2rem 1.4rem;
    margin-top:1rem; animation:fadeSlideUp 0.6s ease both;
}
.home-guide-title {
    font-family:'Courier Prime',monospace !important;
    font-size:0.68rem; font-weight:700;
    letter-spacing:0.2em; text-transform:uppercase;
    color:#ffa500; margin-bottom:0.7rem;
}
.home-guide-item {
    display:flex; align-items:flex-start; gap:0.7rem;
    padding:0.45rem 0; border-bottom:1px solid rgba(255,165,0,0.07);
    font-family:'Libre Baskerville',serif !important; font-size:0.75rem;
}
.home-guide-item:last-child { border-bottom:none; }
.home-guide-icon { font-size:1.1rem; min-width:1.5rem; text-align:center; }
.home-guide-name { color:#e8d0a0; font-weight:700; min-width:140px; }
.home-guide-wire { color:#ffcc44; font-family:'Courier Prime',monospace !important; font-weight:700; }
.home-guide-note { color:#7a6848; font-style:italic; font-size:0.68rem; }

/* Be with us */
.be-with-us {
    background:rgba(10,10,30,0.9);
    border:1px solid rgba(255,165,0,0.3);
    border-radius:6px; padding:1rem 1.2rem;
    text-align:center; margin-top:1.2rem;
    animation:fadeSlideUp 0.7s ease 0.2s both;
}
.be-with-us-text {
    font-family:'Playfair Display',serif !important;
    font-size:1.05rem; font-weight:700; color:#e8d0a0; letter-spacing:0.05em;
}
.be-with-us-emojis { font-size:1.1rem; letter-spacing:0.3rem; margin-top:0.3rem; }

/* Footer */
.app-footer {
    text-align:center;
    font-family:'Libre Baskerville',serif !important;
    font-size:0.65rem; font-style:italic; color:#4a3820; margin-top:2rem;
    border-top:1px solid rgba(255,165,0,0.12); padding-top:0.8rem;
}
</style>
<div class="scan-line"></div>
""", unsafe_allow_html=True)

# ── Welcome ───────────────────────────────────────────────────
st.markdown("""
<div class="welcome-wrap">
    <div class="welcome-eyebrow">✦ Electrical Engineering Tool ✦</div>
    <div class="welcome-title">Welcome to Ateeq Problem Solving</div>
    <div class="welcome-divider"><span></span><em>⚡</em><span></span></div>
    <div class="wire-title">⚡ Wire Sizing Helper ⚡</div>
    <div class="welcome-sub">Calculate recommended wire / cable core size from current & voltage — with home appliance guide</div>
</div>
""", unsafe_allow_html=True)

# ── Wire data ─────────────────────────────────────────────────
WIRE_TABLE = [
    # (max_amp, size_mm2, cores, label, type)
    (6,    0.5,  "1.0 mm²", "Single Core",  "Thin bell/signal wire"),
    (10,   1.0,  "1.5 mm²", "Single Core",  "Lighting circuits"),
    (16,   1.5,  "2.5 mm²", "Twin+Earth",   "Standard power sockets"),
    (20,   2.5,  "4.0 mm²", "Twin+Earth",   "High-load sockets / cookers"),
    (27,   4.0,  "6.0 mm²", "Twin+Earth",   "Showers / large appliances"),
    (34,   6.0,  "10 mm²",  "3-Core+Earth", "Sub-mains / large AC"),
    (46,   10.0, "16 mm²",  "3-Core+Earth", "Distribution boards"),
    (61,   16.0, "25 mm²",  "3-Core+Earth", "Industrial / main supply"),
    (80,   25.0, "35 mm²",  "Multi-Core",   "Heavy industrial"),
    (100,  35.0, "50 mm²",  "Multi-Core",   "Very heavy industrial"),
]

HOME_APPLIANCES = [
    # (emoji, name, watts, amps_230v, wire_mm2, core_type, note)
    ("💡", "Lighting (LED/CFL)",         60,   0.26,  "1.5 mm²", "Twin+Earth",   "Per room circuit"),
    ("💡", "Lighting (Tube/Halogen)",    200,   0.87,  "1.5 mm²", "Twin+Earth",   "Per room circuit"),
    ("🌀", "Ceiling Fan",                100,   0.43,  "1.5 mm²", "Twin+Earth",   "Standard speed"),
    ("👕", "Iron / Clothes Press",      2200,   9.57,  "2.5 mm²", "Twin+Earth",   "Dedicated socket"),
    ("🧺", "Washing Machine",           2500,  10.87,  "2.5 mm²", "Twin+Earth",   "Dedicated circuit"),
    ("💧", "Water Pump (0.5 HP)",        373,   1.62,  "1.5 mm²", "Twin+Earth",   "Single phase"),
    ("💧", "Water Pump (1 HP)",          746,   3.24,  "2.5 mm²", "Twin+Earth",   "Single phase"),
    ("🌡️", "Refrigerator",              200,   0.87,  "1.5 mm²", "Twin+Earth",   "Dedicated socket"),
    ("❄️", "Air Conditioner (1 Ton)",   1500,   6.52,  "2.5 mm²", "Twin+Earth",   "Dedicated breaker"),
    ("❄️", "Air Conditioner (1.5 Ton)", 1800,   7.83,  "2.5 mm²", "Twin+Earth",   "Dedicated breaker"),
    ("❄️", "Air Conditioner (2 Ton)",   2300,  10.00,  "4.0 mm²", "Twin+Earth",   "Dedicated breaker"),
    ("🖥️", "Desktop Computer",           300,   1.30,  "1.5 mm²", "Twin+Earth",   "Normal socket"),
    ("💻", "Laptop Charging",            65,   0.28,  "1.5 mm²", "Twin+Earth",   "Normal socket"),
    ("📱", "Mobile Charging",             20,   0.09,  "1.5 mm²", "Twin+Earth",   "Normal socket"),
    ("📺", "LED Television",             100,   0.43,  "1.5 mm²", "Twin+Earth",   "Normal socket"),
    ("🍳", "Electric Kettle",           2000,   8.70,  "2.5 mm²", "Twin+Earth",   "Dedicated socket"),
    ("🔌", "General Power Sockets",      —— ,     ——,  "2.5 mm²", "Twin+Earth",   "Standard ring main"),
]

def get_wire_size(current_a):
    for max_a, _, size, cores, desc in WIRE_TABLE:
        if current_a <= max_a:
            return size, cores, desc
    return "50 mm²+", "Multi-Core", "Consult electrical engineer"

def amps_from_watts(watts, voltage, pf=0.85):
    return watts / (voltage * pf)

STANDARD_SIZES = [1.0,1.5,2.5,4.0,6.0,10.0,16.0,25.0,35.0,50.0]

def nearest_standard_wire(mm2):
    above = [s for s in STANDARD_SIZES if s >= mm2]
    return min(above) if above else STANDARD_SIZES[-1]

# ── Mode selector ─────────────────────────────────────────────
st.markdown('<div class="sec-head">Select Calculation Mode</div>', unsafe_allow_html=True)
mode = st.selectbox("",
    ["⚡  Calculate by Current & Voltage",
     "🏠  Home Appliance Wire Guide"],
    label_visibility="collapsed")

# ════════════════════════════════════════════════════════════
# MODE 1 — Calculate by current & voltage
# ════════════════════════════════════════════════════════════
if "Current" in mode:
    st.markdown('<div class="sec-head">Input Parameters</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        input_mode = st.selectbox("Input Method",
            ["Current (Amperes) — Direct",
             "Power (Watts) + Voltage"])
    with col2:
        voltage = st.number_input("System Voltage (V)",
            min_value=110.0, max_value=11000.0, value=230.0, step=10.0)

    if "Power" in input_mode:
        col3, col4 = st.columns(2)
        with col3:
            power_w = st.number_input("Power Load (Watts)",
                min_value=1.0, max_value=100000.0, value=1000.0, step=10.0)
        with col4:
            pf = st.number_input("Power Factor (0.5–1.0)",
                min_value=0.5, max_value=1.0, value=0.85, step=0.05)
        current = power_w / (voltage * pf)
    else:
        col3, col4 = st.columns(2)
        with col3:
            current = st.number_input("Current (Amperes)",
                min_value=0.1, max_value=500.0, value=10.0, step=0.5)
        with col4:
            safety = st.number_input("Safety Factor (%)",
                min_value=10.0, max_value=50.0, value=25.0, step=5.0,
                help="Add 20–30% safety margin on top of calculated current")

    if "Power" not in input_mode:
        design_current = current * (1 + safety/100)
    else:
        design_current = current * 1.25

    install_type = st.selectbox("Installation Method",
        ["Clipped to surface / Conduit",
         "In wall / Insulated (reduce capacity by 15%)",
         "Underground / Buried (increase capacity by 10%)"])

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        ⚡ &nbsp; Design current includes a 25% safety margin. Always use a dedicated circuit breaker.
        Wire ratings shown are for PVC-insulated copper conductors at 30°C ambient temperature.
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1,2,1])
    with col_b:
        calc_btn = st.button("⚡  Calculate Wire Size")

    if calc_btn:
        adj_current = design_current
        if "wall" in install_type.lower():   adj_current *= 1.15
        if "underground" in install_type.lower(): adj_current *= 0.90

        size_label, core_type, desc = get_wire_size(adj_current)
        cross_mm2 = float(size_label.replace(" mm²","").replace("+","")) if "+" not in size_label else 50.0
        diameter_mm = math.sqrt(4 * cross_mm2 / math.pi)
        resistance = 0.0175 / cross_mm2  # Ω/m copper

        st.markdown('<div class="sec-head">Calculation Results</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-panel">
            <div class="result-label">✦ Recommended Wire Size ✦</div>
            <div>
                <span class="result-value">{size_label}</span>
            </div>
            <div class="result-sub">Core Type: <b style="color:#ffcc44;">{core_type}</b> &nbsp;·&nbsp; {desc}</div>
            <div class="result-row">
                <div class="result-box">
                    <div class="result-box-val">{current:.2f} A</div>
                    <div class="result-box-lbl">Load Current</div>
                </div>
                <div class="result-box">
                    <div class="result-box-val">{adj_current:.2f} A</div>
                    <div class="result-box-lbl">Design Current</div>
                </div>
                <div class="result-box">
                    <div class="result-box-val">{diameter_mm:.2f} mm</div>
                    <div class="result-box-lbl">Wire Diameter</div>
                </div>
                <div class="result-box">
                    <div class="result-box-val">{resistance*1000:.3f} mΩ/m</div>
                    <div class="result-box-lbl">Resistance/m</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Warning
        if adj_current > 100:
            st.markdown('<div class="info-box">⚠ Very high current — consult a licensed electrical engineer before installation.</div>', unsafe_allow_html=True)
        if "wall" in install_type.lower():
            st.markdown('<div class="info-box">⚠ Wires inside walls require derating — consider next size up for safety.</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="be-with-us">
            <div class="be-with-us-text">Be with us for your Queries</div>
            <div class="be-with-us-emojis">⚡ 🔌 🏠 💡 🔧 🛠️ 📐 🔋</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# MODE 2 — Home appliance guide
# ════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="sec-head">Home Appliance Wire Guide — Pakistan / 230V System</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        🏠 &nbsp; This guide shows the recommended copper wire size for each home appliance
        based on the Pakistan 230V single-phase system. Always use a dedicated circuit breaker
        for high-load appliances.
    </div>
    """, unsafe_allow_html=True)

    # Table header
    st.markdown("""
    <div class="app-table">
        <div class="app-table-header">
            <div>Appliance</div>
            <div>Load (W)</div>
            <div>Current (A)</div>
            <div>Wire Size</div>
            <div>Cable Type</div>
        </div>
    """, unsafe_allow_html=True)

    APPLIANCES = [
        ("💡", "Lighting — LED/CFL",        60,   0.26,  "1.5 mm²", "Twin+Earth",   "green"),
        ("💡", "Lighting — Tube/Halogen",   200,   0.87,  "1.5 mm²", "Twin+Earth",   "green"),
        ("🌀", "Ceiling Fan",               100,   0.43,  "1.5 mm²", "Twin+Earth",   "green"),
        ("👕", "Iron / Clothes Press",     2200,   9.57,  "2.5 mm²", "Twin+Earth",   "yellow"),
        ("🧺", "Washing Machine",          2500,  10.87,  "2.5 mm²", "Twin+Earth",   "yellow"),
        ("💧", "Water Pump — 0.5 HP",       373,   1.62,  "1.5 mm²", "Twin+Earth",   "green"),
        ("💧", "Water Pump — 1 HP",         746,   3.24,  "2.5 mm²", "Twin+Earth",   "yellow"),
        ("🌡️", "Refrigerator",             200,   0.87,  "1.5 mm²", "Twin+Earth",   "green"),
        ("❄️", "AC — 1 Ton",              1500,   6.52,  "2.5 mm²", "Twin+Earth",   "yellow"),
        ("❄️", "AC — 1.5 Ton",           1800,   7.83,  "2.5 mm²", "Twin+Earth",   "yellow"),
        ("❄️", "AC — 2 Ton",             2300,  10.00,  "4.0 mm²", "3-Core",        "red"),
        ("🖥️", "Desktop Computer",          300,   1.30,  "1.5 mm²", "Twin+Earth",   "green"),
        ("💻", "Laptop Charging",            65,   0.28,  "1.5 mm²", "Twin+Earth",   "green"),
        ("📱", "Mobile Charging",            20,   0.09,  "1.5 mm²", "Twin+Earth",   "green"),
        ("📺", "LED Television",            100,   0.43,  "1.5 mm²", "Twin+Earth",   "green"),
        ("🍳", "Electric Kettle",          2000,   8.70,  "2.5 mm²", "Twin+Earth",   "yellow"),
        ("🔌", "Power Sockets (General)",   —— ,    ——,  "2.5 mm²", "Twin+Earth",   "blue"),
    ]

    for emoji, name, watts, amps, wire, cable, badge_col in APPLIANCES:
        w_str = f"{watts} W" if isinstance(watts, int) else "varies"
        a_str = f"{amps:.2f} A" if isinstance(amps, float) else "varies"
        st.markdown(f"""
        <div class="app-table-row">
            <div>{emoji} &nbsp;{name}</div>
            <div>{w_str}</div>
            <div>{a_str}</div>
            <div><b style="color:#ffcc44;">{wire}</b></div>
            <div><span class="badge badge-{badge_col}">{cable}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Home wiring guide
    st.markdown('<div class="sec-head">Standard Home Wiring Guide</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="home-guide">
        <div class="home-guide-title">⚡ Recommended Cable for Each Circuit in Your Home</div>

        <div class="home-guide-item">
            <div class="home-guide-icon">💡</div>
            <div>
                <div class="home-guide-name">Lighting Circuit</div>
                <div class="home-guide-wire">1.5 mm² Twin + Earth (2-Core)</div>
                <div class="home-guide-note">All rooms, corridors, outdoor lights — 6A breaker</div>
            </div>
        </div>

        <div class="home-guide-item">
            <div class="home-guide-icon">🔌</div>
            <div>
                <div class="home-guide-name">General Power Sockets</div>
                <div class="home-guide-wire">2.5 mm² Twin + Earth (2-Core)</div>
                <div class="home-guide-note">Standard ring main for all wall sockets — 20A breaker</div>
            </div>
        </div>

        <div class="home-guide-item">
            <div class="home-guide-icon">❄️</div>
            <div>
                <div class="home-guide-name">Air Conditioner</div>
                <div class="home-guide-wire">2.5 mm² to 4.0 mm² (Dedicated Circuit)</div>
                <div class="home-guide-note">Each AC on its own dedicated breaker — 16–20A</div>
            </div>
        </div>

        <div class="home-guide-item">
            <div class="home-guide-icon">🧺</div>
            <div>
                <div class="home-guide-name">Washing Machine / Iron</div>
                <div class="home-guide-wire">2.5 mm² Twin + Earth (Dedicated Socket)</div>
                <div class="home-guide-note">Earthing is essential — 16A breaker</div>
            </div>
        </div>

        <div class="home-guide-item">
            <div class="home-guide-icon">💧</div>
            <div>
                <div class="home-guide-name">Water Pump</div>
                <div class="home-guide-wire">1.5 mm² to 2.5 mm² (Dedicated Circuit)</div>
                <div class="home-guide-note">Use weatherproof outdoor cable — 10–16A breaker</div>
            </div>
        </div>

        <div class="home-guide-item">
            <div class="home-guide-icon">🏠</div>
            <div>
                <div class="home-guide-name">Main Incoming Supply</div>
                <div class="home-guide-wire">10 mm² to 16 mm² (Armoured Cable)</div>
                <div class="home-guide-note">From utility pole/meter to main distribution board — 40–60A</div>
            </div>
        </div>

        <div class="home-guide-item">
            <div class="home-guide-icon">⚠️</div>
            <div>
                <div class="home-guide-name">Important Safety Note</div>
                <div class="home-guide-wire" style="color:#ff8040;">Always use earthed 3-pin sockets</div>
                <div class="home-guide-note">Install RCCB (Earth Leakage breaker) for whole house protection</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="be-with-us">
        <div class="be-with-us-text">Be with us for your Queries</div>
        <div class="be-with-us-emojis">⚡ 🔌 🏠 💡 🔧 🛠️ 📐 🔋</div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Ateeq Problem Solving &nbsp;·&nbsp; Wire Sizing Helper &nbsp;·&nbsp;
    Electrical Engineering Reference Tool &nbsp;·&nbsp; For Educational & Guidance Use Only — Always Consult a Licensed Electrician
</div>
""", unsafe_allow_html=True)
