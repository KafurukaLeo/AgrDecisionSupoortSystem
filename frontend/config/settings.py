"""
Frontend configuration.
"""
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("FRONTEND_API_URL", "http://localhost:8000")
API_V1 = f"{API_BASE_URL}/api/v1"

APP_TITLE = "AI Agri Decision Support Rwanda"
APP_ICON = "🌾"