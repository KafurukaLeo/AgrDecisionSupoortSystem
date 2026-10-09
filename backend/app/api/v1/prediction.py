"""
Prediction endpoint (dummy for now).
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class PredictionRequest(BaseModel):
    crop: str = Field(..., example="Maize")
    season: str = Field(..., example="A")
    district: str = Field(..., example="Kigali")
    year: int = Field(..., example=2024)
    fertilizer_used: bool = Field(False, example=True)
    irrigation_used: bool = Field(False, example=False)
    cultivated_area: float = Field(..., gt=0, example=2.5)


class PredictionResponse(BaseModel):
    predicted_yield: float
    unit: str
    confidence_interval: list[float]
    model_version: str
    disclaimer: str


@router.post("/", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Return a placeholder prediction."""
    # Dummy logic — will be replaced with actual model
    base = 3.0
    if request.fertilizer_used:
        base += 0.5
    if request.irrigation_used:
        base += 0.3

    return PredictionResponse(
        predicted_yield=round(base, 2),
        unit="tons/hectare",
        confidence_interval=[round(base - 0.4, 2), round(base + 0.4, 2)],
        model_version="placeholder_v0",
        disclaimer="Placeholder prediction. Real model will be integrated later.",
    )