"""
Strip surrounding quotes from all string columns.
Fixes an issue where CSV was read with quoting=3, leaving literal quotes.

Usage:
    python -m ml.src.data.fix_quotes
"""
from pathlib import Path
import pandas as pd


def strip_quotes(val):
    """Remove surrounding double or single quotes."""
    if not isinstance(val, str):
        return val
    s = val.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def main():
    input_path = Path("data/processed/sas_2025_integrated.parquet")
    backup_path = Path("data/processed/sas_2025_integrated_backup.parquet")

    print(f"Loading {input_path}")
    df = pd.read_parquet(input_path)
    print(f"Shape: {df.shape}")

    # Backup
    print(f"Saving backup to {backup_path}")
    df.to_parquet(backup_path, index=False)

    # Strip quotes from all object columns
    fixed_cols = 0
    for col in df.columns:
        if df[col].dtype == "object":
            before = df[col].iloc[0] if len(df) > 0 else None
            df[col] = df[col].apply(strip_quotes)
            after = df[col].iloc[0] if len(df) > 0 else None
            if before != after:
                fixed_cols += 1
                print(f"  Fixed: {col}  ({repr(before)} -> {repr(after)})")

    print(f"\nFixed {fixed_cols} columns")

    # Save
    print(f"Saving to {input_path}")
    df.to_parquet(input_path, index=False)

    # Verify
    print("\n=== Sample after fix ===")
    print("District:", df['district'].head(5).tolist())
    print("Crop:", df['crop'].head(5).tolist())


if __name__ == "__main__":
    main()