"""
Preprocessor for incoming prediction requests.

Applies the same transformations used during training:
- Categorical encoding (via saved label encoders)
- Numeric default fill for missing values
- Feature ordering
"""
import pandas as pd
import numpy as np

from backend.app.ml.loader import get_encoders, get_feature_columns


CATEGORICAL_FEATURES = [
    "crop",
    "crop_category",
    "province",
    "district",
    "stratum",
    "season",
    "farmer_gender",
    "land_use",
    "cropping_system",
]

BINARY_FEATURES = [
    "fertilizer_used",
    "irrigation_used",
    "pesticide_used",
    "improved_seeds_used",
    "anti_erosion_activity",
    "organic_fertilizer_used",
    "inorganic_fertilizer_used",
    "irrigation_practiced",
    "plot_irrigated",
]

NUMERIC_FEATURES = [
    "plot_area_ha",
    "crop_area_ha",
    "harvest_ratio",
    "farmer_age",
]

# Median defaults (used only if a numeric input is missing)
DEFAULT_VALUES = {
    "plot_area_ha": 0.5,
    "crop_area_ha": 0.5,
    "harvest_ratio": 100.0,
    "farmer_age": 40,
}


def encode_categorical(value, encoder, default_label="Unknown"):
    """Safely encode a categorical value with a fallback for unseen values."""
    if value is None:
        value = default_label
    value = str(value).strip().strip('"').strip("'")

    classes = list(encoder.classes_)
    if value in classes:
        return int(encoder.transform([value])[0])

    # Fallback: try case-insensitive match
    lower = value.lower()
    for cls in classes:
        if cls.lower() == lower:
            return int(encoder.transform([cls])[0])

    # Fallback: use most common class (index 0 in most encoders) or "Unknown"
    if "Unknown" in classes:
        return int(encoder.transform(["Unknown"])[0])
    return 0  # last-resort default


def preprocess(request_dict):
    """
    Convert a user request into a numeric feature vector.

    Parameters
    ----------
    request_dict : dict
        Keys should include crop, season, district, etc.

    Returns
    -------
    pd.DataFrame with one row, columns in the training order.
    """
    encoders = get_encoders()
    feature_columns = get_feature_columns()

    row = {}

    # Categorical features
    for cat in CATEGORICAL_FEATURES:
        raw_value = request_dict.get(cat)
        if cat in encoders:
            encoded = encode_categorical(raw_value, encoders[cat])
        else:
            encoded = 0
        row[cat + "_encoded"] = encoded

    # Binary features
    for bin_feature in BINARY_FEATURES:
        raw = request_dict.get(bin_feature, 0)
        try:
            row[bin_feature] = int(bool(raw)) if isinstance(raw, bool) else int(raw)
        except (ValueError, TypeError):
            row[bin_feature] = 0

    # Numeric features
    for num in NUMERIC_FEATURES:
        raw = request_dict.get(num)
        if raw is None or (isinstance(raw, float) and np.isnan(raw)):
            row[num] = DEFAULT_VALUES.get(num, 0.0)
        else:
            try:
                row[num] = float(raw)
            except (ValueError, TypeError):
                row[num] = DEFAULT_VALUES.get(num, 0.0)

    # Assemble in training order
    df = pd.DataFrame([row])

    # Ensure all training columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns exactly as training
    df = df[feature_columns]

    return df