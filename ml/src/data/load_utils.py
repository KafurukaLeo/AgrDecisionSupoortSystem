"""
Safe file loading utilities for NISR SAS 2025 data.

Handles:
- Tab-separated files
- Malformed rows (unterminated quotes, stray tabs)
- Mixed data types
- Missing values

Usage:
    from ml.src.data.load_utils import load_sas_csv
    df = load_sas_csv("path/to/file.csv")
"""
from pathlib import Path
import pandas as pd


def load_sas_csv(path, nrows=None):
    """
    Safely load a NISR SAS CSV file (tab-separated).

    Parameters
    ----------
    path : str or Path
        Full path to the CSV file.
    nrows : int, optional
        Limit number of rows (for quick testing).

    Returns
    -------
    pd.DataFrame
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(
        path,
        sep="\t",
        dtype=str,               
        quoting=3,              
        on_bad_lines="skip",     
        nrows=nrows,
        encoding="utf-8",
        engine="python",         
    )

    df.columns = df.columns.str.strip()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

    return df


def to_numeric_safe(series):
    """Convert a series to numeric, coercing errors to NaN."""
    return pd.to_numeric(series, errors="coerce")


def summary(df, label=""):
    """Print a quick summary of a DataFrame."""
    print(f"--- {label} ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)[:10]}{'...' if len(df.columns) > 10 else ''}")
    print()