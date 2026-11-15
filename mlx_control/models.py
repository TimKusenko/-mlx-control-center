"""Model management and organization."""
import re
from typing import Dict, List, Tuple


class ModelGrouper:
    """Parse and organize models by family, size, and quantization."""

    @staticmethod
    def parse(model_id: str) -> Tuple[str, str, str]:
        """
        Parse model ID into (family, size, quantization).

        Examples:
            "mlx-community/Llama-3.2-1B-4bit" -> ("Llama 3.2", "1B", "4-bit")
            "mistralai/Mistral-7B-v0.1" -> ("Mistral", "7B", "unbekannt")
        """
        short = model_id.split("/")[-1]

        # Extract quantization (e.g., -4bit, -8bit)
        q_match = re.search(r"-(\d+)bit$", short, re.I)
        quant = f"{q_match.group(1)}-bit" if q_match else "unbekannt"
        stem = short[: q_match.start()] if q_match else short

        # Extract parameter size (last B-token)
        matches = list(re.finditer(r"(?<![\d.])(\d+(?:\.\d+)?)[bB](?![\w])", stem))
        if not matches:
            matches = list(re.finditer(r"(?<![\d.])(\d+(?:\.\d+)?)[bB](?=-|$)", stem))

        if matches:
            m = matches[-1]
            size = m.group(1) + "B"
            family = (stem[: m.start()].rstrip("-_") or stem).replace("_", " ")
            extra = stem[m.end() :].strip("-_")
            if extra:
                family += " · " + extra
        else:
            size = "Andere"
            family = stem.replace("_", " ")

        return family, size, quant

    @staticmethod
    def group_models(model_ids: List[str]) -> Dict[str, Dict[str, List[Tuple[str, str]]]]:
        """
        Organize models by family, size, and quantization.

        Returns:
            {family: {size: [(quant, model_id), ...]}}
        """
        families = {}
        for mid in model_ids:
            family, size, quant = ModelGrouper.parse(mid)
            families.setdefault(family, {}).setdefault(size, []).append((quant, mid))
        return families

    @staticmethod
    def sort_sizes(sizes: List[str]) -> List[str]:
        """Sort model sizes numerically."""
        def extract_num(s: str) -> float:
            match = re.search(r"\d+(?:\.\d+)?", s)
            return float(match.group()) if match else 999

        return sorted(sizes, key=extract_num)
