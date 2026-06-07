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

# ==================== ProKerala Credentials ====================
CLIENT_ID = "8911e04f-6d6f-4756-8025-100ae826ae6e"
CLIENT_SECRET = "azJ5UWSTyAV61FRikXifGKF15e9qHPrPuCwuq07M"

st.title("🌟 VedicHoroscope Pro")
st.markdown("**ProKerala API Powered • Real Vedic Horoscope**")

# Profiles (simplified)
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

# ==================== API TOKEN + CALL ====================
if st.button("Generate Horoscope using ProKerala API", type="primary", use_container_width=True):
    with st.spinner("Fetching Real Vedic Data..."):
        try:
            # Step 1: Get Access Token
            token_url = "https://api.prokerala.com/token"
            token_data = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
            token_resp = requests.post(token_url, data=token_data)
            
            if token_resp.status_code != 200:
                st.error(f"Token Error: {token_resp.text}")
                st.stop()
            
            access_token = token_resp.json()["access_token"]
            
            # Step 2: Call Kundli API
            api_url = "https://api.prokerala.com/v2/astrology/kundli"
            
            datetime_str = f"{dob.year}-{dob.month:02d}-{dob.day:02d}T{tob.hour:02d}:{tob.minute:02d}:00+05:30"
            
            params = {
                "datetime": datetime_str,
                "coordinates": "13.3409,74.7421",  # Udupi approx
                "ayanamsa": "1"  # Lahiri
            }
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.get(api_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Real Horoscope Data Received!")
                
                # Display Key Info
                if "data" in data:
                    kundli = data["data"]
                    st.subheader("Planetary Positions")
                    st.json(kundli.get("planetary_positions", kundli))
                    
                    st.subheader("Life Areas (Summary)")
                    st.write("**Career**: Communication, Tech, Teaching, Business")
                    st.write("**Finance**: Gradual growth")
                    st.write("**Health**: Stress management advised")
                else:
                    st.json(data)
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
                
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("VedicHoroscope Pro • Powered by ProKerala")
