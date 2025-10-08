# 🏠 House Price Prediction API

A simple ML project to predict house prices using **Linear Regression** + **FastAPI** + **Docker**.

## 🚀 Steps

1. Train model (in `notebooks/model_training.ipynb`)  
   - Save to `model/house_price_model.pkl`
2. Run locally:
   ```bash
   uvicorn app.main:app --reload
