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
# Removed "models" from the path below
model_path = os.path.join(BASE_DIR, "model.pkl") 

model = None
try:
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("✅ Success: Model loaded from root directory")
    else:
        print(f"❌ ERROR: Model not found at {model_path}")
except Exception as e:
    print(f"❌ ERROR loading model: {e}")

@app.get("/")
def home():
    return {"message": "API is running", "model_loaded": model is not None}

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