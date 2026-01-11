# Tiki Book Demand Prediction

This project predicts book demand using Tiki e-commerce data to support
offline bookstore inventory decisions.

## Project Structure
- 01_book_sale_prediction.ipnb: EDA and training
- src/: feature engineer logic
- app/: API and web app
- models/: trained model

## How to Run

### Install dependencies
pip install -r requirements.txt

### Run API
python -m uvicorn app.api:app --reload

### Run Web App
python -m streamlit run app/web.py
