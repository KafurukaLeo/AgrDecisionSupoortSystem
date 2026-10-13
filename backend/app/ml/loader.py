"""
Model loader for the ML prediction engine.

Loads the trained model and label encoders at backend startup.
Ensures the same preprocessing used in training is applied at inference.
"""
from pathlib import Path
import json
import joblib
from functools import lru_cache

from backend.app.config import get_settings


ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


@lru_cache(maxsize=1)
def get_model():
    """Load the trained model once and cache it."""
    model_path = ARTIFACTS / "model.pkl"
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}. "
            f"Run `cp ml/artifacts/models/*.pkl backend/app/ml/artifacts/model.pkl` first."
        )
    return joblib.load(model_path)


@lru_cache(maxsize=1)
def get_encoders():
    """Load all label encoders once and cache them."""
    encoders_path = ARTIFACTS / "label_encoders.pkl"
    if not encoders_path.exists():
        raise FileNotFoundError(
            f"Encoders file not found: {encoders_path}. "
            f"Run `cp ml/artifacts/encoders/*.pkl backend/app/ml/artifacts/` first."
        )
    return joblib.load(encoders_path)


@lru_cache(maxsize=1)
def get_feature_columns():
    """Load the ordered list of feature columns."""
    path = ARTIFACTS / "feature_columns.json"
    if not path.exists():
        raise FileNotFoundError(f"Feature columns file not found: {path}")
    with open(path) as f:
        return json.load(f)


@lru_cache(maxsize=1)
def get_model_name():
    """Return the name of the current best model."""
    path = ARTIFACTS / "best_model.txt"
    if not path.exists():
        return "unknown"
    return path.read_text().strip()


def model_status():
    """Return a status report of the model artifacts."""
    return {
        "model_loaded": (ARTIFACTS / "model.pkl").exists(),
        "encoders_loaded": (ARTIFACTS / "label_encoders.pkl").exists(),
        "feature_columns_loaded": (ARTIFACTS / "feature_columns.json").exists(),
        "model_name": get_model_name(),
    }