from fastapi import FastAPI, HTTPException
from app.schemas import EmailRequest, EmailResponse
from app.model import predict_email, vectorizer, clf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Spam Email Classifier API")

@app.on_event("startup")
async def startup_event():
    """Check if model is loaded on startup"""
    if vectorizer is None or clf is None:
        logger.error("Model failed to load during startup")
        raise RuntimeError("Model not loaded properly")
    logger.info("Spam Classifier API started successfully")

@app.get("/")
def home():
    return {"message": "Spam Email Classifier is running 🚀"}

@app.post("/predict", response_model=EmailResponse)
def predict(request: EmailRequest):
    try:
        prediction, probability = predict_email(request.text)
        return EmailResponse(prediction=prediction, probability=probability)
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))