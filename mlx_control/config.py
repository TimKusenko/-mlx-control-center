"""Configuration management for MLX Control Center."""
import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Centralized configuration handling."""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "mlx-control"
        self.settings_file = self.config_dir / "settings.json"
        self.prompt_file = self.config_dir / "system-prompt.txt"
        self.api_key_file = Path.home() / ".config" / "mlx-api" / "api-key"

        # Environment-based overrides
        import os
        self.mac_host = os.environ.get("MLX_MAC_HOST", "user@your-mac.local")
        self.api_url = os.environ.get("MLX_API_URL", "http://127.0.0.1:8080").rstrip("/")
        self.log_dir = "~/security-ai/multi-model-api/logs"

    def ensure_dirs(self) -> None:
        """Create config directories if missing."""
        self.config_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    def get_api_key(self) -> str:
        """Retrieve API key from secure storage."""
        if not self.api_key_file.exists():
            raise RuntimeError(f"API key missing at {self.api_key_file}")
        key = self.api_key_file.read_text().strip()
        if not key:
            raise RuntimeError(f"API key is empty")
        return key

    def load_settings(self) -> Dict[str, Any]:
        """Load temperature and max_tokens from config."""
        defaults = {"temperature": 0.7, "max_tokens": 512}
        if self.settings_file.exists():
            try:
                data = json.loads(self.settings_file.read_text())
                if isinstance(data, dict):
                    t = data.get("temperature", 0.7)
                    m = data.get("max_tokens", 512)
                    if isinstance(t, (int, float)) and 0 <= t <= 2:
                        defaults["temperature"] = float(t)
                    if isinstance(m, int) and 1 <= m <= 8192:
                        defaults["max_tokens"] = m
            except (OSError, ValueError):
                pass
        return defaults

    def save_settings(self, data: Dict[str, Any]) -> None:
        """Save settings to config file."""
        self.ensure_dirs()
        self.settings_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        self.settings_file.chmod(0o600)

    def get_system_prompt(self) -> str:
        """Get saved system prompt."""
        if self.prompt_file.is_file():
            return self.prompt_file.read_text()
        return ""

    def save_system_prompt(self, prompt: str) -> None:
        """Save system prompt to file."""
        self.ensure_dirs()
        self.prompt_file.write_text(prompt)
        self.prompt_file.chmod(0o600)
