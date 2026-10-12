"""
Productivity record: main analytical table.
"""
from sqlalchemy import Column, Float, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from backend.app.models.base import BaseModel


class ProductivityRecord(BaseModel):
    __tablename__ = "productivity_records"

    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False, index=True)

    cultivated_area = Column(Float, nullable=True)     # hectares
    production = Column(Float, nullable=True)          # tons
    yield_value = Column(Float, nullable=True, index=True)  # tons/hectare

    fertilizer_used = Column(String(10), nullable=True)  # "yes"/"no"/null
    irrigation_used = Column(String(10), nullable=True)
    improved_seeds_used = Column(String(10), nullable=True)
    pesticide_used = Column(String(10), nullable=True)

    crop = relationship("Crop", back_populates="productivity_records")
    season = relationship("Season", back_populates="productivity_records")
    district = relationship("District", back_populates="productivity_records")