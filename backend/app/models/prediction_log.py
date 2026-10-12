"""
Log of predictions made through the API.
"""
from sqlalchemy import Column, Float, Integer, String, JSON

from backend.app.models.base import BaseModel


class PredictionLog(BaseModel):
    __tablename__ = "prediction_logs"

    crop = Column(String(100), nullable=False)
    season = Column(String(5), nullable=False)
    district = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    cultivated_area = Column(Float, nullable=True)

    input_features = Column(JSON, nullable=True)
    predicted_yield = Column(Float, nullable=False)
    model_version = Column(String(50), nullable=False)