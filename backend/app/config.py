"""
Application configuration.
Reads from environment variables (.env file).
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Agri Decision Support Rwanda"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    SECRET_KEY: str = "change-me"

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/agri_db"

    # ML
    MODEL_PATH: str = "ml/artifacts/models/random_forest_v1.pkl"
    SCALER_PATH: str = "ml/artifacts/encoders/scaler.pkl"
    ENCODER_PATH: str = "ml/artifacts/encoders/label_encoders.pkl"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()