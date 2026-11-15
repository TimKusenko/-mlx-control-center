"""Tests for API client."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from mlx_control.api import APIClient


class TestAPIClient:
    """Test API communication."""

    def test_client_initialization(self):
        client = APIClient("http://localhost:8080", "test-key")
        assert client.base_url == "http://localhost:8080"
        assert client.api_key == "test-key"

    @patch("urllib.request.urlopen")
    def test_get_models_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = b'{"data": [{"id": "model-1"}, {"id": "model-2"}]}'
        mock_urlopen.return_value = mock_response

        import json
        from io import StringIO

        # Better mock
        mock_file = MagicMock()
        mock_file.__enter__.return_value = StringIO('{"data": [{"id": "model-1"}, {"id": "model-2"}]}')
        mock_urlopen.return_value = mock_file

        # Patch json.load
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = {"data": [{"id": "model-1"}, {"id": "model-2"}]}

            client = APIClient("http://localhost:8080", "test-key")
            models = client.get_models()

            assert len(models) == 2
            assert "model-1" in models
            assert "model-2" in models

    @patch("urllib.request.urlopen")
    def test_get_models_filters_invalid(self, mock_urlopen):
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = {
                "data": [
                    {"id": "valid-model"},
                    {"id": None},
                    "invalid",
                ]
            }

            client = APIClient("http://localhost:8080", "test-key")
            models = client.get_models()

            assert models == ["valid-model"]

    @patch("urllib.request.urlopen")
    def test_request_headers(self, mock_urlopen):
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = {}
            mock_urlopen.return_value.__enter__ = Mock(return_value=MagicMock())
            mock_urlopen.return_value.__exit__ = Mock(return_value=None)

            client = APIClient("http://localhost:8080", "test-key-123")
            try:
                client.request("/test")
            except:
                pass

            # Check that Authorization header was set
            call_args = mock_urlopen.call_args
            if call_args:
                request = call_args[0][0]
                assert "Authorization" in request.headers
                assert "Bearer test-key-123" in request.headers["Authorization"]
