import streamlit as st
import requests
from datetime import datetime

# API Endpoint
API_URL = "https://kmeans-fullstack.onrender.com"  # Update this when deploying

# Page Configuration
st.set_page_config(page_title="Doctor Recommendation System", page_icon="🩺", layout="centered")

# Custom Styles
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 12px;
            border-radius: 8px;
        }
        .stTextInput>div>div>input {
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
        }
        .title-text {
            font-size: 36px;
            font-weight: bold;
            color: #2E8B57;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# UI Title
st.markdown('<p class="title-text">🩺 Doctor Recommendation System</p>', unsafe_allow_html=True)

# Input Time
st.write("### Enter Appointment Time")
time_input = st.time_input("Select Time", datetime.now().time())

# Convert to HH:MM format
formatted_time = time_input.strftime("%H:%M")

# Submit Button
if st.button("🔍 Get Recommended Doctors"):
    with st.spinner("Fetching recommendations..."):
        response = requests.get(f"{API_URL}?time={formatted_time}")

        if response.status_code == 200:
            doctors = response.json().get("Recommended Doctors", [])
            if doctors:
                st.success("✅ Doctors Found!")
                st.write("### Recommended Doctors:")
                for doc in doctors:
                    st.markdown(f"- **👨‍⚕️ NPI: {doc}**")
            else:
                st.warning("⚠️ No doctors found for this time.")
        else:
            st.error("❌ Error fetching recommendations. Please try again.")
