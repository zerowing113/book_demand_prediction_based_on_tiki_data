from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib

app = FastAPI(title="Book Demand Prediction API")

model = joblib.load("models/book_demand_model.pkl")

class BookInput(BaseModel):
    category: str
    current_price: float = Field(gt=0)
    original_price: float = Field(gt=0)
    avg_rating: float = Field(ge=0, le=5)
    n_review: int = Field(ge=0)
    pages: int = Field(gt=0)

def demand_bucket(qty):
    if qty < 200:
        return "Low"
    elif qty < 2000:
        return "Medium"
    else:
        return "High"

@app.post("/predict")
def predict_demand(book: BookInput):

    input_df = pd.DataFrame([book.dict()])

    raw_pred = model.predict(input_df)[0]

    # Handle negative prediction
    final_pred = max(0, raw_pred)

    bucket = demand_bucket(final_pred)

    return {
        "predicted_quantity": int(final_pred),
        "demand_level": bucket
    }
