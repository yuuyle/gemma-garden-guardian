from __future__ import annotations

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
