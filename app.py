import streamlit as st
import pandas as pd
import joblib
import numpy as np

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

import os

@st.cache_resource
def load_assets():
    # Force the app to look in the exact directory where app.py lives
    base_path = os.path.dirname(__file__)
    
    model_path = os.path.join(base_path, "rf_regressor_model.pkl")
    scaler_path = os.path.join(base_path, "regressor_scaler.pkl")
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

try:
    model, scaler = load_assets()
except Exception as e:
    st.error(f"⚠️ Error loading model or scaler files: {e}")
    st.stop()

# 3. Interactive User Interface Components (Chapter 5.1 Dimensions)
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

# 4. Data Processing & Prediction
st.subheader("🎯 Burnout Assessment Result")

# Create a dataframe using the exact feature names your model was trained on
# NOTE: Replace these column names if your dataset used different headers (e.g., 'cgpa' vs 'CGPA')
input_data = pd.DataFrame([{
    'Academic Pressure Score': academic_pressure,
    'Anxiety Score': anxiety_score,
    'Current CGPA': cgpa,
    'Attendance Percentage': attendance,
    'Daily Sleep Hours': sleep_hours
}])

if st.button("🚀 Calculate Burnout Risk Index", use_container_width=True):
    with st.spinner("Processing dimensions through pipeline..."):
        try:
            # Scale the input data using the imported scaler
            scaled_input = scaler.transform(input_data)
            
            # Predict using the Random Forest model
            prediction = model.predict(scaled_input)[0]
            
            # Display Result
            # Assuming output is a score (adjust formatting based on your target variable logic)
            st.metric(label="Predicted Burnout Score", value=f"{prediction:.2f}")
            
            # Provide Contextual Feedback based on the score
            if prediction >= 7.0:
                st.error("🚨 **High Risk of Burnout:** Immediate intervention, counseling, and workload reduction are strongly recommended.")
            elif 4.0 <= prediction < 7.0:
                st.warning("⚠️ **Moderate Risk of Burnout:** Student is experiencing manageable but escalating strain. Consider preventive support.")
            else:
                st.success("✅ **Low Risk of Burnout:** Healthy balance detected. Encourage maintaining current habits.")
                
        except Exception as e:
            st.error(f"Prediction Error: {str(e)}")
            st.info("Tip: Double-check that the feature names match the exact column order your scaler/model expects.")
