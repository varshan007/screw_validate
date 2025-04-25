import streamlit as st
import math

# Constants
STANDARD_TROUGH_LOAD = 0.45
DRIVE_EFFICIENCY = 0.88
GRAVITY = 32.2

st.title("Biomass Screw Conveyor Designer")

st.sidebar.header("Input Parameters")

# User Inputs
biomass_type = st.sidebar.text_input("Biomass Type", "rice husk")
feed_rate_kgph = st.sidebar.number_input("Feed Rate (kg/hr)", 100, 10000, 500)
bulk_density = st.sidebar.number_input("Bulk Density (kg/m³)", 50, 1000, 180)
moisture_content = st.sidebar.slider("Moisture Content (%)", 0, 100, 15)
incline_angle_deg = st.sidebar.slider("Inclination Angle (°)", 0, 45, 20)

# Conversion
feed_rate_cfh = (feed_rate_kgph / bulk_density) * 35.3147

# Screw diameter
def calculate_screw_diameter(cfh):
    if cfh < 2000:
        return 6
    elif cfh < 6000:
        return 9
    elif cfh < 10000:
        return 12
    else:
        return 16

# Pitch
def calculate_pitch(diameter):
    return diameter

# Shaft Diameter
def calculate_shaft_diameter(screw_diameter):
    return round(screw_diameter * 0.3, 2)

# Thickness
def calculate_thickness(diameter):
    if diameter <= 9:
        return 0.25
    elif diameter <= 12:
        return 0.375
    else:
        return 0.5

# Power Requirement
def calculate_power(feed_rate_cfh, bulk_density, incline_deg, diameter):
    MHP = (feed_rate_cfh * bulk_density * GRAVITY * math.sin(math.radians(incline_deg))) / (33000 * 60)
    FHP = 0.5
    fi = 1 + (incline_deg / 90)
    TSHP = ((FHP + MHP) * fi) / DRIVE_EFFICIENCY
    return round(TSHP, 2)

# Material Selection
def recommend_material(biomass, mc):
    if "wood" in biomass or "husk" in biomass:
        return "Stainless Steel 304"
    elif "wet" in biomass or mc > 25:
        return "316 SS or Coated Carbon Steel"
    else:
        return "Mild Steel"

# Calculations
Ds = calculate_screw_diameter(feed_rate_cfh)
pitch = calculate_pitch(Ds)
shaft_dia = calculate_shaft_diameter(Ds)
thickness = calculate_thickness(Ds)
material = recommend_material(biomass_type, moisture_content)
power_hp = calculate_power(feed_rate_cfh, bulk_density / 62.4, incline_angle_deg, Ds)

# Results Display
st.subheader("Design Output")

st.write(f"**Screw Diameter:** {Ds} inch")
st.write(f"**Pitch:** {pitch} inch")
st.write(f"**Shaft Diameter:** {shaft_dia} inch")
st.write(f"**Flight Thickness:** {thickness} inch")
st.write(f"**Material:** {material}")
st.write(f"**Inclination Angle:** {incline_angle_deg}°")
st.write(f"**Power Requirement:** {power_hp} HP")