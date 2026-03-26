from fastapi import FastAPI
import joblib
import pandas as pd
import os
from schema import LoanData
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Credit Risk Prediction API")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# ✅ Load model
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "models", "model.pkl")

model = joblib.load(model_path)

print("✅ Model loaded:", type(model))

# ✅ Health route (IMPORTANT for Railway)
@app.get("/")
def home():
    return {"message": "API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Predict route
@app.post("/predict")
def predict(data: LoanData):
    try:
        input_dict = data.dict()

        input_dict.setdefault("installment_rate", 2)
        input_dict.setdefault("other_installment_plans", "none")

        df = pd.DataFrame([input_dict])

        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]

        return {
            "prediction": int(prediction),
            "probability": float(probability)
        }

    except Exception as e:
        return {"error": str(e)}