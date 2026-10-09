"""
Launcher for the Streamlit frontend.
Adds project root to sys.path so `frontend` package imports resolve.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from streamlit.web import cli as stcli

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        str(PROJECT_ROOT / "frontend" / "app.py"),
        "--server.port=8501",
        "--server.headless=true",
    ]
    sys.exit(stcli.main())