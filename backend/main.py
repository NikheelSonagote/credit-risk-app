from fastapi import FastAPI
import joblib
import pandas as pd
import os
from schema import LoanData

app = FastAPI(title="Credit Risk Prediction API")

# ... your routes ...

if __name__ == "__main__":
    # Railway provides the port via an environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# ✅ Load model properly
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "models", "model.pkl")

model = joblib.load(model_path)

print("✅ Model loaded:", type(model))

@app.get("/")
def read_root():
    return {"message": "Credit Risk API is running!"}

@app.post("/predict")
def predict(data: LoanData):
    try:
        input_dict = data.dict()

        # ✅ Add missing defaults
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