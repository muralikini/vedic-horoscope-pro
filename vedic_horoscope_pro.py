import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import json
import os

st.set_page_config(page_title="VedicHoroscope Pro", page_icon="🌟", layout="wide")

# Profiles
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

st.title("🌟 VedicHoroscope Pro")
st.markdown("**Multi-Person Vedic Astrology App with Monthly Predictions**")

# Sidebar - Profile Management
with st.sidebar:
    st.header("👤 Profile Management")
    action = st.radio("Action", ["Load Profile", "Create New"], horizontal=True)
    
    if action == "Load Profile" and profiles:
        selected = st.selectbox("Select Profile", list(profiles.keys()))
        if st.button("Load Profile"):
            st.session_state.current = profiles[selected]
            st.rerun()
    
    st.divider()
    st.header("Birth Details")
    
    current = st.session_state.get("current", {})
    
    name = st.text_input("Full Name", value=current.get("name", "New Person"))
    gender = st.selectbox("Gender", ["Male", "Female"], index=0)
    
    col1, col2 = st.columns(2)
    with col1:
        dob = st.date_input("Date of Birth", datetime.strptime(current.get("dob", "1990-01-01"), "%Y-%m-%d").date() if current.get("dob") else datetime(1978,4,14).date())
    with col2:
        tob = st.time_input("Time of Birth", datetime.strptime(current.get("tob", "17:00"), "%H:%M").time() if current.get("tob") else datetime.strptime("17:00", "%H:%M").time())
    
    place = st.text_input("Birth Place", value=current.get("place", "Udupi, Karnataka, India"))
    
    if st.button("💾 Save Profile"):
        profiles[name] = {"name": name, "gender": gender, "dob": str(dob), "tob": str(tob), "place": place}
        save_profiles(profiles)
        st.success(f"✅ Profile '{name}' Saved!")

    st.divider()
    chart_style = st.radio("Chart Style", ["North Indian", "South Indian"])
    selected_year = st.number_input("Annual Horoscope Year", 2025, 2050, 2026)

# Generate Button
if st.button("Generate Complete Horoscope", type="primary", use_container_width=True):
    with st.spinner("Analyzing Birth Chart..."):
        # Basic Dynamic Logic
        year = dob.year
        lagna = "Gemini" if (month := dob.month) in [4,5] else "Cancer" if month in [6,7] else "Leo"  # Very basic simulation
        
        st.success(f"Horoscope Generated for **{name}** (Born {dob})")
        
        tabs = st.tabs(["Natal Chart", "Annual Forecast", "Gemstones", "Remedies", "Full Analysis"])
        
        with tabs[0]:
            st.subheader(f"Natal Chart — {name}")
            st.info(f"**Lagna**: {lagna} | **Moon Sign**: Simulated based on input")
            st.caption("Note: For fully accurate planetary positions, professional software is recommended.")
        
        with tabs[1]:
            st.subheader(f"📅 Annual Horoscope — {selected_year}")
            st.write("**General Prediction**: A year of mixed results. Focus on communication, learning, and steady effort.")
            
            st.subheader("Month-wise Predictions (General)")
            # Generic but structured
            for month in ["January","April","July","October"]:
                with st.expander(month):
                    st.write("**Career**: Opportunities through networking")
                    st.write("**Finance**: Moderate growth")
                    st.write("**Health**: Manage stress")
                    st.write("**Family**: Generally supportive")
        
        with tabs[2]:
            st.subheader("💎 Gemstone Recommendations")
            st.info("**Common Recommendation**: Emerald or Ruby (consult local astrologer)")
        
        with tabs[3]:
            st.subheader("🛠️ Remedies")
            st.write("- Chant Gayatri Mantra daily")
            st.write("- Perform remedies as per your specific chart")
        
        with tabs[4]:
            st.subheader("Important Note")
            st.warning("This app currently uses **simulated / general** predictions. For highly accurate Vedic calculations (planetary degrees, exact dasha, etc.), we need a proper astrology library.")

# PDF Download (Basic)
        if st.button("📥 Download PDF Report"):
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, f"Horoscope Report - {name}")
            c.drawString(100, 720, f"DOB: {dob} | Place: {place}")
            c.drawString(100, 690, f"Year: {selected_year}")
            c.save()
            buffer.seek(0)
            st.download_button("Download PDF", buffer, f"{name}_Horoscope.pdf", "application/pdf")

st.caption("VedicHoroscope Pro • Multi-Person Support")
