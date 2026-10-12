"""
Import all models so Alembic and SQLAlchemy detect them.
"""
from backend.app.models.base import BaseModel  # noqa: F401
from backend.app.models.location import Province, District  # noqa: F401
from backend.app.models.crop import Crop  # noqa: F401
from backend.app.models.season import Season  # noqa: F401
from backend.app.models.productivity import ProductivityRecord  # noqa: F401
from backend.app.models.prediction_log import PredictionLog  # noqa: F401