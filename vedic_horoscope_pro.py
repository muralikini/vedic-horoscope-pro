import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import json
import os

st.set_page_config(page_title="VedicHoroscope Pro", page_icon="🌟", layout="wide")

# ==================== ProKerala API Credentials ====================
CLIENT_ID = "8911e04f-6d6f-4756-8025-100ae826ae6e"
CLIENT_SECRET = "azJ5UWSTyAV61FRikXifGKF15e9qHPrPuCwuq07M"

st.title("🌟 VedicHoroscope Pro")
st.markdown("**ProKerala API Powered • Dynamic Vedic Astrology**")

# Profiles (kept for convenience)
PROFILES_FILE = "profiles.json"

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        try:
            with open(PROFILES_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=4)

profiles = load_profiles()

# Sidebar
with st.sidebar:
    st.header("👤 Profile Management")
    # (Profile code same as before - omitted for brevity, you can keep it)
    
    st.divider()
    st.header("Birth Details")
    name = st.text_input("Full Name", "Muralidhar Kini")
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    col1, col2 = st.columns(2)
    with col1:
        dob = st.date_input("Date of Birth", datetime(1978, 4, 14))
    with col2:
        tob = st.time_input("Time of Birth", datetime.strptime("17:00", "%H:%M").time())
    
    place = st.text_input("Birth Place", "Udupi, Karnataka, India")
    
    chart_style = st.radio("Chart Style", ["North Indian", "South Indian"])
    selected_year = st.number_input("Annual Horoscope Year", 2025, 2050, 2026)

# ==================== ProKerala API Call ====================
if st.button("Generate Horoscope using ProKerala API", type="primary", use_container_width=True):
    with st.spinner("Fetching Real Vedic Data from ProKerala..."):
        try:
            # Prepare time in required format
            birth_time = f"{dob.year}-{dob.month:02d}-{dob.day:02d} {tob.hour:02d}:{tob.minute:02d}:00"
            
            url = "https://api.prokerala.com/v2/astrology/horoscope"
            params = {
                "datetime": birth_time,
                "latitude": 13.3409,
                "longitude": 74.7421,
                "ayanamsa": "lahiri"
            }
            
            headers = {
                "Authorization": f"Bearer {CLIENT_ID}:{CLIENT_SECRET}"  # May need proper OAuth
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Real Data Received from ProKerala!")
                st.json(data)  # Temporary - shows raw response
                
                # You can parse data['horoscope'] etc. here later
                
            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Failed to connect to ProKerala API: {e}")
            st.info("Falling back to simulated data...")

        # Fallback / Simulated Content
        st.subheader("Life Areas Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Career** — Communication, Tech, Teaching, Business")
            st.write("**Finance** — Gradual growth")
        with col2:
            st.write("**Health** — Stress & nervous system")
            st.write("**Marriage / Kids** — Stable with effort")

st.caption("VedicHoroscope Pro • Powered by ProKerala API")
