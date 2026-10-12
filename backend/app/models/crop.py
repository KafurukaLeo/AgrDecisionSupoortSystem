"""
Crop model.
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from backend.app.models.base import BaseModel


class Crop(BaseModel):
    __tablename__ = "crops"

    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=True)  # e.g., cereal, legume, tuber

    productivity_records = relationship("ProductivityRecord", back_populates="crop")