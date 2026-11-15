"""API client for MLX backend communication."""
import json
import logging
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class APIClient:
    """Handles HTTP requests to MLX API."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def request(
        self, path: str, payload: Optional[Dict] = None, timeout: int = 1200
    ) -> Dict[str, Any]:
        """Make authenticated request to API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")

        url = self.base_url + path
        req = urllib.request.Request(url, data=data, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=timeout) as res:
                return json.load(res)
        except urllib.error.HTTPError as exc:
            detail = exc.read(1200).decode("utf-8", "replace")
            logger.error(f"HTTP {exc.code}: {detail}")
            raise RuntimeError(f"API Error {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            logger.error(f"Connection failed: {exc}")
            raise RuntimeError(f"Cannot reach API: {exc}") from exc

    def get_status(self) -> Dict[str, Any]:
        """Get current API status."""
        return self.request("/status", timeout=5)

    def get_models(self) -> List[str]:
        """List available models."""
        data = self.request("/v1/models")
        models = [x["id"] for x in data.get("data", []) if isinstance(x, dict) and x.get("id")]
        return sorted(models)

    def get_active_model(self) -> Optional[str]:
        """Get currently active model."""
        try:
            return self.get_status().get("active_model")
        except Exception:
            return None

    def chat_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send chat completion request."""
        return self.request("/v1/chat/completions", payload)
