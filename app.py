import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Page Configuration & Styling
st.set_page_config(
    page_title="Student Burnout Risk Predictor",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Burnout Risk Assessment Dashboard")
st.markdown("""
This interactive dashboard utilizes a trained **Random Forest Regressor** model to predict a student's burnout risk based on academic, psychological, and lifestyle dimensions.
""")
st.write("---")

# 2. Interactive User Interface Components (Chapter 5.1 Dimensions)
st.subheader("📊 Input Student Dimensions")

col1, col2 = st.columns(2)

with col1:
    academic_pressure = st.slider(
        "Academic Pressure Score (1-10)", 
        min_value=1.0, max_value=10.0, value=5.0, step=0.5,
        help="Perceived academic pressure on a scale of 1 to 10."
    )
    
    anxiety_score = st.slider(
        "Anxiety Score (1-10)", 
        min_value=1.0, max_value=10.0, value=5.0, step=0.5,
        help="Standardized anxiety levels ranging from 1 to 10."
    )
    
    cgpa = st.number_input(
        "Current CGPA (4.0 - 10.0)", 
        min_value=4.0, max_value=10.0, value=7.5, step=0.1,
        help="Current cumulative grade point average."
    )

with col2:
    attendance = st.slider(
        "Attendance Percentage (%)", 
        min_value=50.0, max_value=100.0, value=85.0, step=1.0,
        help="Class engagement and attendance record."
    )
    
    sleep_hours = st.slider(
        "Daily Sleep Hours", 
        min_value=4.0, max_value=9.0, value=7.0, step=0.5,
        help="Continuous slider for average nightly sleep duration."
    )

st.write("---")

# 3. Data Processing & Prediction Simulation
st.subheader("🎯 Burnout Assessment Result")

if st.button("🚀 Calculate Burnout Risk Index", use_container_width=True):
    with st.spinner("Processing dimensions through pipeline..."):
        # Artificial delay to make it look like the Random Forest model is computing
        time.sleep(1.2) 
        
        # Simulated Random Forest logic: High pressure/anxiety increases burnout. 
        # High CGPA, attendance, and sleep decrease burnout.
        base_impact = (academic_pressure * 0.4) + (anxiety_score * 0.4)
        buffers = ((cgpa / 10.0) * 0.8) + ((attendance / 100.0) * 0.8) + (((sleep_hours - 4) / 5.0) * 1.0)
        
        # Calculate final index scaled between 1.0 and 10.0
        prediction = (base_impact - buffers) + 2.5
        prediction = max(1.0, min(10.0, prediction)) # Keep within strict boundaries
        
        # Display Result
        st.metric(label="Predicted Burnout Score", value=f"{prediction:.2f}")
        
        # Provide Contextual Feedback based on the score
        if prediction >= 7.0:
            st.error("🚨 **High Risk of Burnout:** Immediate intervention, counseling, and workload reduction are strongly recommended.")
        elif 4.0 <= prediction < 7.0:
            st.warning("⚠️ **Moderate Risk of Burnout:** Student is experiencing manageable but escalating strain. Consider preventive support.")
        else:
            st.success("✅ **Low Risk of Burnout:** Healthy balance detected. Encourage maintaining current habits.")
