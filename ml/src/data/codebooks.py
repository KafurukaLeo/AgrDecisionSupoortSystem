"""
NISR SAS 2025 Codebooks

Source: Screening Questionnaire (SAS 2025) and Plot Questionnaire (SAS 2025)
All codes here are directly from the official NISR questionnaires.
"""

# -----------------------------------------------------------------------------
# GEOGRAPHY
# -----------------------------------------------------------------------------

PROVINCE_CODES = {
    1: "Kigali",
    2: "South",
    3: "West",
    4: "North",
    5: "East",
}

DISTRICT_CODES = {
    # Kigali
    11: "Nyarugenge",
    12: "Gasabo",
    13: "Kicukiro",
    # South
    21: "Nyanza",
    22: "Gisagara",
    23: "Nyaruguru",
    24: "Huye",
    25: "Nyamagabe",
    26: "Ruhango",
    27: "Muhanga",
    28: "Kamonyi",
    # West
    31: "Karongi",
    32: "Rutsiro",
    33: "Rubavu",
    34: "Nyabihu",
    35: "Ngororero",
    36: "Rusizi",
    37: "Nyamasheke",
    # North
    41: "Rulindo",
    42: "Gakenke",
    43: "Musanze",
    44: "Burera",
    45: "Gicumbi",
    # East
    51: "Rwamagana",
    52: "Nyagatare",
    53: "Gatsibo",
    54: "Kayonza",
    55: "Kirehe",
    56: "Ngoma",
    57: "Bugesera",
}

STRATUM_CODES = {
    10: "Agricultural land on hillside",
    20: "Agricultural land in marshland",
    30: "Rangeland",
    40: "Mixed",
    90: "Large Scale Farmer",
}

FARMER_CATEGORY_CODES = {
    1: "Individual LSF",
    2: "Cooperative/Company/Association LSF",
    3: "Small farmer",
}

# -----------------------------------------------------------------------------
# CROPS (from questionnaire page 11 and 14)
# -----------------------------------------------------------------------------

CROP_CODES = {
    # Seasonal crops
    101: "Maize",
    102: "Paddy rice",
    103: "Sorghum",
    104: "Wheat",
    105: "Other cereal",
    106: "Bush bean",
    107: "Climbing bean",
    108: "Pea",
    109: "Other pulse",
    110: "Irish potato",
    111: "Sweet potato",
    112: "Taro",
    113: "Yams",
    114: "Other tubers",
    115: "Tomato",
    116: "Cabbage",
    117: "Cauliflower",
    118: "Onion",
    119: "Carrot",
    120: "Eggplant",
    121: "Other seasonal vegetables",
    122: "Soybean",
    123: "Groundnut",
    124: "Sunflower",
    125: "Black eggplant",
    126: "Sweet pepper",
    127: "Amaranth",
    128: "Celery",
    129: "Spinach",
    130: "Small red bean",
    131: "Sugar beet",
    132: "Garlic",
    133: "African cabbage",
    134: "Leek",
    135: "French beans",
    136: "Lettuce",
    137: "Broccoli",
    138: "Millet",
    139: "Cucumber",
    140: "Chia seeds",
    141: "Other seasonal crop",
    # Annual crops
    201: "Pyrethrum",
    202: "Pepper",
    203: "Pumpkin",
    204: "Napia grass",
    205: "Sugar cane",
    206: "Tobacco",
    207: "Other annual crop",
    # Perennial crops
    300: "Banana",
    301: "Cooking banana",
    302: "Dessert banana",
    303: "Banana for beer",
    304: "Coffee",
    305: "Cassava",
    306: "Mulberry",
    307: "Jatropha",
    308: "Stevia",
    309: "Macadamia",
    310: "Tea",
    311: "Other perennial crop",
    # Fruit trees
    401: "Tree tomato",
    402: "Pineapple",
    403: "Avocado",
    404: "Passion fruit",
    405: "Palm",
    406: "Mango",
    407: "Apple",
    408: "Papaya",
    409: "Orange",
    410: "Lemon",
    411: "Guava",
    412: "Olive",
    413: "Watermelon",
    414: "Mandarin",
    415: "Jack fruit",
    416: "Gooseberry",
    417: "Strawberry",
    418: "Sugar apple",
    419: "Other fruit",
    # Fodder crops
    501: "Napia grass for fodder",
    502: "Maize for fodder",
    503: "Soybean for fodder",
    504: "Leucena",
    505: "Desmodium",
    506: "Mucuna",
    507: "Setaria",
    508: "Tripsacum",
    509: "Herbaceous",
    510: "Other fodder crop",
}

CROP_CATEGORY_CODES = {
    "Cereal": "Cereal",
    "Legume": "Legume",
    "Tuber": "Tuber",
    "Vegetable": "Vegetable",
    "Fruit": "Fruit",
    "Annual": "Annual",
    "Perennial": "Perennial",
    "Fodder": "Fodder",
}

# -----------------------------------------------------------------------------
# AGRICULTURAL PRACTICES
# -----------------------------------------------------------------------------

STAGE_PRACTICE_CODES = {
    1: "Ploughing",
    2: "Soil leveling",
    3: "Raking",
    4: "Manuring",
    5: "Sowing",
    6: "Weeding",
    7: "Irrigation",
    8: "Harvesting",
    9: "Threshing",
    10: "Winnowing",
    11: "Harvest packing",
    12: "Pesticides spraying",
    13: "Other stage of agriculture practice",
}

