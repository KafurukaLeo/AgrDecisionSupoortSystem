"""
Launcher for the Streamlit frontend.
Adds project root to sys.path so frontend package imports resolve.
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from streamlit.web import cli as stcli

if __name__ == "__main__":
    streamlit_port = os.getenv("STREAMLIT_PORT", "8501")
    streamlit_host = os.getenv("STREAMLIT_HOST", "127.0.0.1")
    sys.argv = [
        "streamlit",
        "run",
        str(PROJECT_ROOT / "frontend" / "app.py"),
        f"--server.port={streamlit_port}",
        f"--server.address={streamlit_host}",
        "--server.headless=true",
    ]
    sys.exit(stcli.main())