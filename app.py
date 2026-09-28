import streamlit as st
import math
import pandas as pd

st.set_page_config(
    page_title="Centrifugal Pump Sizing Tool",
    page_icon="⚙️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #06111f;
    color: #eef7ff;
}
h1, h2, h3 { color: #eef7ff; }
.title {
    text-align:center;
    color:#42c4ff;
    font-size:42px;
    font-weight:bold;
}
.subtitle {
    text-align:center;
    color:#9eb3c7;
    font-size:18px;
    margin-bottom:30px;
}
.result-box {
    background:#071522;
    border:1px solid #203d54;
    border-radius:12px;
    padding:18px;
    margin-bottom:12px;
}
.result-title { color:#8fa6b9; font-size:14px; }
.result-value {
    color:#57c8ff;
    font-size:26px;
    font-weight:bold;
}
.motor-box {
    background:#071522;
    border:1px solid #203d54;
    border-radius:12px;
    padding:20px;
    text-align:center;
}
.motor-value {
    color:#73e3a0;
    font-size:30px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">⚙️ Centrifugal Pump Total Head & Power</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Calculate total manometric head, hydraulic power, '
    'shaft power and recommended motor size</div>',
    unsafe_allow_html=True
)

st.sidebar.header("⚙️ Input Parameters")

flow = st.sidebar.number_input("Flow Rate", min_value=0.01, value=25.0, step=1.0)
flow_unit = st.sidebar.selectbox("Flow Unit", ["m³/h", "L/s"])

suction = st.sidebar.number_input(
    "Static Suction Lift (m)", min_value=0.0, value=5.0, step=1.0
)
delivery = st.sidebar.number_input(
    "Static Delivery Head (m)", min_value=0.0, value=30.0, step=1.0
)
pipe_length = st.sidebar.number_input(
    "Pipe Length (m)", min_value=0.0, value=80.0, step=1.0
)
diameter_mm = st.sidebar.number_input(
    "Pipe Internal Diameter (mm)", min_value=1.0, value=50.0, step=1.0
)
roughness_mm = st.sidebar.number_input(
    "Pipe Roughness (mm)", min_value=0.0, value=0.045, step=0.005
)
efficiency_percent = st.sidebar.number_input(
    "Pump Efficiency (%)", min_value=1.0, max_value=100.0,
    value=80.0, step=1.0
)

st.sidebar.button("🔵 CALCULATE", use_container_width=True)

if flow_unit == "m³/h":
    Q = flow / 3600.0
else:
    Q = flow / 1000.0

D = diameter_mm / 1000.0
roughness = roughness_mm / 1000.0
efficiency = efficiency_percent / 100.0

rho = 1000.0
g = 9.81
nu = 1.004e-6

area = math.pi * D**2 / 4.0
velocity = Q / area
Re = velocity * D / nu

if Re < 2300:
    friction_factor = 64.0 / Re
else:
    friction_factor = 0.25 / (
        math.log10(
            roughness / (3.7 * D) + 5.74 / (Re ** 0.9)
        ) ** 2
    )

friction_head = (
    friction_factor
    * (pipe_length / D)
    * (velocity ** 2 / (2 * g))
)

static_head = suction + delivery
total_head = static_head + friction_head

water_power_kw = rho * g * Q * total_head / 1000.0
shaft_power_kw = water_power_kw / efficiency
shaft_hp = shaft_power_kw / 0.746

motor_required = shaft_power_kw * 1.15

motor_sizes = [
    0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3, 3.7,
    5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45,
    55, 75, 90, 110
]

recommended_motor = next(
    (x for x in motor_sizes if x >= motor_required),
    math.ceil(motor_required)
)
recommended_hp = recommended_motor / 0.746

st.subheader("📊 Calculation Results")

c1, c2, c3, c4 = st.columns(4)

results = [
    ("Static Head", f"{static_head:.2f} m"),
    ("Pipe Velocity", f"{velocity:.2f} m/s"),
    ("Friction Head", f"{friction_head:.2f} m"),
    ("Total Manometric Head", f"{total_head:.2f} m"),
]

for col, (name, value) in zip([c1, c2, c3, c4], results):
    with col:
        st.markdown(
            f'<div class="result-box">'
            f'<div class="result-title">{name}</div>'
            f'<div class="result-value">{value}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.subheader("⚡ Power Calculation")

p1, p2, p3 = st.columns(3)

with p1:
    st.metric("Hydraulic / Water Power", f"{water_power_kw:.2f} kW")
with p2:
    st.metric("Shaft Power", f"{shaft_power_kw:.2f} kW")
with p3:
    st.metric("Shaft Power", f"{shaft_hp:.2f} HP")

st.markdown(
    f'<div class="motor-box">'
    f'<div class="result-title">Recommended Standard Motor</div>'
    f'<div class="motor-value">{recommended_motor} kW / '
    f'{recommended_hp:.1f} HP</div>'
    f'</div>',
    unsafe_allow_html=True
)

st.subheader("🔧 Engineering Details")

d1, d2 = st.columns(2)

with d1:
    st.write(f"**Flow Rate:** {flow:.2f} {flow_unit}")
    st.write(f"**Flow:** {Q:.6f} m³/s")
    st.write(f"**Pipe Diameter:** {diameter_mm:.2f} mm")
    st.write(f"**Pipe Area:** {area:.6f} m²")

with d2:
    st.write(f"**Reynolds Number:** {Re:,.0f}")
    st.write(f"**Friction Factor:** {friction_factor:.5f}")
    st.write(f"**Pipe Velocity:** {velocity:.2f} m/s")
    st.write(f"**Pump Efficiency:** {efficiency_percent:.1f}%")

st.subheader("📈 Head vs Flow Rate")

current_flow_m3h = Q * 3600.0
max_flow = max(100.0, current_flow_m3h * 2.0)

flow_range = []
head_range = []

for i in range(101):
    q = max_flow * i / 100.0
    h = max(0.0, total_head * (1 - 0.65 * (q / max_flow) ** 2))
    flow_range.append(q)
    head_range.append(h)

chart_data = pd.DataFrame({
    "Flow Rate (m³/h)": flow_range,
    "Head (m)": head_range
})

st.line_chart(chart_data, x="Flow Rate (m³/h)", y="Head (m)")

st.subheader("📐 Engineering Formulas")

st.code("""
Q = Flow rate converted to m³/s
Velocity = Q / Pipe Area
Reynolds Number = V × D / ν
Friction Head = f × (L/D) × (V² / 2g)
Total Manometric Head = Suction Lift + Delivery Head + Friction Head
Water Power = ρ × g × Q × Total Head
Shaft Power = Water Power / Pump Efficiency
HP = Shaft Power / 0.746
Motor Requirement = Shaft Power × 1.15
""")

st.markdown("---")
st.caption("Centrifugal Pump Total Head & Power Sizing Tool • Engineering Project")
