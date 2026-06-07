import streamlit as st
import requests
from datetime import datetime
import json

st.set_page_config(page_title="VedicHoroscope Pro", page_icon="🌟", layout="wide")

CLIENT_ID = "8911e04f-6d6f-4756-8025-100ae826ae6e"
CLIENT_SECRET = "yM7M3BTjO16l51l8j2fg8AZnC2Q2lHOVMAmzPXMt"

st.title("🌟 VedicHoroscope Pro")
st.markdown("**ProKerala API • Real Vedic Horoscope**")

with st.sidebar:
    st.header("Birth Details")
    name = st.text_input("Full Name", "Muralidhar Kini")
    dob = st.date_input("Date of Birth", datetime(1978, 4, 14))
    tob = st.time_input("Time of Birth", datetime.strptime("17:00", "%H:%M").time())
    place = st.text_input("Birth Place", "Udupi, Karnataka, India")

if st.button("Generate Horoscope using ProKerala API", type="primary"):
    with st.spinner("Authenticating & Fetching Data..."):
        try:
            # Get Access Token
            token_url = "https://api.prokerala.com/token"
            token_data = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
            
            token_response = requests.post(token_url, data=token_data, timeout=10)
            
            if token_response.status_code != 200:
                st.error(f"Authentication Failed: {token_response.text}")
                st.info("Please double-check your Client ID and Client Secret in the dashboard.")
                st.stop()
            
            access_token = token_response.json()["access_token"]
            st.success("✅ Authentication Successful!")

            # Call Kundli API
            api_url = "https://api.prokerala.com/v2/astrology/kundli"
            datetime_str = f"{dob.year}-{dob.month:02d}-{dob.day:02d}T{tob.hour:02d}:{tob.minute:02d}:00+05:30"
            
            params = {
                "datetime": datetime_str,
                "coordinates": "13.3409,74.7421",
                "ayanamsa": "1"
            }
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.get(api_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Horoscope Generated Successfully!")
                st.json(data)   # Raw output for now
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")

st.caption("If authentication keeps failing, try regenerating Client Secret from ProKerala Dashboard")
