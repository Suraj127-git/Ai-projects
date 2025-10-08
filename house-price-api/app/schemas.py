from pydantic import BaseModel
from typing import List

class HouseFeatures(BaseModel):
    features: List[float]  # list of numeric values
