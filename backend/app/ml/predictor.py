"""
Prediction pipeline.

Combines loader + preprocessor + model to produce predictions.
"""
import numpy as np

from backend.app.ml.loader import get_model, get_model_name
from backend.app.ml.preprocessor import preprocess


def predict_yield(request_dict):
    """
    Generate a yield prediction for a single input.

    Parameters
    ----------
    request_dict : dict
        Example:
            {
                "crop": "Maize",
                "season": "A",
                "district": "Gasabo",
                "province": "Kigali",
                "stratum": "LSF",
                "crop_category": "Cereal",
                "farmer_gender": "Male",
                "land_use": "Agricultural land on hillside",
                "cropping_system": "Pure Cropping",
                "crop_area_ha": 1.0,
                "plot_area_ha": 1.2,
                "fertilizer_used": 1,
                "irrigation_used": 0,
                "pesticide_used": 0,
                "improved_seeds_used": 1,
            }

    Returns
    -------
    dict with predicted_yield, confidence_interval, model_version.
    """
    model = get_model()

    # Preprocess input to numeric features
    X = preprocess(request_dict)

    # The model was trained on log1p(yield). Predict, then inverse-transform.
    log_pred = float(model.predict(X)[0])
    y_pred_kg_ha = float(np.expm1(log_pred))

    # Guard against negative predictions
    y_pred_kg_ha = max(y_pred_kg_ha, 0.0)

    # Approximate 95% confidence interval based on typical RF spread
    # (this is a heuristic; a production system would use quantile regression
    # or bootstrapped trees)
    spread = 0.30  # ±30% of prediction
    low = y_pred_kg_ha * (1 - spread)
    high = y_pred_kg_ha * (1 + spread)

    # Convert to tons/hectare for display
    y_pred_t_ha = y_pred_kg_ha / 1000.0
    low_t_ha = low / 1000.0
    high_t_ha = high / 1000.0

    return {
        "predicted_yield": round(y_pred_kg_ha, 2),
        "predicted_yield_t_ha": round(y_pred_t_ha, 2),
        "unit": "kg/hectare",
        "confidence_interval": [round(low, 2), round(high, 2)],
        "confidence_interval_t_ha": [round(low_t_ha, 2), round(high_t_ha, 2)],
        "model_version": get_model_name(),
        "disclaimer": (
            "This is a statistical prediction based on historical patterns "
            "in the NISR SAS 2025 dataset. It does not guarantee actual "
            "productivity, which depends on many factors beyond the model."
        ),
    }