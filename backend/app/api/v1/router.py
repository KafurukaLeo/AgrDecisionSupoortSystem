"""
Aggregates all v1 API routes.
"""
from fastapi import APIRouter

from backend.app.api.v1 import health, productivity, prediction, filters

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(productivity.router, prefix="/productivity", tags=["Productivity"])
api_router.include_router(prediction.router, prefix="/predict", tags=["Prediction"])
api_router.include_router(filters.router, prefix="/filters", tags=["Filters"])