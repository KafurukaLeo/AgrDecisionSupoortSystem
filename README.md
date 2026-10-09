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

## Setup
1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and update values
5. Run backend: `uvicorn backend.app.main:app --reload`
6. Run frontend: `streamlit run frontend/app.py`

## Project Structure
See `docs/architecture/` for details.