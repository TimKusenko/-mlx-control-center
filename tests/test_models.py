"""Tests for model parsing and grouping."""
import pytest
from mlx_control.models import ModelGrouper


class TestModelGrouper:
    """Test model ID parsing."""

    def test_parse_llama_quantized(self):
        model_id = "mlx-community/Llama-3.2-1B-4bit"
        family, size, quant = ModelGrouper.parse(model_id)
        assert "Llama" in family
        assert size == "1B"
        assert quant == "4-bit"

    def test_parse_mistral(self):
        model_id = "mistralai/Mistral-7B-v0.1"
        family, size, quant = ModelGrouper.parse(model_id)
        assert "Mistral" in family
        assert size == "7B"
        assert quant == "unbekannt"

    def test_parse_unknown_format(self):
        model_id = "custom-model"
        family, size, quant = ModelGrouper.parse(model_id)
        assert family == "custom-model"  # Dashes are not replaced
        assert size == "Andere"
        assert quant == "unbekannt"

    def test_group_models(self):
        models = [
            "mlx-community/Llama-3.2-1B-4bit",
            "mlx-community/Llama-3.2-1B-8bit",
            "mistralai/Mistral-7B-v0.1",
        ]
        grouped = ModelGrouper.group_models(models)
        assert len(grouped) >= 2
        assert any("Llama" in family for family in grouped)
        assert any("Mistral" in family for family in grouped)

    def test_sort_sizes(self):
        sizes = ["7B", "1B", "70B", "3.2B"]
        sorted_sizes = ModelGrouper.sort_sizes(sizes)
        assert sorted_sizes[0] == "1B"
        assert sorted_sizes[-1] == "70B"
