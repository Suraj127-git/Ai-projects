import pickle
import os
import logging

logger = logging.getLogger(__name__)

def load_model():
    """Load the model with error handling"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), "../model/spam_model.pkl")
        
        # Check if model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        
        vectorizer = model.get("vectorizer")
        clf = model.get("classifier")
        
        if vectorizer is None or clf is None:
            raise ValueError("Model file is missing required components")
            
        logger.info("Model loaded successfully")
        return vectorizer, clf
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

# Load model at startup
try:
    vectorizer, clf = load_model()
except Exception as e:
    print(f"Failed to load model: {e}")
    vectorizer, clf = None, None

def predict_email(text: str):
    """Predict if an email is spam or ham"""
    if vectorizer is None or clf is None:
        raise RuntimeError("Model not loaded properly")
    
    X = vectorizer.transform([text])
    pred = clf.predict(X)[0]
    prob = clf.predict_proba(X).max()
    return pred, float(prob)