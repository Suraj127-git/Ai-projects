from fastapi import FastAPI
from app.schemas import HouseFeatures
from app.model import predict_price

app = FastAPI(title="House Price Prediction API")

@app.get("/")
def root():
    return {"message": "Welcome to House Price Prediction API!"}

@app.post("/predict")
def get_prediction(data: HouseFeatures):
    prediction = predict_price(data.features)
    return {"predicted_price": prediction}
