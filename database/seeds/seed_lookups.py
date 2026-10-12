"""
Seed lookup tables with initial values.

Run from the project root:
    python -m database.seeds.seed_lookups
"""
from backend.app.core.database import SessionLocal
from backend.app.models import Crop, Season, Province, District


CROPS = [
    {"name": "Maize", "category": "Cereal"},
    {"name": "Rice", "category": "Cereal"},
    {"name": "Sorghum", "category": "Cereal"},
    {"name": "Beans", "category": "Legume"},
    {"name": "Groundnuts", "category": "Legume"},
    {"name": "Soybeans", "category": "Legume"},
    {"name": "Irish Potatoes", "category": "Tuber"},
    {"name": "Sweet Potatoes", "category": "Tuber"},
    {"name": "Cassava", "category": "Tuber"},
    {"name": "Bananas", "category": "Fruit"},
    {"name": "Plantain", "category": "Fruit"},
    {"name": "Vegetables", "category": "Vegetable"},
]

PROVINCES = [
    {"name": "Kigali", "districts": ["Gasabo", "Kicukiro", "Nyarugenge"]},
    {"name": "Northern", "districts": ["Burera", "Gakenke", "Gicumbi", "Musanze", "Rulindo"]},
    {"name": "Southern", "districts": [
        "Gisagara", "Huye", "Kamonyi", "Muhanga",
        "Nyamagabe", "Nyanza", "Nyaruguru", "Ruhango",
    ]},
    {"name": "Eastern", "districts": [
        "Bugesera", "Gatsibo", "Kayonza", "Kirehe",
        "Ngoma", "Nyagatare", "Rwamagana",
    ]},
    {"name": "Western", "districts": [
        "Karongi", "Ngororero", "Nyabihu", "Nyamasheke",
        "Rubavu", "Rusizi", "Rutsiro",
    ]},
]

SEASONS = [
    {"code": "A", "description": "Season A (September - January)", "year": 2024},
    {"code": "B", "description": "Season B (February - June)", "year": 2024},
    {"code": "C", "description": "Season C (July - September)", "year": 2024},
    {"code": "A", "description": "Season A (September - January)", "year": 2025},
    {"code": "B", "description": "Season B (February - June)", "year": 2025},
    {"code": "C", "description": "Season C (July - September)", "year": 2025},
]


def seed_crops(db):
    added = 0
    for c in CROPS:
        if not db.query(Crop).filter_by(name=c["name"]).first():
            db.add(Crop(**c))
            added += 1
    db.commit()
    print(f"Crops: {added} added")


def seed_provinces_and_districts(db):
    provinces_added = 0
    districts_added = 0

    for p in PROVINCES:
        province = db.query(Province).filter_by(name=p["name"]).first()
        if not province:
            province = Province(name=p["name"])
            db.add(province)
            db.commit()
            db.refresh(province)
            provinces_added += 1

        for d_name in p["districts"]:
            exists = (
                db.query(District)
                .filter_by(name=d_name, province_id=province.id)
                .first()
            )
            if not exists:
                db.add(District(name=d_name, province_id=province.id))
                districts_added += 1
        db.commit()

    print(f"Provinces: {provinces_added} added")
    print(f"Districts: {districts_added} added")


def seed_seasons(db):
    added = 0
    for s in SEASONS:
        exists = (
            db.query(Season)
            .filter_by(code=s["code"], year=s["year"])
            .first()
        )
        if not exists:
            db.add(Season(**s))
            added += 1
            db.commit()   # commit one by one for safety

    print(f"Seasons: {added} added")


def seed():
    print("Seeding lookup tables...")
    db = SessionLocal()
    try:
        seed_crops(db)
        seed_provinces_and_districts(db)
        seed_seasons(db)
        print("Done.")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()