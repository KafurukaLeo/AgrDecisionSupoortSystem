# AI-Powered Agricultural Productivity Decision Support System for Rwanda

## Overview
An AI-powered system that analyzes NISR agricultural data and predicts agricultural productivity, presented through an interactive dashboard.

## Tech Stack
- Python
- Pandas & NumPy
- Scikit-learn
- Matplotlib / Plotly
- Streamlit (frontend)
- FastAPI (backend)
- PostgreSQL
- Git / GitHub

## Quick Start (Windows)
1. Install Python 3.10 or newer (tick "Add python.exe to PATH")
2. Double-click `setup.bat` (one time only: creates the virtual environment and installs packages)
3. Double-click `start.bat` (starts backend + frontend and opens http://localhost:8501)

- Backend API docs: http://127.0.0.1:8000/docs
- `start.bat` runs `setup.bat` automatically on a new computer, so step 2 is optional.
- Do not copy the `venv/` folder between computers; `setup.bat` rebuilds it.

### Enabling the Prediction Tool
The trained model files are not stored in Git. Copy them to:
- `backend/app/ml/artifacts/model.pkl`  (the Random Forest, e.g. `best_model_random_forest.pkl`)
- `backend/app/ml/artifacts/label_encoders.pkl`

Until then, the Prediction Tool shows a warning and the Predict button is disabled.

## Manual Setup (any OS)
1. Clone the repository
2. Create a virtual environment: `python -m venv venv` and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and update values
5. Run backend: `uvicorn backend.app.main:app --reload`
6. Run frontend: `python run_frontend.py`

## Project Structure
See `docs/architecture/` for details.

# Backend — AI Agri Decision Support Rwanda

FastAPI backend for the AI-Powered Agricultural Productivity Decision Support System.

## Structure

- `app/main.py` — FastAPI application entry point
- `app/config.py` — Application configuration (reads `.env`)
- `app/api/v1/` — API route handlers
  - `health.py` — Health check
  - `productivity.py` — Productivity endpoints
  - `prediction.py` — Prediction endpoint
  - `filters.py` — Filter options
  - `router.py` — Route aggregator
- `app/core/` — Core utilities (security, logging)
- `app/models/` — SQLAlchemy ORM models (Phase 4)
- `app/schemas/` — Pydantic request/response schemas
- `app/services/` — Business logic layer
- `app/repositories/` — Data access layer
- `app/ml/` — ML inference integration (Phase 7)
- `app/middleware/` — Custom middleware
- `app/utils/` — Helper functions

## Running the Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload --port 8000