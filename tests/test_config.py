"""Tests for configuration management."""
import json
import tempfile
from pathlib import Path

import pytest
from mlx_control.config import Config


class TestConfig:
    """Test configuration handling."""

    @pytest.fixture
    def temp_config_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_settings_load_defaults(self, monkeypatch, temp_config_dir):
        config = Config()
        monkeypatch.setattr(config, "config_dir", temp_config_dir)
        monkeypatch.setattr(config, "settings_file", temp_config_dir / "settings.json")

        settings = config.load_settings()
        assert settings["temperature"] == 0.7
        assert settings["max_tokens"] == 512

    def test_settings_save_and_load(self, monkeypatch, temp_config_dir):
        config = Config()
        monkeypatch.setattr(config, "config_dir", temp_config_dir)
        monkeypatch.setattr(config, "settings_file", temp_config_dir / "settings.json")

        test_data = {"temperature": 1.2, "max_tokens": 1024}
        config.save_settings(test_data)

        loaded = config.load_settings()
        assert loaded["temperature"] == 1.2
        assert loaded["max_tokens"] == 1024

    def test_system_prompt_save_and_load(self, monkeypatch, temp_config_dir):
        config = Config()
        monkeypatch.setattr(config, "config_dir", temp_config_dir)
        monkeypatch.setattr(config, "prompt_file", temp_config_dir / "prompt.txt")

        prompt = "You are a helpful assistant."
        config.save_system_prompt(prompt)

        loaded = config.get_system_prompt()
        assert loaded == prompt

    def test_invalid_temperature(self, monkeypatch, temp_config_dir):
        config = Config()
        monkeypatch.setattr(config, "config_dir", temp_config_dir)
        monkeypatch.setattr(config, "settings_file", temp_config_dir / "settings.json")

        invalid_data = {"temperature": 5.0, "max_tokens": 512}
        config.settings_file.write_text(json.dumps(invalid_data))

        settings = config.load_settings()
        assert settings["temperature"] == 0.7  # Should use default
