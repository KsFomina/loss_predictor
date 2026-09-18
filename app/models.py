
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime

from app.database import Base

class ItemFeature(Base):
    __tablename__='item_features'
    item_id= Column(String, primary_key=True, index=True)
    historical_return_rate = Column(Float, nullable=False)
    avg_item_losses_30d=Column(Float, nullable=False)
    updated_at=Column(DateTime, nullable=True)

class Prediction(Base):
    __tablename__='predictions'
    request_id = Column(String, primary_key=True, index=True)
    prediction =Column(Float, nullable=False)
    model_version = Column(String, nullable=False)
