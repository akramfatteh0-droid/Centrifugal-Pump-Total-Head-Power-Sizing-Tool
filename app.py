import math
import pandas as pd
import streamlit as st

# ============================================================
# CENTRIFUGAL PUMP TOTAL HEAD & POWER SIZING TOOL
# GitHub + Streamlit Community Cloud ready
# ============================================================

st.set_page_config(
    page_title="Centrifugal Pump Sizing Tool",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- CSS ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #F4F7FB;
        color: #102A43;
    }

    [data-testid="stSidebar"] {
        background: #0B1F3A;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    .team-box {
        background: #FFFFFF;
        border: 2px solid #1976D2;
        border-radius: 14px;
        padding: 18px 22px;
        margin: 10px 0 22px 0;
        box-shadow: 0 3px 12px rgba(11,31,58,0.10);
    }

    .team-title {
        color: #0B1F3A;
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .teacher {
        color: #B45309;
        font-weight: 800;
        margin-top: 10px;
    }

    [data-testid="stSidebar"] {
        background: #081827;
    }

    .main-title {
        text-align: center;
        font-size: clamp(30px, 5vw, 48px);
        font-weight: 800;
        margin-bottom: 4px;
        color: #0B1F3A;
    }

    .main-title span {
        color: #38c4ff;
    }

    .subtitle {
        text-align: center;
        color: #334E68;
        margin-bottom: 28px;
    }

    .result-card {
        background: #FFFFFF;
        border: 1px solid #B8C7D9;
        border-radius: 14px;
        padding: 16px;
        min-height: 110px;
        margin-bottom: 12px;
    }

    .result-label {
        color: #486581;
        font-size: 13px;
    }

    .result-value {
        color: #0B63CE;
        font-size: 25px;
        font-weight: 700;
        margin-top: 6px;
    }

    .motor-card {
        background: #FFFFFF;
        border: 1px solid #2d644a;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        margin-top: 12px;
        margin-bottom: 20px;
    }

    .motor-label {
        color: #486581;
        font-size: 14px;
    }

    .motor-value {
        color: #087F5B;
        font-size: 30px;
        font-weight: 800;
        margin-top: 6px;
    }

    .info-card {
        background: #FFFFFF;
        border: 1px solid #B8C7D9;
        border-radius: 14px;
        padding: 18px;
    }

    .footer {
        text-align: center;
        color: #486581;
        padding: 25px 0 10px;
    }

    div.stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- Header -------------------------
st.markdown(
    '<div class="main-title">Centrifugal Pump <span>Total Head & Power</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">'
    "Calculate total manometric head, hydraulic power, shaft power and recommended motor size."
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="team-box">
    <div class="team-title">🐍 Group Name: Python Masters</div>
    <b>Project Team Members</b><br>
    1. Fatteh Saad — Enrollment No. 25012250610079<br>
    2. Fatteh Akram — Enrollment No. 25012250610078<br>
    3. Memdu Ahmad — Enrollment No. 25012250610077<br>
    4. Ghanchi Sahil — Enrollment No. 25012250610047<br>
    <div class="teacher">Teacher: Mohammad Shaikh Azim</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------- Sidebar ------------------------
st.sidebar.header("⚙️ Input Parameters")

flow = st.sidebar.number_input(
    "Flow Rate",
    min_value=0.01,
    value=25.0,
    step=1.0,
    format="%.2f",
)

flow_unit = st.sidebar.selectbox(
    "Flow Unit",
    ["m³/h", "L/s"],
)

suction = st.sidebar.number_input(
    "Static Suction Lift (m)",
    min_value=0.0,
    value=5.0,
    step=0.5,
)

delivery = st.sidebar.number_input(
    "Static Delivery Head (m)",
    min_value=0.0,
    value=30.0,
    step=0.5,
)

pipe_length = st.sidebar.number_input(
    "Pipe Length (m)",
    min_value=0.0,
    value=80.0,
    step=1.0,
)

diameter_mm = st.sidebar.number_input(
    "Pipe Internal Diameter (mm)",
    min_value=1.0,
    value=50.0,
    step=1.0,
)

roughness_mm = st.sidebar.number_input(
    "Pipe Roughness (mm)",
    min_value=0.0,
    value=0.045,
    step=0.005,
    format="%.3f",
)

efficiency_percent = st.sidebar.number_input(
    "Pump Efficiency (%)",
    min_value=1.0,
    max_value=100.0,
    value=80.0,
    step=1.0,
)

st.sidebar.caption(
    "Water assumption: ρ = 1000 kg/m³, g = 9.81 m/s², "
    "kinematic viscosity ν = 1.004 × 10⁻⁶ m²/s."
)

# ----------------------------- Calculation --------------------
def calculate_pump(
    flow_value,
    unit,
    suction_lift,
    delivery_head,
    pipe_len,
    diameter,
    roughness,
    efficiency,
):
    if unit == "m³/h":
        q = flow_value / 3600.0
    else:
        q = flow_value / 1000.0

    diameter_m = diameter / 1000.0
    roughness_m = roughness / 1000.0

    rho = 1000.0
    g = 9.81
    nu = 1.004e-6

    area = math.pi * diameter_m**2 / 4.0
    velocity = q / area
    reynolds = velocity * diameter_m / nu

    if reynolds < 2300:
        friction_factor = 64.0 / reynolds
        flow_regime = "Laminar"
    else:
        friction_factor = 0.25 / (
            math.log10(
                roughness_m / (3.7 * diameter_m)
                + 5.74 / (reynolds**0.9)
            )
            ** 2
        )
        flow_regime = "Turbulent"

    friction_head = (
        friction_factor
        * (pipe_len / diameter_m)
        * (velocity**2 / (2.0 * g))
    )

    static_head = suction_lift + delivery_head
    total_head = static_head + friction_head

    water_power_kw = rho * g * q * total_head / 1000.0
    shaft_power_kw = water_power_kw / efficiency
    shaft_hp = shaft_power_kw / 0.746

    # Same 15% design allowance used in the supplied HTML.
    motor_required_kw = shaft_power_kw * 1.15

    standard_motor_sizes = [
        0.37, 0.55, 0.75, 1.1, 1.5,
        2.2, 3.0, 3.7, 5.5, 7.5,
        11.0, 15.0, 18.5, 22.0, 30.0,
        37.0, 45.0, 55.0, 75.0, 90.0, 110.0,
    ]

    recommended_motor_kw = next(
        (size for size in standard_motor_sizes if size >= motor_required_kw),
        math.ceil(motor_required_kw),
    )

    recommended_motor_hp = recommended_motor_kw / 0.746

    return {
        "flow_m3s": q,
        "flow_m3h": q * 3600.0,
        "diameter_m": diameter_m,
        "area": area,
        "velocity": velocity,
        "reynolds": reynolds,
        "flow_regime": flow_regime,
        "friction_factor": friction_factor,
        "friction_head": friction_head,
        "static_head": static_head,
        "total_head": total_head,
        "water_power_kw": water_power_kw,
        "shaft_power_kw": shaft_power_kw,
        "shaft_hp": shaft_hp,
        "motor_required_kw": motor_required_kw,
        "recommended_motor_kw": recommended_motor_kw,
        "recommended_motor_hp": recommended_motor_hp,
    }


result = calculate_pump(
    flow,
    flow_unit,
    suction,
    delivery,
    pipe_length,
    diameter_mm,
    roughness_mm,
    efficiency_percent / 100.0,
)

# ----------------------------- Results -----------------------
st.subheader("📊 Calculation Results")

cards = [
    ("Static Head", f"{result['static_head']:.2f} m"),
    ("Pipe Velocity", f"{result['velocity']:.2f} m/s"),
    ("Friction Head", f"{result['friction_head']:.2f} m"),
    ("Total Manometric Head", f"{result['total_head']:.2f} m"),
]

columns = st.columns(4)

for column, (label, value) in zip(columns, cards):
    with column:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">{label}</div>
                <div class="result-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------- Power --------------------------
st.subheader("⚡ Power Calculation")

p1, p2, p3 = st.columns(3)

with p1:
    st.metric("Hydraulic / Water Power", f"{result['water_power_kw']:.2f} kW")

with p2:
    st.metric("Shaft Power", f"{result['shaft_power_kw']:.2f} kW")

with p3:
    st.metric("Shaft Power", f"{result['shaft_hp']:.2f} HP")

st.markdown(
    f"""
    <div class="motor-card">
        <div class="motor-label">Recommended Standard Motor</div>
        <div class="motor-value">
            {result['recommended_motor_kw']:.2f} kW /
            {result['recommended_motor_hp']:.1f} HP
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- Details -----------------------
st.subheader("🔧 Engineering Details")

d1, d2 = st.columns(2)

with d1:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write(f"**Flow Rate:** {flow:.2f} {flow_unit}")
    st.write(f"**Flow:** {result['flow_m3s']:.6f} m³/s")
    st.write(f"**Pipe Diameter:** {diameter_mm:.2f} mm")
    st.write(f"**Pipe Area:** {result['area']:.6f} m²")
    st.write(f"**Pipe Length:** {pipe_length:.2f} m")
    st.markdown("</div>", unsafe_allow_html=True)

with d2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write(f"**Reynolds Number:** {result['reynolds']:,.0f}")
    st.write(f"**Flow Regime:** {result['flow_regime']}")
    st.write(f"**Friction Factor:** {result['friction_factor']:.5f}")
    st.write(f"**Pump Efficiency:** {efficiency_percent:.1f}%")
    st.write(f"**Motor Design Requirement:** {result['motor_required_kw']:.2f} kW")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------- Graph --------------------------
st.subheader("📈 Head vs Flow Rate")

current_flow = result["flow_m3h"]
max_flow = max(100.0, current_flow * 2.0)

flow_values = []
head_values = []

for i in range(101):
    q = max_flow * i / 100.0
    h = max(0.0, result["total_head"] * (1.0 - 0.65 * (q / max_flow) ** 2))
    flow_values.append(q)
    head_values.append(h)

graph_data = pd.DataFrame(
    {
        "Flow Rate (m³/h)": flow_values,
        "Head (m)": head_values,
    }
)

st.line_chart(
    graph_data,
    x="Flow Rate (m³/h)",
    y="Head (m)",
)

# ----------------------------- Formulas ----------------------
with st.expander("📐 Engineering Formulas Used"):
    st.code(
        """
Q = Flow rate converted to m³/s

Velocity = Q / Pipe Area

Reynolds Number = V × D / ν

Friction Head = f × (L/D) × (V² / 2g)

Total Manometric Head =
Static Suction Lift + Static Delivery Head + Friction Head

Water Power = ρ × g × Q × Total Head

Shaft Power = Water Power / Pump Efficiency

HP = Shaft Power / 0.746

Motor Requirement = Shaft Power × 1.15
        """,
        language="text",
    )

st.info(
    "Engineering note: this is a sizing/calculation tool. "
    "Final pump and motor selection should be checked against the "
    "manufacturer's pump curve, system losses, and applicable design standards."
)

st.markdown(
    '<div class="footer">Centrifugal Pump Total Head & Power Sizing Tool • Engineering Project</div>',
    unsafe_allow_html=True,
)
