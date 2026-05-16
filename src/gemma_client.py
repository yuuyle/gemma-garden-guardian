from __future__ import annotations

import json
import mimetypes
import os
import re
from dataclasses import dataclass
from typing import Any

from jsonschema import ValidationError

from src.prompts import build_analysis_prompt
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
    temperature: float = 0.1
    max_output_tokens: int = 2048

    @classmethod
    def from_env(cls) -> "GemmaClientConfig":
        return cls(
            mode=os.getenv("GEMMA_GARDEN_MODE", "mock").strip().lower() or "mock",
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT", "").strip(),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip(),
            model_id=os.getenv("GEMMA_MODEL_ID", "gemma-4-26b-a4b-it-maas").strip(),
            max_retries=int(os.getenv("GEMMA_MAX_RETRIES", "1")),
            temperature=float(os.getenv("GEMMA_TEMPERATURE", "0.1")),
            max_output_tokens=int(os.getenv("GEMMA_MAX_OUTPUT_TOKENS", "2048")),
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

        mime_type = self._guess_image_mime_type(image_name=image_name, image_bytes=image_bytes)
        prompt = build_analysis_prompt(crop_type=crop_type, notes=notes)

        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise GemmaClientError(
                "google-genai is not installed. Run `pip install -r requirements.txt`."
            ) from exc

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                ],
            )
        ]
        config = types.GenerateContentConfig(
            temperature=self.config.temperature,
            top_p=0.9,
            max_output_tokens=self.config.max_output_tokens,
        )

        try:
            response = self._generate_content_with_location(
                genai=genai,
                location=self.config.location,
                contents=contents,
                config=config,
            )
        except Exception as exc:
            if self.config.location != "global" and "global endpoint" in str(exc):
                response = self._generate_content_with_location(
                    genai=genai,
                    location="global",
                    contents=contents,
                    config=config,
                )
            else:
                raise

        text = getattr(response, "text", "") or ""
        if not text:
            raise GemmaClientError("Vertex AI returned an empty response.")
        return self._extract_json_payload(text)

    def _generate_content_with_location(
        self,
        genai: Any,
        location: str,
        contents: Any,
        config: Any,
    ) -> Any:
        client = genai.Client(
            vertexai=True,
            project=self.config.project_id,
            location=location,
        )
        return client.models.generate_content(
            model=self.config.model_id,
            contents=contents,
            config=config,
        )

    def _validate_or_repair(self, payload: dict[str, Any] | str, crop_type: str) -> dict[str, Any]:
        if isinstance(payload, str):
            payload = self._extract_json_payload(payload)

        try:
            return validate_analysis(payload)
        except ValidationError:
            repaired = repair_analysis_payload(payload=payload, crop_type=crop_type)
            return validate_analysis(repaired)

    def _extract_json_payload(self, text: str) -> dict[str, Any]:
        """Parse model text that may be plain JSON or fenced Markdown JSON."""
        stripped = text.strip()
        if not stripped:
            raise GemmaClientError("Model response was empty.")

        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, flags=re.DOTALL)
        if fence_match:
            stripped = fence_match.group(1).strip()
        elif not stripped.startswith("{"):
            start = stripped.find("{")
            end = stripped.rfind("}")
            if start == -1 or end == -1 or end <= start:
                raise GemmaClientError("Model response did not contain a JSON object.")
            stripped = stripped[start : end + 1]

        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise GemmaClientError(f"Model response was not valid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise GemmaClientError("Model response JSON must be an object.")
        return payload

    def _guess_image_mime_type(self, image_name: str, image_bytes: bytes) -> str:
        if image_bytes.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
            return "image/webp"

        guessed, _ = mimetypes.guess_type(image_name)
        if guessed in {"image/jpeg", "image/png", "image/webp"}:
            return guessed
        raise GemmaClientError(
            "Vertex AI image input supports JPEG, PNG, and WebP in this app. "
            f"Unsupported or unknown file type: {image_name or 'uploaded image'}"
        )


def analyze_image_mock(crop_type: str, notes: str = "", image_name: str = "") -> dict:
    """Phase 1/2 client entrypoint that returns a mock Gemma-shaped response."""
    return build_mock_analysis(crop_type=crop_type, notes=notes, image_name=image_name)
