"""
Filter options endpoint (placeholder).
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/options")
def get_filter_options():
    return {
        "crops": ["Maize", "Beans", "Rice", "Potatoes", "Bananas", "Cassava"],
        "seasons": ["A", "B", "C"],
        "years": [2020, 2021, 2022, 2023, 2024, 2025],
        "provinces": ["Kigali", "Northern", "Southern", "Eastern", "Western"],
        "districts": ["Gasabo", "Kicukiro", "Nyarugenge", "Musanze", "Huye"],
    }