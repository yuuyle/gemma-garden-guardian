from __future__ import annotations

from src.sample_outputs import build_mock_analysis


def analyze_image_mock(crop_type: str, notes: str = "", image_name: str = "") -> dict:
    """Phase 1/2 client entrypoint that returns a mock Gemma-shaped response."""
    return build_mock_analysis(crop_type=crop_type, notes=notes, image_name=image_name)
