import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="VedicHoroscope Pro", page_icon="🌟", layout="wide")

# ProKerala Credentials
CLIENT_ID = "8911e04f-6d6f-4756-8025-100ae826ae6e"
CLIENT_SECRET = "azJ5UWSTyAV61FRikXifGKF15e9qHPrPuCwuq07M"

st.title("🌟 VedicHoroscope Pro")
st.markdown("**ProKerala API • Real Vedic Horoscope**")

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

if st.button("Generate Horoscope using ProKerala API", type="primary", use_container_width=True):
    with st.spinner("Connecting to ProKerala API..."):
        try:
            # Get Access Token
            token_resp = requests.post(
                "https://api.prokerala.com/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET
                }
            )
            
            if token_resp.status_code != 200:
                st.error(f"Authentication Error: {token_resp.text}")
                st.stop()
            
            access_token = token_resp.json()["access_token"]

            # Use January 1st for Sandbox Mode
            test_date = datetime(2025, 1, 1, tob.hour, tob.minute)
            datetime_str = f"{test_date.year}-{test_date.month:02d}-{test_date.day:02d}T{test_date.hour:02d}:{test_date.minute:02d}:00+05:30"
            
            response = requests.get(
                "https://api.prokerala.com/v2/astrology/kundli",
                params={
                    "datetime": datetime_str,
                    "coordinates": "13.3409,74.7421",
                    "ayanamsa": "1"
                },
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Horoscope Generated (Sandbox Mode)")
                st.json(data)  # Show raw data
                
            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")

st.info("**Note**: In Sandbox mode, ProKerala only allows January 1st. For full dates, you need to upgrade to Production mode.")

st.caption("VedicHoroscope Pro • Powered by ProKerala")
