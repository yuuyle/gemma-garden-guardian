from __future__ import annotations

from copy import deepcopy
from typing import Any

from jsonschema import Draft202012Validator


CONFIDENCE_VALUES = ["low", "medium", "high"]
RISK_VALUES = ["low", "medium", "high"]
STATUS_VALUES = ["healthy", "needs_attention", "monitor", "unknown"]


ANALYSIS_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Gemma Garden Guardian Analysis",
    "type": "object",
    "required": [
        "crop_type",
        "overall_status",
        "summary",
        "observations",
        "risk_level",
        "risks",
        "recommended_actions",
        "uncertainty",
        "next_photo_suggestions",
    ],
    "additionalProperties": False,
    "properties": {
        "crop_type": {"type": "string", "minLength": 1},
        "overall_status": {"type": "string", "enum": STATUS_VALUES},
        "summary": {"type": "string", "minLength": 1},
        "observations": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["category", "finding", "confidence"],
                "additionalProperties": False,
                "properties": {
                    "category": {"type": "string", "minLength": 1},
                    "finding": {"type": "string", "minLength": 1},
                    "confidence": {"type": "string", "enum": CONFIDENCE_VALUES},
                },
            },
        },
        "risk_level": {"type": "string", "enum": RISK_VALUES},
        "risks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "reason", "confidence"],
                "additionalProperties": False,
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "reason": {"type": "string", "minLength": 1},
                    "confidence": {"type": "string", "enum": CONFIDENCE_VALUES},
                },
            },
        },
        "recommended_actions": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["priority", "action", "reason"],
                "additionalProperties": False,
                "properties": {
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                    "action": {"type": "string", "minLength": 1},
                    "reason": {"type": "string", "minLength": 1},
                },
            },
        },
        "uncertainty": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "next_photo_suggestions": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
    },
}


ANALYSIS_VALIDATOR = Draft202012Validator(ANALYSIS_SCHEMA)


def validate_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate an analysis payload and return it unchanged when valid."""
    ANALYSIS_VALIDATOR.validate(payload)
    return payload


def build_fallback_analysis(crop_type: str, reason: str) -> dict[str, Any]:
    """Return a valid conservative analysis when a model response cannot be used."""
    return {
        "crop_type": crop_type or "unknown crop",
        "overall_status": "unknown",
        "summary": (
            "The analysis could not be completed reliably, so this fallback result avoids "
            "making crop health claims. Please retake the photo and confirm visible signs locally."
        ),
        "observations": [
            {
                "category": "system",
                "finding": f"The model response was not usable: {reason}",
                "confidence": "low",
            }
        ],
        "risk_level": "medium",
        "risks": [
            {
                "name": "uncertain_analysis",
                "reason": "The app could not validate a complete structured response.",
                "confidence": "low",
            }
        ],
        "recommended_actions": [
            {
                "priority": "high",
                "action": "Retake the photo in clear natural light and review the plant in person.",
                "reason": "A clearer observation is safer than relying on an incomplete model response.",
            }
        ],
        "uncertainty": [
            "No specific crop issue can be confirmed from this failed analysis.",
            "Local growing conditions and recent care history still need to be checked.",
        ],
        "next_photo_suggestions": [
            "Capture one full-plant photo and one close-up of the most concerning area.",
            "Avoid harsh shadows, blur, and very close crops that hide the plant context.",
        ],
    }


def repair_analysis_payload(payload: dict[str, Any], crop_type: str) -> dict[str, Any]:
    """Apply small safe repairs before validation.

    This is intentionally conservative. It fills missing optional arrays and normalizes a few
    enum-like values, but it does not invent detailed observations.
    """
    repaired = deepcopy(payload)
    repaired.setdefault("crop_type", crop_type or "unknown crop")
    repaired.setdefault("overall_status", "unknown")
    repaired.setdefault("summary", "Visible signs should be checked locally before acting.")
    repaired.setdefault("observations", [])
    repaired.setdefault("risks", [])
    repaired.setdefault("recommended_actions", [])
    repaired.setdefault("uncertainty", [])
    repaired.setdefault("next_photo_suggestions", [])

    if repaired.get("risk_level") not in RISK_VALUES:
        repaired["risk_level"] = "medium"
    if repaired.get("overall_status") not in STATUS_VALUES:
        repaired["overall_status"] = "unknown"

    if not repaired["observations"]:
        repaired["observations"] = [
            {
                "category": "general",
                "finding": "The response did not include a detailed visible observation.",
                "confidence": "low",
            }
        ]
    if not repaired["recommended_actions"]:
        repaired["recommended_actions"] = [
            {
                "priority": "medium",
                "action": "Inspect the plant in person and take a clearer follow-up photo.",
                "reason": "The structured response did not include enough actionable guidance.",
            }
        ]

    return repaired
