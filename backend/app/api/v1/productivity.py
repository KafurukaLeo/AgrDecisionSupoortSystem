"""
Productivity endpoints (dummy data for now).
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
def get_summary():
    """Overall productivity KPIs (placeholder)."""
    return {
        "average_yield": 2.85,
        "total_production_tons": 1250000,
        "total_cultivated_hectares": 438000,
        "unit": "tons/hectare",
        "note": "Placeholder data — will be replaced with real NISR data",
    }


@router.get("/by-crop")
def get_by_crop():
    """Productivity grouped by crop (placeholder)."""
    return {
        "data": [
            {"crop": "Maize", "average_yield": 3.2},
            {"crop": "Beans", "average_yield": 1.8},
            {"crop": "Rice", "average_yield": 4.1},
            {"crop": "Potatoes", "average_yield": 8.5},
        ],
        "note": "Placeholder data",
    }