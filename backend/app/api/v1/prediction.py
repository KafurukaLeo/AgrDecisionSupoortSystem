"""
Prediction endpoint — serves ML model predictions.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.ml.predictor import predict_yield
from backend.app.ml.loader import model_status

router = APIRouter()


class PredictionRequest(BaseModel):
    crop: str = Field(..., example="Maize")
    crop_category: str = Field("Cereal", example="Cereal")
    season: str = Field("A", example="A")
    province: str = Field("Kigali", example="Kigali")
    district: str = Field("Gasabo", example="Gasabo")
    stratum: str = Field("LSF", example="LSF")
    farmer_gender: str = Field("Male", example="Male")
    land_use: str = Field("Agricultural land on hillside",
                          example="Agricultural land on hillside")
    cropping_system: str = Field("Pure Cropping", example="Pure Cropping")
    plot_area_ha: float = Field(1.0, gt=0, example=1.0)
    crop_area_ha: float = Field(1.0, gt=0, example=1.0)
    harvest_ratio: float = Field(100.0, ge=0, example=100.0)
    farmer_age: int = Field(40, ge=0, example=40)
    fertilizer_used: bool = Field(False)
    irrigation_used: bool = Field(False)
    pesticide_used: bool = Field(False)
    improved_seeds_used: bool = Field(False)
    anti_erosion_activity: bool = Field(False)
    organic_fertilizer_used: bool = Field(False)
    inorganic_fertilizer_used: bool = Field(False)
    irrigation_practiced: bool = Field(False)
    plot_irrigated: bool = Field(False)


class PredictionResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    predicted_yield: float
    predicted_yield_t_ha: float
    unit: str
    confidence_interval: list[float]
    confidence_interval_t_ha: list[float]
    model_version: str
    disclaimer: str


@router.get("/status")
def prediction_status():
    """Report whether the model is loaded and ready."""
    return model_status()


@router.post("/", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Predict yield based on the trained Random Forest model.
    """
    try:
        payload = request.model_dump()
        result = predict_yield(payload)
        return PredictionResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")