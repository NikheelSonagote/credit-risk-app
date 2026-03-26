import pandas as pd
import os
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load data
url = "https://raw.githubusercontent.com/selva86/datasets/master/GermanCredit.csv"
df = pd.read_csv(url)

# Split
X = df.drop("credit_risk", axis=1)
y = df["credit_risk"]

# Column separation
categorical_cols = X.select_dtypes(include='object').columns
numerical_cols = X.select_dtypes(include='int64').columns

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]
)

# Pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', LogisticRegression(max_iter=2000, class_weight='balanced'))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Train
pipeline.fit(X_train, y_train)

# ✅ SAVE MODEL (IMPORTANT)
# ✅ Load model
BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "models", "model.pkl")

os.makedirs(os.path.dirname(model_path), exist_ok=True)

joblib.dump(pipeline, model_path)

print("✅ Model trained and saved at:", model_path)