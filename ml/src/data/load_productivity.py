import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
Load integrated SAS data into PostgreSQL.

Reads: data/processed/sas_2025_integrated.parquet
Writes: crops (auto-created), productivity_records

Usage:
    python -m ml.src.data.load_productivity
"""
from pathlib import Path
import pandas as pd

from backend.app.core.database import SessionLocal
from backend.app.models import Crop, Season, Province, District, ProductivityRecord


INPUT = Path("data/processed/sas_2025_integrated.parquet")


def _safe_float(val):
    if pd.isna(val):
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def to_bool_str(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return "yes" if int(value) == 1 else "no"
    v = str(value).strip().lower()
    if v in ("1", "1.0", "yes", "true"):
        return "yes"
    if v in ("0", "0.0", "no", "false"):
        return "no"
    return None


def get_crop_category(crop_name):
    """Infer category from crop name."""
    name = str(crop_name).lower()
    if any(k in name for k in ["maize", "rice", "sorghum", "wheat", "millet", "cereal"]):
        return "Cereal"
    if any(k in name for k in ["bean", "pea", "groundnut", "soybean", "pulse"]):
        return "Legume"
    if any(k in name for k in ["potato", "cassava", "taro", "yam", "tuber", "beet"]):
        return "Tuber"
    if any(k in name for k in ["tomato", "cabbage", "onion", "carrot", "eggplant",
                                "pepper", "spinach", "lettuce", "broccoli",
                                "cucumber", "garlic", "leek", "celery", "amaranth",
                                "vegetable"]):
        return "Vegetable"
    if any(k in name for k in ["banana", "mango", "papaya", "avocado", "orange",
                                "lemon", "guava", "pineapple", "passion", "fruit",
                                "strawberry", "jack"]):
        return "Fruit"
    if any(k in name for k in ["coffee", "tea", "macadamia", "mulberry", "stevia",
                                "perennial", "jatropha"]):
        return "Perennial"
    if any(k in name for k in ["fodder", "napia", "leucena", "desmodium", "mucuna",
                                "setaria", "tripsacum", "herbaceous"]):
        return "Fodder"
    return "Other"


def get_or_create_crop(db, crop_cache, name):
    """Get crop ID or create if missing."""
    key = name.strip().lower()
    if key in crop_cache:
        return crop_cache[key]

    category = get_crop_category(name)
    c = Crop(name=name.strip(), category=category)
    db.add(c)
    db.commit()
    db.refresh(c)
    crop_cache[key] = c.id
    return c.id


def load():
    print(f"Loading {INPUT}")
    df = pd.read_parquet(INPUT)
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

    db = SessionLocal()

    crops = {c.name.lower(): c.id for c in db.query(Crop).all()}
    districts = {d.name.lower(): d.id for d in db.query(District).all()}
    seasons = {(s.code, s.year): s.id for s in db.query(Season).all()}

    print(f"Existing lookups — crops: {len(crops)}, districts: {len(districts)}, seasons: {len(seasons)}")
    print(f"Will auto-create missing crops as they appear.\n")

    inserted = 0
    skipped = 0
    crops_created = 0
    skip_reasons = {"no_crop": 0, "no_district": 0, "no_season": 0, "no_yield": 0, "error": 0}

    for idx, row in df.iterrows():
        try:
            crop_raw = row.get("crop")
            if pd.isna(crop_raw) or str(crop_raw).strip() == "":
                skip_reasons["no_crop"] += 1
                skipped += 1
                continue

            crop_name = str(crop_raw).strip()
            crop_key = crop_name.lower()

            if crop_key not in crops:
                crop_id = get_or_create_crop(db, crops, crop_name)
                crops_created += 1
            else:
                crop_id = crops[crop_key]

            season_code = str(row.get("season", "")).strip().upper()
            season_id = seasons.get((season_code, 2025))
            if not season_id:
                skip_reasons["no_season"] += 1
                skipped += 1
                continue

            district_name = str(row.get("district", "")).strip().lower()
            district_id = districts.get(district_name)
            if not district_id:
                skip_reasons["no_district"] += 1
                skipped += 1
                continue

            yield_val = _safe_float(row.get("yield_value"))
            if yield_val is None:
                skip_reasons["no_yield"] += 1
                skipped += 1
                continue

            crop_area = _safe_float(row.get("crop_area_ha"))
            production_val = yield_val * crop_area if crop_area else None

            fertilizer = to_bool_str(row.get("organic_fertilizer_used")) or \
                         to_bool_str(row.get("inorganic_fertilizer_used"))
            irrigation = to_bool_str(row.get("irrigation_practiced")) or \
                         to_bool_str(row.get("irrigation_used"))
            seeds = to_bool_str(row.get("seeds_used"))
            pesticide = to_bool_str(row.get("pesticide_used"))

            record = ProductivityRecord(
                crop_id=crop_id,
                season_id=season_id,
                district_id=district_id,
                cultivated_area=crop_area,
                production=production_val,
                yield_value=yield_val,
                fertilizer_used=fertilizer,
                irrigation_used=irrigation,
                improved_seeds_used=seeds,
                pesticide_used=pesticide,
            )
            db.add(record)
            inserted += 1

            if inserted % 5000 == 0:
                db.commit()
                print(f"  Inserted {inserted} records... (crops created: {crops_created})")

        except Exception as e:
            skipped += 1
            skip_reasons["error"] += 1
            if skip_reasons["error"] <= 5:
                print(f"  Row {idx} error: {e}")

    db.commit()
    print(f"\n[OK] Inserted: {inserted}")
    print(f"   Skipped: {skipped}")
    print(f"   Crops auto-created: {crops_created}")
    print(f"   Skip reasons: {skip_reasons}")
    db.close()


if __name__ == "__main__":
    load()