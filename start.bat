@echo off
setlocal
cd /d "%~dp0"

REM --- Run setup automatically if this computer has no working venv yet
set "NEEDS_SETUP="
if not exist "venv\Scripts\python.exe" set "NEEDS_SETUP=1"
if not defined NEEDS_SETUP (
  "venv\Scripts\python.exe" -c "import fastapi, streamlit" >nul 2>&1
  if errorlevel 1 set "NEEDS_SETUP=1"
)
if defined NEEDS_SETUP (
  echo First run on this computer - running setup...
  call setup.bat
  if not exist "venv\Scripts\python.exe" exit /b 1
)

echo Starting backend  (http://127.0.0.1:8000) ...
start "Backend - FastAPI" cmd /k ""venv\Scripts\python.exe" -m uvicorn backend.app.main:app --port 8000"

echo Starting frontend (http://localhost:8501) ...
start "Frontend - Streamlit" cmd /k ""venv\Scripts\python.exe" run_frontend.py"

echo Waiting for the servers to start...
timeout /t 8 /nobreak >nul
start "" http://localhost:8501

echo.
echo Two windows were opened (Backend and Frontend). Close them to stop the app.
