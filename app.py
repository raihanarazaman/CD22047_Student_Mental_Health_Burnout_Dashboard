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

# Custom CSS for Light Purple Background and Black Sliders
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
    
    /* 1. Change the slider handle (the dot) to black */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #000000 !important;
        border: 2px solid #000000 !important;
    }
    
    /* 2. Change the active track (left side of the handle) to black */
    div[data-testid="stSlider"] [data-disabled="false"] > div > div > div > div {
        background: #000000 !important;
    }
    
    /* 3. Keep the floating value label above the slider readable */
    div[data-testid="stSlider"] [data-disabled="false"] {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Student Mental Health and Burnout Detection")

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
        index=4, # Defaults to 5
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
        index=6, # Defaults to 7.0
        help="Average nightly sleep duration."
    )

st.write("---")

# 3. Data Processing & Prediction Simulation
st.subheader("🎯 Burnout Assessment Result")

if st.button("🚀 Calculate Burnout Risk Index", use_container_width=True):
    with st.spinner("Processing dimensions through pipeline..."):
        time.sleep(1.2) 
        
        # Mathematical Simulation
        base_impact = (academic_pressure * 0.4) + (anxiety_score * 0.4)
        buffers = ((cgpa / 4.0) * 0.8) + ((attendance / 100.0) * 0.8) + (((sleep_hours - 4) / 5.0) * 1.0)
        
        prediction = (base_impact - buffers) + 2.5
        prediction = max(1.0, min(10.0, prediction)) # Keep within strict boundaries
        
        st.metric(label="Predicted Burnout Score", value=f"{prediction:.2f}")
        
        # Provide Contextual Feedback based on the score
        if prediction >= 7.0:
            st.error("🚨 **High Risk of Burnout:** Immediate intervention, counseling, and workload reduction are strongly recommended.")
        elif 4.0 <= prediction < 7.0:
            st.warning("⚠️ **Moderate Risk of Burnout:** Student is experiencing manageable but escalating strain. Consider preventive support.")
        else:
            st.success("✅ **Low Risk of Burnout:** Healthy balance detected. Encourage maintaining current habits.")
