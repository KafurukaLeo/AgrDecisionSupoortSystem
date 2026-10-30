"""
Inspect NISR SAS 2025 files.

Verified against actual NISR SAS 2025 filenames (Nov 2025 release).

Usage:
    python -m ml.src.data.inspect
    python -m ml.src.data.inspect > ml/artifacts/inspection_report.txt 2>&1
"""
from pathlib import Path
import pandas as pd


DATA_ROOT = Path("data/raw/sas_2025")
OUTPUT_DIR = Path("ml/artifacts")


FILES = {
    "Season A": {
        "production": "season_a/Rwa_raw_SeasonA2025_Production.csv",
        "practices":  "season_a/Rwa_raw_SeasonA2025_Agricultural_practice.csv",
        "screening":  "season_a/Rwa_raw_SeasonA2025_Screening.csv",
        "fertilizer": "season_a/Rwa_raw_fertilizer_pesticideA2025.csv",
    },
    "Season B": {
        "production": "season_b/Rwa_raw_SeasonB2025_Production.csv",
        "practices":  "season_b/Rwa_raw_SeasonB2025_Agricultural_practice.csv",
        "screening":  "season_b/Rwa_raw_SeasonB2025_Screening.csv",
        "fertilizer": "season_b/Rwa_raw_fertilizer_pesticideB2025.csv",
    },
    "Season C": {
        "production": "season_c/Rwa_raw_SeasonC2025_Production.csv",
        "practices":  "season_c/Rwa_raw_SeasonC2025_Agricultural_practice.csv",
        "screening":  "season_c/Rwa_raw_SeasonC2025_Screening.csv",
        "fertilizer": "season_c/Rwa_raw_fertilizer_pesticideC2025.csv",
    },
}


def inspect_file(filepath: Path, label: str):
    print("=" * 78)
    print(f"File: {label}")
    print(f"Path: {filepath}")
    print("=" * 78)

    if not filepath.exists():
        print(f"WARNING: FILE NOT FOUND\n")
        return None

    try:
        df = pd.read_csv(filepath, sep="\t", low_memory=False)
    except Exception as e:
        print(f"WARNING: Could not read file: {e}\n")
        return None

    print(f"Shape: {df.shape}")

    # Column summary
    print(f"\nColumns ({len(df.columns)}):")
    for col in df.columns:
        non_null = df[col].notna().sum()
        dtype = str(df[col].dtype)
        print(f"  {col:<30} {dtype:<10} non-null: {non_null}")

    # Show first 3 rows (truncated to fit terminal)
    print(f"\nFirst 3 rows (first 12 cols):")
    print(df.iloc[:3, :12].to_string())
    print()

    return df


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows = []

    for season, files in FILES.items():
        print(f"\n{'#' * 78}")
        print(f"# {season}")
        print(f"{'#' * 78}\n")

        for label, rel_path in files.items():
            full_path = DATA_ROOT / rel_path
            df = inspect_file(full_path, f"{season} / {label}")

            if df is not None:
                summary_rows.append({
                    "season": season,
                    "file_type": label,
                    "path": str(full_path),
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                })
            else:
                summary_rows.append({
                    "season": season,
                    "file_type": label,
                    "path": str(full_path),
                    "rows": 0,
                    "columns": 0,
                })

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    summary = pd.DataFrame(summary_rows)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()