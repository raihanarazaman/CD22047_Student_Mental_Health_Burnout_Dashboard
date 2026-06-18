import numpy as np
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

# 1. Initialize FastAPI Application Instance
app = FastAPI(title="CD22047 Student Burnout Prediction Engine", version="1.0.0")

# 2. Configure Cross-Origin Resource Sharing (CORS) Security Policies
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Securely Load Your Trained 5-Feature Random Forest Binary Pipeline Artifacts
try:
    model = joblib.load('rf_regressor_model.pkl')
    scaler = joblib.load('regressor_scaler.pkl')
except FileNotFoundError:
    print("⚠️ Weight binaries missing from execution root directory path.")

# 4. Construct Data Validation Schema Mapping to Your Top 5 Features
class StudentProfileSchema(BaseModel):
    academic_pressure: float
    anxiety_score: float
    cgpa: float
    attendance: float
    sleep_hours: float

# 5. Continuous Prediction API Endpoint Route
@app.post("/predict")
async def process_burnout_metrics(profile: StudentProfileSchema):
    try:
        # Extract frontend variables in the sequence expected by the model
        raw_input_matrix = np.array([[
            profile.academic_pressure,
            profile.anxiety_score,
            profile.cgpa,
            profile.attendance,
            profile.sleep_hours
        ]])
        
        # Apply standard data scale parameters
        standardized_matrix = scaler.transform(raw_input_matrix)
        
        # Execute model prediction to find continuous burnout index score (0.00 - 10.00)
        calculated_score = float(model.predict(standardized_matrix)[0])
        risk_percentage = (calculated_score / 10.0) * 100
        
        # Assign thresholds, status badges, and custom hex colors matching your style preferences
        if calculated_score <= 3.50:
            tier = "Low Burnout Risk State"
            hex_color = "#2ecc71" # Vibrant Protective Green
            analysis = "Stable baseline conditions observed. Student maintains adequate biological sleep rest buffers."
        elif 3.50 < calculated_score <= 6.50:
            tier = "Medium Burnout Risk State"
            hex_color = "#f39c12" # Amber Caution Warning
            analysis = "Early operational imbalances noted. Sleep windows are declining due to academic workload constraints."
        else:
            tier = "Critical High Burnout Risk State"
            hex_color = "#e74c3c" # Threat Red Danger
            analysis = "Severe time-allocation stress combined with critical sleep deprivation. Immediate support highly advised."
            
        return {
            "index_score": round(calculated_score, 2),
            "percentage_metric": round(risk_percentage, 1),
            "status_tier": tier,
            "theme_hex": hex_color,
            "clinical_critique": analysis
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 6. Default Route to Serve Your Custom HTML5 Dashboard UI
@app.get("/", response_class=HTMLResponse)
async def deliver_dashboard_interface():
    html_target_path = os.path.join("templates", "dashboard.html")
    if os.path.exists(html_target_path):
        with open(html_target_path, "r", encoding="utf-8") as file:
            return file.read()
    return "<h1>Critical System Deployment Anomaly: 'templates/dashboard.html' file matrix path is broken.</h1>"