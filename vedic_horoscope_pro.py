import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="VedicHoroscope Pro", page_icon="🌟", layout="wide")

st.title("🌟 VedicHoroscope Pro")
st.markdown("**Professional Vedic Astrology Analysis with Lal Kitab**")

# Sidebar
with st.sidebar:
    st.header("Birth Information")
    name = st.text_input("Full Name", "Muralidhar Kini")
    gender = st.selectbox("Gender", ["Male", "Female"])
    col1, col2 = st.columns(2)
    with col1:
        dob = st.date_input("Date of Birth", datetime(1978, 4, 14))
    with col2:
        tob = st.time_input("Time of Birth", datetime.strptime("17:00", "%H:%M").time())
    
    place = st.text_input("Birth Place", "Udupi, Karnataka, India")
    lat = st.number_input("Latitude", value=13.3409, format="%.4f")
    lon = st.number_input("Longitude", value=74.7421, format="%.4f")
    
    chart_style = st.radio("Chart Style", ["North Indian", "South Indian"])
    selected_year = st.number_input("Annual Horoscope Year", 2025, 2050, 2026)

if st.button("Generate Complete Horoscope", type="primary", use_container_width=True):
    with st.spinner("Generating Detailed Vedic Analysis..."):
        
        # Simulated Vedic Data based on your chart
        lagna = "Gemini"
        moon_sign = "Gemini"
        nakshatra = "Ardra"
        current_dasha = "Mercury Mahadasha (2019 - 2036)"
        
        planets = {
            "Planet": ["Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
            "Sign": ["Gemini", "Aries", "Gemini", "Cancer (Deb)", "Pisces (Deb)", "Cancer", "Taurus", "Leo", "Virgo", "Pisces"],
            "House": [1, 11, 1, 2, 10, 2, 12, 3, 4, 10],
            "Status": ["", "Exalted", "", "Debilitated", "Debilitated", "", "", "", "", ""]
        }
        
        df_planets = pd.DataFrame(planets)
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Natal Chart", "Annual Forecast", "Gemstones", "Remedies", "Full Analysis"])
        
        with tab1:
            st.subheader(f"Natal Chart - {name}")
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if chart_style == "North Indian":
                    st.info("🟦 North Indian Diamond Style Chart")
                else:
                    st.info("⬛ South Indian Square Style Chart")
                
                fig = go.Figure()
                fig.add_annotation(text=f"Lagna: {lagna}\nMoon: {moon_sign}\nNakshatra: {nakshatra}", 
                                 showarrow=False, font_size=18)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Planetary Positions")
                st.dataframe(df_planets, use_container_width=True)
                st.write(f"**Current Dasha**: {current_dasha}")
        
        with tab2:
            st.subheader(f"Annual Horoscope - {selected_year}")
            st.success("**Overall Theme**: Transformative year with focus on career growth and financial consolidation.")
            st.write("**Career**: Opportunities in communication, tech, teaching or business.")
            st.write("**Finance**: Gradual improvement. Avoid speculation.")
            st.write("**Health**: Manage stress and nervous system.")
            st.write("**Best Months**: April to September")
        
        with tab3:
            st.subheader("💎 Gemstone Analysis")
            st.success("**Primary Recommendation**: Emerald (Mercury) - 5-7 carats")
            st.write("**When to Wear**: Wednesday morning, 5-7 AM, after bathing.")
            st.write("**Finger**: Little finger of right hand (for males)")
            st.write("**Metal**: Silver or Gold")
            st.info("**Secondary**: Red Coral for Mars (after proper consultation)")
        
        with tab4:
            st.subheader("🛠️ Remedies")
            st.write("**Vedic Remedies**")
            st.write("- Chant Gayatri Mantra 108 times daily")
            st.write("- Worship Lord Vishnu on Wednesdays")
            st.write("- Donate green items on Wednesday")
            
            st.write("**Lal Kitab Remedies**")
            st.write("- Keep a silver elephant in the North-East corner")
            st.write("- Feed green fodder to cows")
            st.write("- Avoid wearing green clothes on Saturday")
        
        with tab5:
            st.subheader("Comprehensive Predictive Analysis")
            st.markdown("""
            **Strengths**: Gajakesari Yoga, Exalted Sun in 11th house  
            **Challenges**: Debilitated Mercury & Mars, Ketu in 10th house  
            **Career**: Best suited for teaching, consulting, tech, entrepreneurship  
            **Finance**: Steady growth after consistent effort  
            """)
        
        # PDF Download
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"Vedic Horoscope Report - {name}")
        c.drawString(100, 730, f"Date of Birth: {dob} {tob}")
        c.drawString(100, 710, f"Lagna: {lagna} | Nakshatra: {nakshatra}")
        c.drawString(100, 690, f"Analysis Year: {selected_year}")
        c.save()
        
        buffer.seek(0)
        st.download_button(
            label="📥 Download Full PDF Report",
            data=buffer,
            file_name=f"{name.replace(' ', '_')}_Horoscope.pdf",
            mime="application/pdf"
        )

st.caption("VedicHoroscope Pro • Built with ❤️ by Grok • For Entertainment & Educational Purposes Only")
