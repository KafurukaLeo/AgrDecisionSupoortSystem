"""
Location model: Province and District.
"""
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from backend.app.models.base import BaseModel


class Province(BaseModel):
    __tablename__ = "provinces"

    name = Column(String(100), unique=True, nullable=False, index=True)

    districts = relationship("District", back_populates="province")


class District(BaseModel):
    __tablename__ = "districts"

    name = Column(String(100), nullable=False, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)

    province = relationship("Province", back_populates="districts")
    productivity_records = relationship("ProductivityRecord", back_populates="district")