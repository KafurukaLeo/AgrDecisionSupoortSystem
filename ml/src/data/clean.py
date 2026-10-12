"""
Clean NISR SAS 2025 files.

Renames NISR columns to human-readable names,
decodes codes, and handles missing values.

Usage:
    python -m ml.src.data.clean
"""
from pathlib import Path
import pandas as pd

from ml.src.data.load_utils import load_sas_csv, to_numeric_safe


DATA_ROOT = Path("data/raw/sas_2025")
OUTPUT_DIR = Path("data/interim")


# -----------------------------------------------------------------------------
# Column mappings — from NISR code to our pipeline name
# -----------------------------------------------------------------------------

COMMON_COLS = {
    "Segment_ID": "segment_id",
    "s1q1":       "province",
    "s1q2":       "district",
    "s1q3":       "stratum",
    "s1q6":       "farmer_category",
    "s1q7":       "farmer_type",
    "s1q8":       "farmer_gender",
    "s1q9":       "farmer_age",
    "s2q1":       "plot_number",
    "plot_weight": "survey_weight",
    "Plot_weight": "survey_weight",
}


PRODUCTION_RENAME = {
    **COMMON_COLS,
    "s2q3":                    "grid_points_count",
    "s2q4":                    "crop",
    "CropCategory":            "crop_category",
    "s2q4_o":                  "crop_other",
    "s2q7":                    "land_use",
    "s3q1":                    "crop_grown_flag",
    "s3q3":                    "seed_type",
    "s3q7":                    "seeds_used",
    "s3q9":                    "organic_matter_used",
    "s3q16":                   "organic_fertilizer_used",
    "s3q17":                   "inorganic_fertilizer_other",
    "s3q18":                   "pesticide_used",
    "s3q19":                   "irrigation_used",
    "s4q1":                    "erosion_degree",
    "s4q2":                    "anti_erosion_activity",
    "s4q3":                    "anti_erosion_this_plot",
    "s4q4":                    "anti_erosion_this_season",
    "s4q6":                    "consolidated_site",
    "s4q8":                    "equipment_used",
    "s4q9":                    "mechanical_equipment_used",
    "s4q13":                   "irrigation_practiced",
    "s4q14":                   "plot_irrigated",
    "Plot_area_ha":            "plot_area_ha",
    "Harvest_ratio":           "harvest_ratio",
    "Crop_Area_ha":            "crop_area_ha",
    "Harvested_Crop_Area_ha":  "harvested_crop_area_ha",
    "Yield":                   "yield_value",
}


PRACTICES_RENAME = {
    **COMMON_COLS,
    "s2q2_ha":          "plot_area_ha",
    "s2q2":             "plot_area_ha",
    "s4q1":             "erosion_degree",
    "s4q2":             "anti_erosion_activity",
    "s4q3":             "anti_erosion_this_plot",
    "s4q4":             "anti_erosion_this_season",
    "s4q6":             "consolidated_site",
    "s4q7":             "agroforestry_trees",
    "s4q8":             "equipment_used",
    "s4q9":             "mechanical_equipment_used",
    "s4q13":            "irrigation_practiced",
    "s4q14":            "plot_irrigated",
    "s4q15":            "irrigation_technique",
    "s4q16":            "irrigation_source",
    "s4q17":            "irrigation_tool",
    "s4q18":            "irrigation_cost",
    "Plot_size_ha":     "plot_area_ha",
    "crop_area":        "crop_area_ha",
}


SCREENING_RENAME = {
    **COMMON_COLS,
    "s1q4":              "farmer_id",
    "s1q5_2":            "farmer_id_number",
    "s1q5_3":            "farmer_type_long",
    "s2q2":              "plot_number_2",
    "s2q4":              "land_use",
    "s2q5_bloc":         "block_area",
    "s2q5":              "plot_area_m2",
    "s2q7":              "land_use_detail",
    "s2q9":              "erosion_degree",
    "s2q13":             "fruit_trees_present",
    "s2q14":             "semi_arid_flag",
    "s2q15":             "cropping_system",
    "s2q16":             "num_main_crops",
    "s3q1":              "crop",
    "s3q1_o":            "crop_other",
    "CropCategory":      "crop_category",
    "s3q2_1":            "crop_code_1",
    "s3q2_2":            "crop_proportion",
    "s3q3_1":            "crop_density",
    "s3q3_2":            "crop_density_code",
    "s3q4":              "crop_rank",
    "s3q5":              "planted_this_season",
    "s3q6":              "harvest_expected",
    "s3q7":              "expected_harvest_period",
    "Plot_size_ha":      "plot_area_ha",
    "crop_area":         "crop_area_ha",
}


