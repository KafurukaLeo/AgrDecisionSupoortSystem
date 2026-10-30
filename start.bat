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

if not defined BACKEND_PORT set "BACKEND_PORT=8000"
if not defined STREAMLIT_PORT set "STREAMLIT_PORT=8501"
if not defined FRONTEND_API_URL set "FRONTEND_API_URL=http://127.0.0.1:%BACKEND_PORT%"

echo Starting backend  (http://127.0.0.1:%BACKEND_PORT%) ...
start "Backend - FastAPI" cmd /k ""venv\Scripts\python.exe" -m uvicorn backend.app.main:app --host 127.0.0.1 --port %BACKEND_PORT%"

echo Starting frontend (http://localhost:%STREAMLIT_PORT%) ...
start "Frontend - Streamlit" cmd /k "set FRONTEND_API_URL=%FRONTEND_API_URL% && set STREAMLIT_PORT=%STREAMLIT_PORT% && ""venv\Scripts\python.exe" run_frontend.py"

echo Waiting for the servers to start...
timeout /t 8 /nobreak >nul
start "" http://localhost:%STREAMLIT_PORT%

echo.
echo Two windows were opened (Backend and Frontend). Close them to stop the app.
