from fastapi import FastAPI
import joblib
import pandas as pd
import os
from schema import LoanData
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Credit Risk Prediction API")

# ✅ CORS: Allows your index.html to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# ✅ Load model (Fixed path: looking in the same folder as main.py)
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "model.pkl")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Could not find model.pkl at {model_path}")

model = joblib.load(model_path)

@app.get("/")
def home():
    return {"message": "Credit Risk API is Live"}

@app.POST("/predict")
def predict(data: LoanData):
    try:
        # ✅ Use model_dump() for Pydantic v2 compatibility
        input_dict = data.model_dump()
        
        # Ensure DataFrame column names match what the model expects
        df = pd.DataFrame([input_dict])

        prediction = model.predict(df)[0]
        # Get probability if the model supports it
        probability = model.predict_proba(df)[0].max() if hasattr(model, "predict_proba") else 1.0

        return {
            "prediction": int(prediction),
            "probability": f"{round(float(probability) * 100, 2)}%"
        }
    except Exception as e:
        return {"error": str(e)}