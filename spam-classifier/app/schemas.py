from pydantic import BaseModel

class EmailRequest(BaseModel):
    text: str

class EmailResponse(BaseModel):
    prediction: str
    probability: float
