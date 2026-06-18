import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Page Configuration & Styling
st.set_page_config(
    page_title="Student Mental Health and Burnout Detection",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for Light Purple Background, Black Sliders, and White Button Text
st.markdown(
    """
    <style>
    /* Main background color */
    .stApp {
        background-color: #F3E8FF; /* Light Pastel Purple */
    }
    
    /* Ensure all text layers remain crisp and readable over purple */
    h1, h2, h3, p, span, label {
        color: #2D1A4D !important; /* Deep Plum/Dark Purple for high contrast */
    }
    
    /* Input dropdowns and number input styling */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border-radius: 8px;
    }

    /* --- SLIDER BLACK THEME CUSTOMIZATION --- */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #000000 !important;
        border: 2px solid #000000 !important;
    }
    div[data-testid="stSlider"] [data-disabled="false"] > div > div > div > div {
        background: #000000 !important;
    }
    div[data-testid="stSlider"] [data-disabled="false"] {
        color: #000000 !important;
    }

    /* --- BUTTON WHITE FONT CUSTOMIZATION --- */
    div[data-testid="stButton"] button {
        background-color: #4C1D95 !important; 
        border: 1px solid #4C1D95 !important;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #3B0764 !important;
        border-color: #3B0764 !important;
    }
    div[data-testid="stButton"] button:hover p {
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Student Mental Health & Mental State Detection")
st.markdown("""
This interactive dashboard utilizes multi-dimensional student inputs to calculate predictive markers for both **Academic Burnout** and underlying **Depression Risk**.
""")
st.write("---")

st.subheader("Please Choose Student Dimension")

col1, col2 = st.columns(2)

with col1:
    academic_pressure = st.slider(
        "Academic Pressure Score (1-10)", 
        min_value=1.0, max_value=10.0, value=5.0, step=1.0,
        help="Perceived academic pressure on a scale of 1 to 10."
    )
    
    anxiety_score = st.selectbox(
        "Anxiety Score (1-10)",
        options=list(range(1, 11)),
        index=4, 
        help="Standardized anxiety levels ranging from 1 to 10."
    )
    
    cgpa = st.number_input(
        "Current CGPA (0.0 - 4.0)", 
        min_value=0.0, max_value=4.0, value=3.5, step=0.1,
        help="Current cumulative grade point average."
    )

with col2:
    attendance = st.slider(
        "Attendance Percentage (%)", 
        min_value=50.0, max_value=100.0, value=85.0, step=1.0,
        help="Class engagement and attendance record."
    )
    
    sleep_options = list(np.arange(4.0, 9.5, 0.5))
    sleep_hours = st.selectbox(
        "Daily Sleep Hours",
        options=sleep_options,
        index=6, 
        help="Average nightly sleep duration."
    )

st.write("---")

# 3. Data Processing & Prediction Simulation
st.subheader("🎯 Mental Health Assessment Results")

if st.button("🚀 Calculate Mental Health Metrics", use_container_width=True):
    with st.spinner("Processing dimensions through pipeline..."):
        time.sleep(1.2) 
        
        # --- 1. BURNOUT INDEX CALCULATION (Driven heavily by academic load)
        burnout_base = (academic_pressure * 0.4) + (anxiety_score * 0.4)
        burnout_buffers = ((cgpa / 4.0) * 0.8) + ((attendance / 100.0) * 0.8) + (((sleep_hours - 4) / 5.0) * 1.0)
        burnout_score = max(1.0, min(10.0, (burnout_base - burnout_buffers) + 2.5))
        
        # --- 2. DEPRESSION INDEX CALCULATION (Driven heavily by psychological/lifestyle strain)
        # Anxiety and sleep loss have vastly larger weights here than GPA or attendance
        depression_base = (anxiety_score * 0.6) + (academic_pressure * 0.2)
        sleep_loss_penalty = ((9.0 - sleep_hours) / 5.0) * 2.0  # Less sleep severely drives depression score up
        academic_protection = ((cgpa / 4.0) * 0.3) + ((attendance / 100.0) * 0.3)
        depression_score = max(1.0, min(10.0, (depression_base + sleep_loss_penalty - academic_protection) + 1.5))
        
        # --- DISPLAY RESULTS SIDE-BY-SIDE ---
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric(label="Predicted Burnout Score", value=f"{burnout_score:.2f}")
            if burnout_score >= 7.0:
                st.error("🚨 **High Burnout Risk:** Immediate intervention and workload reduction recommended.")
            elif 4.0 <= burnout_score < 7.0:
                st.warning("⚠️ **Moderate Burnout Risk:** Escalating strain. Consider preventive support.")
            else:
                st.success("✅ **Low Burnout Risk:** Healthy academic balance.")
                
        with res_col2:
            st.metric(label="Predicted Depression Score", value=f"{depression_score:.2f}")
            if depression_score >= 7.0:
                st.error("🚨 **High Depression Risk:** Clinical screening and professional counseling recommended.")
            elif 4.0 <= depression_score < 7.0:
                st.warning("⚠️ **Moderate Depression Risk:** Underlying mood disruptions detected. Monitor closely.")
            else:
                st.success("✅ **Low Depression Risk:** Emotional baseline appears stable.")
