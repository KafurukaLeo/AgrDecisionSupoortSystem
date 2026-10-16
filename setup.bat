@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo  AI Agri Decision Support Rwanda - one-time setup
echo ============================================================

REM --- Find a Python interpreter (prefer 3.12, then any 3.x, then plain python)
set "PY="
py -3.12 --version >nul 2>&1 && set "PY=py -3.12"
if not defined PY (
  py -3 --version >nul 2>&1 && set "PY=py -3"
)
if not defined PY (
  python --version >nul 2>&1 && set "PY=python"
)
if not defined PY (
  echo.
  echo Python was not found.
  echo Install Python 3.10 or newer from https://www.python.org/downloads/
  echo and tick "Add python.exe to PATH" during installation.
  pause
  exit /b 1
)
echo Using: %PY%

REM --- A venv copied from another computer does not work here, so rebuild it
if exist "venv\Scripts\python.exe" (
  "venv\Scripts\python.exe" -c "import sys" >nul 2>&1
  if errorlevel 1 (
    echo The existing venv came from another computer. Rebuilding it...
    rmdir /s /q venv
  )
)

if not exist "venv\Scripts\python.exe" (
  echo Creating virtual environment...
  %PY% -m venv venv
  if errorlevel 1 (
    echo Could not create the virtual environment.
    pause
    exit /b 1
  )
)

REM --- Create .env from the template if missing
if not exist ".env" (
  if exist ".env.example" (
    copy ".env.example" ".env" >nul
    echo Created .env from .env.example
  )
)

echo Installing packages (this can take a few minutes the first time)...
"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Package installation failed. Check your internet connection and try again.
  pause
  exit /b 1
)

echo.
echo Setup complete.
if not exist "backend\app\ml\artifacts\model.pkl" (
  echo.
  echo NOTE: The trained model files are not present, so the Prediction Tool
  echo       will show a warning. Copy these two files to enable predictions:
  echo         model.pkl           -^> backend\app\ml\artifacts\model.pkl
  echo         label_encoders.pkl  -^> backend\app\ml\artifacts\label_encoders.pkl
)
echo.
echo Next step: double-click start.bat
pause
