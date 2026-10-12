"""
Model registry: save and load models + encoders.

Usage:
    from ml.src.models.registry import load_model, load_encoders
    model = load_model()
"""
from pathlib import Path
import joblib


MODELS_DIR = Path("ml/artifacts/models")
ENCODERS_DIR = Path("ml/artifacts/encoders")


def load_model():
    """Load the best model."""
    best_marker = MODELS_DIR / "best_model.txt"
    if not best_marker.exists():
        raise FileNotFoundError(f"No best model marker at {best_marker}")

    best_name = best_marker.read_text().strip()
    model_path = MODELS_DIR / f"best_model_{best_name}.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    return joblib.load(model_path), best_name


def load_encoders():
    """Load label encoders and scaler."""
    return joblib.load(ENCODERS_DIR / "label_encoders.pkl")


def load_scaler():
    """Load StandardScaler."""
    return joblib.load(ENCODERS_DIR / "scaler.pkl")