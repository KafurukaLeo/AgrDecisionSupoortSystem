"""
Fast scanner for NISR SAS 2025 files.
Reads header + counts rows WITHOUT loading into Pandas.

Usage:
    python -m ml.src.data.quick_scan
"""
from pathlib import Path


DATA_ROOT = Path("data/raw/sas_2025")

FILES = [
    ("A", "production",  "season_a/Rwa_raw_SeasonA2025_Production.csv"),
    ("A", "practices",   "season_a/Rwa_raw_SeasonA2025_Agricultural_practice.csv"),
    ("A", "screening",   "season_a/Rwa_raw_SeasonA2025_Screening.csv"),
    ("A", "fertilizer",  "season_a/Rwa_raw_fertilizer_pesticideA2025.csv"),
    ("B", "production",  "season_b/Rwa_raw_SeasonB2025_Production.csv"),
    ("B", "practices",   "season_b/Rwa_raw_SeasonB2025_Agricultural_practice.csv"),
    ("B", "screening",   "season_b/Rwa_raw_SeasonB2025_Screening.csv"),
    ("B", "fertilizer",  "season_b/Rwa_raw_fertilizer_pesticideB2025.csv"),
    ("C", "production",  "season_c/Rwa_raw_SeasonC2025_Production.csv"),
    ("C", "practices",   "season_c/Rwa_raw_SeasonC2025_Agricultural_practice.csv"),
    ("C", "screening",   "season_c/Rwa_raw_SeasonC2025_Screening.csv"),
    ("C", "fertilizer",  "season_c/Rwa_raw_fertilizer_pesticideC2025.csv"),
]


def scan(path: Path):
    """Read header, count lines, return (rows, cols, header_list)."""
    if not path.exists():
        return None

    with open(path, encoding="utf-8", errors="ignore") as f:
        header_line = f.readline().rstrip("\n")
        cols = header_line.split("\t")

        # Count remaining lines
        rows = 0
        for _ in f:
            rows += 1

    return rows, len(cols), cols


def main():
    print(f"{'Season':<8}{'File':<12}{'Rows':>8}{'Cols':>8}")
    print("-" * 40)

    all_results = {}

    for season, label, rel_path in FILES:
        full = DATA_ROOT / rel_path
        result = scan(full)

        if result is None:
            print(f"{season:<8}{label:<12}{'MISSING':>8}")
            continue

        rows, cols, header = result
        print(f"{season:<8}{label:<12}{rows:>8}{cols:>8}")
        all_results[(season, label)] = header

    # Save all headers to a text file
    out_path = Path("ml/artifacts/headers.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for (season, label), header in all_results.items():
            f.write(f"\n{'=' * 70}\n")
            f.write(f"Season {season} / {label}\n")
            f.write(f"{'=' * 70}\n")
            f.write("\t".join(header) + "\n")

    print(f"\nAll headers saved to: {out_path}")


if __name__ == "__main__":
    main()