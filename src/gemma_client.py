from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from jsonschema import ValidationError

from src.sample_outputs import build_mock_analysis
from src.schemas import build_fallback_analysis, repair_analysis_payload, validate_analysis


class GemmaClientError(RuntimeError):
    """Raised when the Gemma client cannot produce a reliable result."""


@dataclass(frozen=True)
class GemmaClientConfig:
    mode: str = "mock"
    project_id: str = ""
    location: str = "us-central1"
    model_id: str = "gemma-4-26b-a4b-it-maas"
    max_retries: int = 1

    @classmethod
    def from_env(cls) -> "GemmaClientConfig":
        return cls(
            mode=os.getenv("GEMMA_GARDEN_MODE", "mock").strip().lower() or "mock",
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT", "").strip(),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip(),
            model_id=os.getenv("GEMMA_MODEL_ID", "gemma-4-26b-a4b-it-maas").strip(),
            max_retries=int(os.getenv("GEMMA_MAX_RETRIES", "1")),
        )


@dataclass
class AnalysisResult:
    analysis: dict[str, Any]
    source: str
    used_fallback: bool = False
    error: str = ""


class GemmaClient:
    """Small client wrapper that keeps mock mode first and cloud mode optional."""

    def __init__(self, config: GemmaClientConfig | None = None) -> None:
        self.config = config or GemmaClientConfig.from_env()

    def analyze_image(
        self,
        image_bytes: bytes,
        crop_type: str,
        notes: str = "",
        image_name: str = "",
    ) -> AnalysisResult:
        if self.config.mode == "mock":
            analysis = build_mock_analysis(crop_type=crop_type, notes=notes, image_name=image_name)
            return AnalysisResult(analysis=validate_analysis(analysis), source="mock")

        last_error: Exception | None = None
        for _attempt in range(max(1, self.config.max_retries + 1)):
            try:
                payload = self._analyze_with_vertex(
                    image_bytes=image_bytes,
                    crop_type=crop_type,
                    notes=notes,
                    image_name=image_name,
                )
                analysis = self._validate_or_repair(payload=payload, crop_type=crop_type)
                return AnalysisResult(analysis=analysis, source="vertex")
            except Exception as exc:
                last_error = exc

        try:
            analysis = build_mock_analysis(crop_type=crop_type, notes=notes, image_name=image_name)
            validated = validate_analysis(analysis)
            return AnalysisResult(
                analysis=validated,
                source="mock-fallback",
                used_fallback=True,
                error=str(last_error),
            )
        except Exception as exc:
            fallback = build_fallback_analysis(crop_type=crop_type, reason=str(exc))
            return AnalysisResult(
                analysis=validate_analysis(fallback),
                source="fallback",
                used_fallback=True,
                error=str(exc),
            )

    def _analyze_with_vertex(
        self,
        image_bytes: bytes,
        crop_type: str,
        notes: str,
        image_name: str,
    ) -> dict[str, Any]:
        if not image_bytes:
            raise GemmaClientError("No image bytes were provided.")
        if not self.config.project_id:
            raise GemmaClientError("GOOGLE_CLOUD_PROJECT is required when GEMMA_GARDEN_MODE=vertex.")

        raise GemmaClientError(
            "Vertex AI Gemma 4 call is not wired yet. Keep GEMMA_GARDEN_MODE=mock until "
            "Google Cloud authentication and the Model Garden endpoint are configured."
        )

    def _validate_or_repair(self, payload: dict[str, Any] | str, crop_type: str) -> dict[str, Any]:
        if isinstance(payload, str):
            payload = json.loads(payload)

        try:
            return validate_analysis(payload)
        except ValidationError:
            repaired = repair_analysis_payload(payload=payload, crop_type=crop_type)
            return validate_analysis(repaired)


def analyze_image_mock(crop_type: str, notes: str = "", image_name: str = "") -> dict:
    """Phase 1/2 client entrypoint that returns a mock Gemma-shaped response."""
    return build_mock_analysis(crop_type=crop_type, notes=notes, image_name=image_name)
