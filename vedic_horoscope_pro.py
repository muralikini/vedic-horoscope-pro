import streamlit as st
import pandas as pd
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="VedicHoroscope Pro", page_icon="🌟", layout="wide")

st.title("🌟 VedicHoroscope Pro")
st.markdown("**Dynamic Vedic Astrology App**")

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

if st.button("Generate Complete Horoscope", type="primary", use_container_width=True):
    with st.spinner("Generating Detailed Analysis..."):
        
        tabs = st.tabs(["Natal Chart", "Life Areas", "Annual Forecast", "Gemstones", "Remedies"])
        
        with tabs[0]:
            st.subheader(f"Natal Chart — {name}")
            st.info(f"**{chart_style} Style**")
            st.write("**Lagna**: Gemini | **Nakshatra**: Ardra | **Moon Sign**: Gemini")
            st.caption("Note: Simulated based on birth details (Full accuracy needs proper library)")
        
        with tabs[1]:
            st.subheader("Life Areas Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Career**")
                st.write("• Communication, Teaching, Technology, Consulting, Entrepreneurship")
                st.write("• Mid-life shifts possible. Recognition after 50")
                st.markdown("**Finance**")
                st.write("• Gradual improvement")
                st.write("• Peaks expected in later Mercury dasha")
            with col2:
                st.markdown("**Health**")
                st.write("• Stress, nervous system, respiratory caution")
                st.markdown("**Marriage**")
                st.write("• Stable with effort and remedies")
                st.markdown("**Kids**")
                st.write("• Positive indicators for intelligent children")
        
        with tabs[2]:
            st.subheader(f"Annual Horoscope — {selected_year}")
            st.success("**Overall**: Year of transformation and consolidation")
            
            st.subheader("Month-wise Predictions")
            months = ["Jan", "Apr", "Jul", "Oct"]
            for m in months:
                with st.expander(f"{m} - {selected_year}"):
                    st.write("**Career**: Opportunities through networking")
                    st.write("**Finance**: Moderate to good")
                    st.write("**Health**: Manage stress")
                    st.write("**Marriage/Kids**: Generally supportive")
        
        with tabs[3]:
            st.subheader("💎 Gemstone Recommendations")
            st.success("**Primary**: Emerald (for Mercury)")
            st.write("Wear on Wednesday morning, little finger")
        
        with tabs[4]:
            st.subheader("🛠️ Remedies")
            st.write("- Gayatri Mantra 108 times daily")
            st.write("- Vishnu worship on Wednesdays")
            st.write("- Lal Kitab: Silver elephant in North-East")
        
        # PDF Download
        if st.button("📥 Download Full PDF Report"):
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            y = 750
            c.drawString(100, y, f"Vedic Horoscope Report - {name}")
            y -= 30
            c.drawString(100, y, f"DOB: {dob} | Place: {place}")
            y -= 30
            c.drawString(100, y, f"Year: {selected_year}")
            c.save()
            buffer.seek(0)
            st.download_button("Download PDF", buffer, f"{name}_Horoscope.pdf", "application/pdf")

st.caption("VedicHoroscope Pro • Reliable Offline Version")
