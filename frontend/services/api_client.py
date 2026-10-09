"""
HTTP client for backend API.
"""
import requests
from typing import Optional, Dict, Any

from frontend.config.settings import API_V1


class APIClient:
    def __init__(self, base_url: str = API_V1, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: Dict) -> Any:
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    # Health
    def health(self) -> Dict:
        return self._get("/health/")

    # Productivity
    def get_summary(self) -> Dict:
        return self._get("/productivity/summary")

    def get_by_crop(self) -> Dict:
        return self._get("/productivity/by-crop")

    # Filters
    def get_filter_options(self) -> Dict:
        return self._get("/filters/options")

    # Prediction
    def predict(self, payload: Dict) -> Dict:
        return self._post("/predict/", payload)


api_client = APIClient()