"""
Train ML models on NISR SAS 2025 data.

Trains Linear Regression, Random Forest, and Gradient Boosting.
Saves best model to artifacts.

Usage:
    python -m ml.src.models.train
"""
from pathlib import Path
import json
import time

import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


PROCESSED = Path("ml/artifacts/processed")
MODELS_DIR = Path("ml/artifacts/models")
METRICS_DIR = Path("ml/artifacts/metrics")


def load_data():
    X_train = pd.read_parquet(PROCESSED / "X_train.parquet")
    X_test = pd.read_parquet(PROCESSED / "X_test.parquet")
    y_train = pd.read_parquet(PROCESSED / "y_train.parquet").iloc[:, 0]
    y_test = pd.read_parquet(PROCESSED / "y_test.parquet").iloc[:, 0]
    return X_train, X_test, y_train, y_test


def evaluate(model, X_test, y_test, name):
    """Evaluate a trained model and return metrics dict."""
    pred_log = model.predict(X_test)
    y_true = np.expm1(y_test)     # inverse log transform
    y_pred = np.expm1(pred_log)

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    return {
        "model": name,
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
    }


def main():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading processed data...")
    X_train, X_test, y_train, y_test = load_data()
    print(f"  Train: {X_train.shape}")
    print(f"  Test:  {X_test.shape}")

    models = {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_leaf=5,
            n_jobs=-1,
            random_state=42,
        ),
        "gradient_boosting": GradientBoostingRegressor(
            n_estimators=150,
            max_depth=5,
            learning_rate=0.05,
            random_state=42,
        ),
    }

    results = []
    best_model = None
    best_rmse = float("inf")
    best_name = None

    for name, model in models.items():
        print(f"\nTraining {name}...")
        start = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - start

        metrics = evaluate(model, X_test, y_test, name)
        metrics["train_time_sec"] = round(train_time, 2)
        results.append(metrics)

        print(f"  MAE:  {metrics['mae']:.2f}")
        print(f"  RMSE: {metrics['rmse']:.2f}")
        print(f"  R2:   {metrics['r2']:.4f}")
        print(f"  Time: {train_time:.2f}s")

        if metrics["rmse"] < best_rmse:
            best_rmse = metrics["rmse"]
            best_model = model
            best_name = name

    # Save all metrics
    metrics_path = METRICS_DIR / "model_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Metrics saved to {metrics_path}")

    # Save best model
    model_path = MODELS_DIR / f"best_model_{best_name}.pkl"
    joblib.dump(best_model, model_path)
    print(f"[OK] Best model: {best_name}")
    print(f"[OK] Saved to: {model_path}")

    # Save marker file for loader
    with open(MODELS_DIR / "best_model.txt", "w") as f:
        f.write(best_name)

    # Feature importance for tree models
    if hasattr(best_model, "feature_importances_"):
        fi = pd.DataFrame({
            "feature": X_train.columns,
            "importance": best_model.feature_importances_,
        }).sort_values("importance", ascending=False)
        fi_path = METRICS_DIR / "feature_importance.csv"
        fi.to_csv(fi_path, index=False)
        print(f"[OK] Feature importance saved to {fi_path}")
        print("\nTop 10 features:")
        print(fi.head(10).to_string(index=False))


if __name__ == "__main__":
    main()