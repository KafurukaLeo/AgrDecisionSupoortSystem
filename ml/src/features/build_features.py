"""
Feature engineering for NISR SAS 2025.

Loads integrated parquet, builds ML-ready features, saves to artifacts.

Usage:
    python -m ml.src.features.build_features
"""
from pathlib import Path
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

import joblib


INPUT = Path("data/processed/sas_2025_integrated.parquet")
ARTIFACTS = Path("ml/artifacts")
ENCODERS = ARTIFACTS / "encoders"
PROCESSED = ARTIFACTS / "processed"


# Feature configuration
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

TARGET = "yield_value"
WEIGHT = "survey_weight"


def clean_features(df):
    """Basic feature cleaning before encoding."""
    print("Cleaning features...")

    # Drop rows without target
    df = df.dropna(subset=[TARGET]).copy()
    print(f"  After dropping null target: {len(df)} rows")

    # Drop rows with negative or zero yield
    df = df[df[TARGET] > 0].copy()
    print(f"  After dropping zero/negative yield: {len(df)} rows")

    # Strip quotes and whitespace from categorical features
    for col in CATEGORICAL_FEATURES:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.strip('"').str.strip("'")
            df[col] = df[col].replace({"nan": "Unknown", "": "Unknown"})

    # Fill binary features
    for col in BINARY_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Fill numeric features with median
    for col in NUMERIC_FEATURES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    # Winsorize target at 99th percentile
    p99 = df[TARGET].quantile(0.99)
    n_capped = (df[TARGET] > p99).sum()
    df[TARGET] = df[TARGET].clip(upper=p99)
    print(f"  Winsorized {n_capped} rows at p99 = {p99:.2f}")

    return df


def encode_categoricals(df):
    """Label-encode categorical features and save encoders."""
    ENCODERS.mkdir(parents=True, exist_ok=True)
    encoders = {}

    for col in CATEGORICAL_FEATURES:
        if col not in df.columns:
            continue

        le = LabelEncoder()
        df[col + "_encoded"] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    joblib.dump(encoders, ENCODERS / "label_encoders.pkl")
    print(f"  Saved {len(encoders)} label encoders")

    return df


def scale_numerics(X_train, X_test):
    """Standardize numeric features."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, ENCODERS / "scaler.pkl")
    return X_train_scaled, X_test_scaled


def build():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    print(f"Loading {INPUT}")
    df = pd.read_parquet(INPUT)
    print(f"  Shape: {df.shape}")

    df = clean_features(df)
    df = encode_categoricals(df)

    # Assemble final feature matrix
    feature_cols = (
        [c + "_encoded" for c in CATEGORICAL_FEATURES if c in df.columns]
        + [c for c in BINARY_FEATURES if c in df.columns]
        + [c for c in NUMERIC_FEATURES if c in df.columns]
    )
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols].copy()
    y = df[TARGET].copy()

    # Log-transform target
    y_log = np.log1p(y)
    print(f"  Log-transformed target")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_log, test_size=0.2, random_state=42
    )
    print(f"  Train: {X_train.shape}, Test: {X_test.shape}")

    # Save processed datasets
    X_train.to_parquet(PROCESSED / "X_train.parquet", index=False)
    X_test.to_parquet(PROCESSED / "X_test.parquet", index=False)
    y_train.to_frame().to_parquet(PROCESSED / "y_train.parquet", index=False)
    y_test.to_frame().to_parquet(PROCESSED / "y_test.parquet", index=False)

    # Save feature column list
    with open(PROCESSED / "feature_columns.json", "w") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"\n[OK] Features saved to {PROCESSED}")
    print(f"     {len(feature_cols)} features")
    print(f"     {len(X_train)} train rows, {len(X_test)} test rows")


if __name__ == "__main__":
    build()