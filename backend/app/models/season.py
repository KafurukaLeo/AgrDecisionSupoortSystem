from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.app.models.base import BaseModel


class Season(BaseModel):
    __tablename__ = "seasons"
    __table_args__ = (
        UniqueConstraint("code", "year", name="uq_season_code_year"),
    )

    code = Column(String(5), nullable=False)   # "A", "B", "C"
    description = Column(String(200), nullable=True)
    year = Column(Integer, nullable=False, index=True)

    productivity_records = relationship("ProductivityRecord", back_populates="season")