FERTILIZER_RENAME = {
    **COMMON_COLS,
    "s2q2":       "plot_area_m2",
    "s3q1":       "crop_grown_flag",
    "s3q2b":      "crop",
    "s3q2b_Other": "crop_other",
    "s3q3":       "plot_area_m2_detail",
    "s3q5":       "seed_source",
    "s3q6_1":     "organic_fertilizer_type_1",
    "s3q6_2":     "organic_fertilizer_type_2",
    "s3q7":       "organic_fertilizer_used",
    "s3q8":       "organic_fertilizer_source",
    "s3q9":       "organic_fertilizer_quantity",
    "s3q16":      "inorganic_fertilizer_used",
    "s3q18":      "irrigation_used",
    "s3q19":      "anti_erosion_used",
    "s3q201":     "inorganic_fertilizer_type_1",
    "s3q211":     "inorganic_fertilizer_quantity_1",
    "s3q221":     "inorganic_fertilizer_cost_1",
    "s3q231":     "inorganic_fertilizer_source_1",
    "s3q241":     "inorganic_fertilizer_other_1",
    "s3q101":     "pesticide_type_1",
    "s3q111":     "pesticide_quantity_1",
    "s3q121":     "pesticide_cost_1",
    "s3q131":     "pesticide_source_1",
    "s3q141":     "pesticide_other_1",
    "s3q151":     "pesticide_crop_1",
}


# -----------------------------------------------------------------------------
# Yes/No standardization
# -----------------------------------------------------------------------------

YES_NO_COLS = [
    "crop_grown_flag", "seeds_used", "organic_matter_used",
    "organic_fertilizer_used", "inorganic_fertilizer_used",
    "pesticide_used", "irrigation_used",
    "anti_erosion_activity", "anti_erosion_this_plot",
    "anti_erosion_this_season", "consolidated_site",
    "equipment_used", "mechanical_equipment_used",
    "irrigation_practiced", "plot_irrigated",
    "planted_this_season", "harvest_expected", "fruit_trees_present",
    "semi_arid_flag", "anti_erosion_used",
]


def standardize_yes_no(df):
    """Convert Yes/No columns to boolean (1/0)."""
    for col in df.columns:
        if col in YES_NO_COLS:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({"yes": 1, "no": 0})
            )
    return df


# -----------------------------------------------------------------------------
# Numeric conversion
# -----------------------------------------------------------------------------

NUMERIC_COLS = [
    "segment_id", "plot_number", "farmer_age", "grid_points_count",
    "plot_area_ha", "plot_area_m2", "crop_area_ha", "harvested_crop_area_ha",
    "harvest_ratio", "yield_value", "survey_weight",
    "num_main_crops", "crop_rank", "block_area",
]


def coerce_numeric(df):
    """Force numeric columns to numeric type."""
    for col in df.columns:
        if col in NUMERIC_COLS:
            df[col] = to_numeric_safe(df[col])
    return df


# -----------------------------------------------------------------------------
# Main cleaning function
# -----------------------------------------------------------------------------

def clean_file(path, rename_map, label):
    """Load, rename, standardize, and return cleaned DataFrame."""
    print(f"  Loading {label}: {path.name}")
    df = load_sas_csv(path)

    # Rename columns (only those present)
    rename_dict = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=rename_dict)

    # Standardize Yes/No
    df = standardize_yes_no(df)

    # Coerce numerics
    df = coerce_numeric(df)

    print(f"    → {df.shape[0]} rows × {df.shape[1]} cols after cleaning")
    return df


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    configs = [
        ("season_a/Rwa_raw_SeasonA2025_Production.csv",
         PRODUCTION_RENAME, "A / production", "production_a.parquet"),
        ("season_a/Rwa_raw_SeasonA2025_Agricultural_practice.csv",
         PRACTICES_RENAME, "A / practices", "practices_a.parquet"),
        ("season_a/Rwa_raw_SeasonA2025_Screening.csv",
         SCREENING_RENAME, "A / screening", "screening_a.parquet"),
        ("season_a/Rwa_raw_fertilizer_pesticideA2025.csv",
         FERTILIZER_RENAME, "A / fertilizer", "fertilizer_a.parquet"),

        ("season_b/Rwa_raw_SeasonB2025_Production.csv",
         PRODUCTION_RENAME, "B / production", "production_b.parquet"),
        ("season_b/Rwa_raw_SeasonB2025_Agricultural_practice.csv",
         PRACTICES_RENAME, "B / practices", "practices_b.parquet"),
        ("season_b/Rwa_raw_SeasonB2025_Screening.csv",
         SCREENING_RENAME, "B / screening", "screening_b.parquet"),
        ("season_b/Rwa_raw_fertilizer_pesticideB2025.csv",
         FERTILIZER_RENAME, "B / fertilizer", "fertilizer_b.parquet"),

        ("season_c/Rwa_raw_SeasonC2025_Production.csv",
         PRODUCTION_RENAME, "C / production", "production_c.parquet"),
        ("season_c/Rwa_raw_SeasonC2025_Agricultural_practice.csv",
         PRACTICES_RENAME, "C / practices", "practices_c.parquet"),
        ("season_c/Rwa_raw_SeasonC2025_Screening.csv",
         SCREENING_RENAME, "C / screening", "screening_c.parquet"),
        ("season_c/Rwa_raw_fertilizer_pesticideC2025.csv",
         FERTILIZER_RENAME, "C / fertilizer", "fertilizer_c.parquet"),
    ]

    print("=" * 60)
    print("Cleaning NISR SAS 2025 files")
    print("=" * 60)

    for rel_path, rename_map, label, out_name in configs:
        full_path = DATA_ROOT / rel_path
        try:
            df = clean_file(full_path, rename_map, label)
            out_path = OUTPUT_DIR / out_name
            df.to_parquet(out_path, index=False)
            print(f"    → Saved: {out_path}")
        except Exception as e:
            print(f"    ✗ Error cleaning {label}: {e}")
        print()

    print("=" * 60)
    print("Cleaning complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()