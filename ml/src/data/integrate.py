"""
Integrate cleaned SAS files into one dataset per season.

Merges:
  - Production (main)
  - Screening (plot info)
  - Practices (agricultural practices)
  - Fertilizer (inputs)

Usage:
    python -m ml.src.data.integrate
"""
from pathlib import Path
import pandas as pd


INTERIM_DIR = Path("data/interim")
PROCESSED_DIR = Path("data/processed")


def load_season(suffix):
    """Load all four cleaned files for a given season."""
    files = {
        "production": INTERIM_DIR / f"production_{suffix}.parquet",
        "practices":  INTERIM_DIR / f"practices_{suffix}.parquet",
        "screening":  INTERIM_DIR / f"screening_{suffix}.parquet",
        "fertilizer": INTERIM_DIR / f"fertilizer_{suffix}.parquet",
    }

    data = {}
    for key, path in files.items():
        if path.exists():
            data[key] = pd.read_parquet(path)
            print(f"  Loaded {key}_{suffix}: {data[key].shape}")
        else:
            print(f"  WARNING: Missing: {path}")
            data[key] = pd.DataFrame()
    return data


def integrate_season(season, suffix):
    """Integrate all files for one season."""
    print(f"\nIntegrating Season {season}...")
    data = load_season(suffix)

    prod = data["production"]
    if prod.empty:
        print(f"  ERROR: No production data — skipping Season {season}")
        return None

    prod = prod.copy()
    prod["season"] = season

    # Merge screening (plot-level info)
    scr = data["screening"]
    if not scr.empty:
        scr_cols = [
            "segment_id", "plot_number",
            "plot_area_ha", "cropping_system", "num_main_crops",
        ]
        scr_cols = [c for c in scr_cols if c in scr.columns]
        scr = scr[scr_cols].drop_duplicates(subset=["segment_id", "plot_number"])
        prod = prod.merge(
            scr, on=["segment_id", "plot_number"], how="left",
            suffixes=("", "_scr"),
        )
        print(f"  Merged screening: {prod.shape}")

    # Merge practices
    pract = data["practices"]
    if not pract.empty:
        pract_cols = [
            "segment_id", "plot_number",
            "irrigation_practiced", "plot_irrigated",
            "irrigation_technique", "irrigation_source", "irrigation_tool",
        ]
        pract_cols = [c for c in pract_cols if c in pract.columns]
        pract = pract[pract_cols].drop_duplicates(
            subset=["segment_id", "plot_number"]
        )
        prod = prod.merge(
            pract, on=["segment_id", "plot_number"], how="left",
            suffixes=("", "_prac"),
        )
        print(f"  Merged practices: {prod.shape}")

    # Merge fertilizer
    fert = data["fertilizer"]
    if not fert.empty:
        fert_cols = [
            "segment_id", "plot_number",
            "organic_fertilizer_used", "organic_fertilizer_type_1",
            "inorganic_fertilizer_used", "inorganic_fertilizer_type_1",
            "inorganic_fertilizer_quantity_1",
            "pesticide_type_1", "pesticide_quantity_1",
        ]
        fert_cols = [c for c in fert_cols if c in fert.columns]
        fert = fert[fert_cols].drop_duplicates(
            subset=["segment_id", "plot_number"]
        )
        prod = prod.merge(
            fert, on=["segment_id", "plot_number"], how="left",
            suffixes=("", "_fert"),
        )
        print(f"  Merged fertilizer: {prod.shape}")

    # Drop rows without yield
    if "yield_value" in prod.columns:
        before = len(prod)
        prod = prod.dropna(subset=["yield_value"])
        after = len(prod)
        print(f"  Dropped {before - after} rows without yield → {after} rows remain")

    return prod


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    all_seasons = []
    for season, suffix in [("A", "a"), ("B", "b"), ("C", "c")]:
        df = integrate_season(season, suffix)
        if df is not None:
            all_seasons.append(df)

    if all_seasons:
        combined = pd.concat(all_seasons, ignore_index=True)
        out_path = PROCESSED_DIR / "sas_2025_integrated.parquet"
        combined.to_parquet(out_path, index=False)
        print(f"\nSaved integrated dataset: {out_path}")
        print(f"   Total rows: {len(combined)}")
        print(f"   Total columns: {len(combined.columns)}")
        print(f"\n   Column names:")
        for col in combined.columns:
            print(f"     {col}")


if __name__ == "__main__":
    main()