EROSION_DEGREE_CODES = {
    1: "Severe (Rill/Gully/Mass movement)",
    2: "Moderate (Overland flow)",
    3: "Low (Wind erosion)",
    4: "Very Low (Splash erosion)",
}

# -----------------------------------------------------------------------------
# INPUTS
# -----------------------------------------------------------------------------

IRRIGATION_TECHNIQUE_CODES = {
    1: "Surface irrigation",
    2: "Flood irrigation",
    3: "Drip irrigation",
    4: "Sprinkler irrigation",
    5: "Pivot irrigation",
    6: "Traditional techniques",
}

IRRIGATION_SOURCE_CODES = {
    1: "Rainwater harvesting",
    2: "Water treatment plant",
    3: "Underground water",
    4: "Lake/stream water",
    5: "Water catchment (dam)",
    6: "Other source",
}

IRRIGATION_TOOL_CODES = {
    1: "Irrigation machine",
    2: "Moto pump",
    3: "Tube wells",
    4: "Water can",
    5: "Water channels",
    6: "Jerrycan/basin",
    7: "Another tool",
}

ORGANIC_FERTILIZER_TYPE_CODES = {
    1: "Manure",
    2: "Green manure",
    3: "Compost",
    4: "Biogas",
    5: "Other",
}

INORGANIC_FERTILIZER_TYPE_CODES = {
    1: "NPK 17-17-17",
    2: "NPK 20-10-10",
    3: "NPK 25-5-5",
    4: "NPK 22-6-12",
    5: "Other NPK",
    6: "Urea solid",
    7: "Urea liquid",
    8: "DAP",
    9: "TSP",
    10: "KCl/MOP",
    11: "Omax",
    12: "Winner",
    13: "Yara Viva",
    14: "Amidas",
    15: "Cereal",
    16: "Boaster",
    17: "Lime",
    18: "Risobium",
    19: "DI Grow",
    20: "Dyma gro",
    21: "Other fertilizer",
}

PESTICIDE_TYPE_CODES = {
    1: "Dithane",
    2: "Ridomil",
    3: "Dimethoate (DUDU)",
    4: "Cypermethrin",
    5: "Dursiban",
    6: "Tilt",
    7: "Pilkare",
    8: "Rocket",
    9: "Beam",
    10: "Lava",
    11: "Rodazin",
    12: "Thiviot",
    13: "Safari max",
    14: "Victory",
    15: "Copper (akarbata)",
    16: "Supra",
    17: "Alfatox",
    18: "Daconil",
    19: "Vende",
    20: "Ortivato",
    21: "Mastercop",
    22: "Atoc",
    23: "Lambdex",
    24: "Evisect",
    25: "Prove",
    26: "Abamectin",
    27: "Fenvalerate",
    28: "Copper oxychloride",
    29: "Othello",
    30: "Balcolex",
    31: "Cabrio",
    32: "Commando",
    33: "Confidor",
    34: "Cypro",
    35: "Easygrowth",
    36: "Endofil",
    37: "Indofil M45",
    38: "Safari",
    39: "Jacket",
    40: "Lambda",
    41: "Mancozeb",
    42: "Millmax",
    43: "Miovit",
    44: "Octiva",
    45: "Orius",
    46: "Ramdan",
    47: "Profex super",
    48: "Round all",
    49: "Safari Zeb",
    50: "Scower",
    51: "Sumithio",
    52: "Vital",
    53: "Carbendazim/Carbapu supa",
    54: "Other pesticides/fungicides",
}

SOURCE_OF_IMPROVED_SEEDS_CODES = {
    1: "Government (MINAGRI/RAB/NAEB)",
    2: "Agro-dealers",
    3: "NGOs",
    4: "Market",
    5: "Other",
}

STORAGE_FACILITY_CODES = {
    1: "Own storage",
    2: "Public storage",
    3: "Storage owned by Cooperatives or private companies",
    4: "Other storage",
}

MARKET_PLACE_CODES = {
    1: "At Farm/Home",
    2: "Market",
    3: "Cooperative/Company/Association",
    4: "Outside the country",
    5: "Another selling place",
}

# -----------------------------------------------------------------------------
# PRODUCTION STATUS EXPLANATION
# -----------------------------------------------------------------------------

PRODUCTION_STATUS_CODES = {
    1: "Drought",
    2: "Heavy rainfall/Hailstones",
    3: "Insufficient rainfall",
    4: "Insufficient/Lack of fertilizers",
    5: "Late sowing",
    6: "Flood",
    7: "Landslide",
    8: "Crop destroyed by animals",
    9: "Diseases and pests",
    10: "Unfertile soil",
    11: "Inappropriate seeds",
    12: "Biennial effect (coffee)",
    13: "Lack of improved seeds",
    14: "Strong winds",
    15: "Perennial crops not yet mature",
    16: "Appropriate use of fertilizers",
    17: "Good quality of seeds",
    18: "Appropriate agricultural practices",
    19: "Other reason",
}

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def decode(value, codebook, default="Unknown"):
    """Safely decode a code to its label."""
    try:
        return codebook.get(int(value), default)
    except (ValueError, TypeError):
        return default


def province_name(code):
    return decode(code, PROVINCE_CODES)


def district_name(code):
    return decode(code, DISTRICT_CODES)


def crop_name(code):
    return decode(code, CROP_CODES)


def stratum_name(code):
    return decode(code, STRATUM_CODES)


def farmer_category_name(code):
    return decode(code, FARMER_CATEGORY_CODES)