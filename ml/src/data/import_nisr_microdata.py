"""Import and stage NISR microdata files for AgrDecisionSupportSystem.

This utility helps with the official NISR archive workflow:
1. Download the study files from the NISR microdata catalog after creating an account.
2. Place the files in a local folder.
3. Run this script to stage/copy them into the repo's expected raw-data layout.
4. Use the existing inspection and cleaning pipeline in ml/src/data/.

The project's downstream pipeline expects files in a structure like:
    data/raw/sas_2025/season_a/Rwa_raw_SeasonA2025_Production.csv
    data/raw/sas_2025/season_b/Rwa_raw_SeasonB2025_Agricultural_practice.csv
    ...

This script is intentionally tolerant: it works with downloaded ZIPs, CSV/TSV files,
and folders that already contain one or more NISR survey extracts.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path[:] = [p for p in sys.path if p not in ("", str(SCRIPT_DIR), str(SCRIPT_DIR.resolve()))]
sys.path.insert(0, str(REPO_ROOT))

import pandas as pd

from ml.src.data.load_utils import load_sas_csv


DEFAULT_RAW_ROOT = Path("data/raw/nisr")
DEFAULT_INTERIM_ROOT = Path("data/interim")

FILE_HINTS = {
    "production": {"production", "prod", "yield", "harvest"},
    "practices": {"practice", "practices", "agricultural_practice"},
    "screening": {"screening", "household", "listing"},
    "fertilizer": {"fertilizer", "pesticide", "input"},
}


def normalize_name(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def infer_role(path: Path) -> str:
    text = normalize_name(path.name)
    for role, hints in FILE_HINTS.items():
        if any(hint in text for hint in hints):
            return role
    return "unknown"


def extract_archives(source: Path, destination: Path) -> list[Path]:
    """Extract ZIP archives and return the extracted files."""
    extracted: list[Path] = []
    if source.is_file() and source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as zf:
            zf.extractall(destination)
        extracted.extend(sorted(destination.rglob("*")))
    return extracted


def discover_files(root: Path) -> list[Path]:
    """Return likely microdata files under a directory tree."""
    patterns = ("*.csv", "*.tsv", "*.txt", "*.dta", "*.sav", "*.xlsx", "*.xls")
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(root.rglob(pattern))
    unique = []
    seen = set()
    for path in matches:
        key = str(path.resolve())
        if key not in seen:
            unique.append(path)
            seen.add(key)
    return sorted(unique)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def stage_files(source: Path, raw_root: Path = DEFAULT_RAW_ROOT, year: str | None = None) -> list[Path]:
    """Stage files into a project-friendly raw structure.

    Example output layout:
        data/raw/nisr/2024/season_a/production.csv
        data/raw/nisr/2024/season_a/practices.csv
    """
    if year is None:
        year = "2024"

    with_paths: list[Path] = []

    if source.is_file() and source.suffix.lower() == ".zip":
        extract_dir = raw_root / year / "incoming"
        extract_archives(source, extract_dir)
        sources = discover_files(extract_dir)
    elif source.is_dir():
        sources = discover_files(source)
    else:
        sources = [source]

    if not sources:
        raise FileNotFoundError(f"No microdata files found under '{source}'")

    for path in sources:
        role = infer_role(path)
        season = "season_unknown"
        lower = path.name.lower()
        if "season_a" in lower or "seasona" in lower:
            season = "season_a"
        elif "season_b" in lower or "seasonb" in lower:
            season = "season_b"
        elif "season_c" in lower or "seasonc" in lower:
            season = "season_c"

        target = raw_root / year / season / role / path.name
        copy_file(path, target)
        with_paths.append(target)

    return with_paths


def validate_file(path: Path) -> dict:
    """Open a file and print a brief validation summary for the user."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    try:
        if path.suffix.lower() in {".csv", ".tsv", ".txt"}:
            df = load_sas_csv(path)
        elif path.suffix.lower() == ".dta":
            df = pd.read_stata(path)
        elif path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path, sep=None, engine="python")
    except Exception as exc:  # pragma: no cover - user may supply non-standard files
        return {"path": str(path), "status": "failed", "message": str(exc)}

    return {
        "path": str(path),
        "status": "ok",
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "preview_columns": list(df.columns[:10]),
    }


def write_manifest(staged: Iterable[Path], manifest_path: Path) -> None:
    payload = []
    for path in staged:
        payload.append({
            "path": str(path),
            "role": infer_role(path),
            "exists": path.exists(),
        })
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage official NISR microdata for the AgrDecisionSupportSystem pipeline.")
    parser.add_argument(
        "--source",
        required=True,
        help="Path to a microdata ZIP, CSV/TSV folder, or a single microdata file.",
    )
    parser.add_argument(
        "--year",
        default="2024",
        help="Survey year to attach to staged files (default: 2024).",
    )
    parser.add_argument(
        "--raw-root",
        default=str(DEFAULT_RAW_ROOT),
        help="Where staged/raw files should be copied (default: data/raw/nisr).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    raw_root = Path(args.raw_root).expanduser().resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source path does not exist: {source}")

    staged = stage_files(source, raw_root=raw_root, year=args.year)
    manifest_path = raw_root / args.year / "manifest.json"
    write_manifest(staged, manifest_path)

    print("\nStaged files:")
    for path in staged:
        details = validate_file(path)
        print(f"- {path}")
        print(f"  {details}")

    print("\nManifest saved to:")
    print(f"  {manifest_path}")

    print("\nNext steps in this project:")
    print("  1. Open the files you staged and confirm they match the official NISR SAS layout.")
    print("  2. Run: python -m ml.src.data.inspect")
    print("  3. Run: python -m ml.src.data.clean")
    print("  4. If the dataset is 2024/2025 multi-season, keep the season_a / season_b / season_c structure.")
    print("\nImportant: the official microdata catalog requires login/registration before download.")
    print("Catalog: https://microdata.statistics.gov.rw/index.php")


if __name__ == "__main__":
    main()
