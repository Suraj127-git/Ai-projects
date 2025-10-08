import joblib
import numpy as np

# Load model
model = joblib.load("model/house_price_model.pkl")

def predict_price(features: list):
    arr = np.array(features).reshape(1, -1)
    prediction = model.predict(arr)
    return prediction[0]
