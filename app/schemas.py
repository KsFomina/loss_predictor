from typing import Literal
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    request_id: str = Field(..., min_length=1)
    item_id:str=Field(..., min_length=1)
    item_price: float=Field(..., ge=0)
    delivery_days: int=Field(..., ge=0)
    client_is_app:bool
    type_prepayment: Literal["card", "cash","sbp"]

class PredictionResponse(BaseModel):
    request_id:str
    prediction:float
    model_version:str

