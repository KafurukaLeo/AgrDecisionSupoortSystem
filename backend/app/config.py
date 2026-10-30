
"""
Application configuration.
Reads settings from environment variables or .env file.
Supports local PostgreSQL and Neon PostgreSQL.
"""

from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Agri Decision Support Rwanda"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    SECRET_KEY: str = "change-me"

    # Database - Neon PostgreSQL
    DATABASE_URL: str = (
        "postgresql://neondb_owner:npg_j2N6VOwlixga"
        "@ep-nameless-brook-b5rbqk7d-pooler.c-7.us-east-2.aws.neon.tech/"
        "agri_db?sslmode=require&channel_binding=require"
    )

    DATABASE_HOST: str = (
        "ep-nameless-brook-b5rbqk7d-pooler.c-7.us-east-2.aws.neon.tech"
    )
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "agri_db"
    DATABASE_USER: str = "neondb_owner"
    DATABASE_PASSWORD: str = "npg_j2N6VOwlixga"

    # Machine Learning
    MODEL_PATH: str = "ml/artifacts/models/random_forest_v1.pkl"
    SCALER_PATH: str = "ml/artifacts/encoders/scaler.pkl"
    ENCODER_PATH: str = "ml/artifacts/encoders/label_encoders.pkl"

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
