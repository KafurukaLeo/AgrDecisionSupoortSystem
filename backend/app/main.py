"""
FastAPI application entry point.

Run either way:
    uvicorn backend.app.main:app --port 8000 --reload   (from project root)
    python main.py                                      (from backend/app)
"""
import sys
from pathlib import Path

# Make `backend.app.*` importable when this file is run directly
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import get_settings
from backend.app.api.v1.router import api_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Agricultural Productivity Decision Support System for Rwanda",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow the frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        app_dir=str(PROJECT_ROOT),
        reload_dirs=[str(PROJECT_ROOT / "backend")],
    )