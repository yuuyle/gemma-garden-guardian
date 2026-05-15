from __future__ import annotations


def build_mock_analysis(crop_type: str, notes: str = "", image_name: str = "") -> dict:
    """Return a safe, schema-shaped mock response for local development."""
    normalized_crop = crop_type or "unknown crop"
    note_context = (
        "The user's notes mention recent context that should be confirmed locally."
        if notes
        else "No user notes were provided, so the mock result stays conservative."
    )

    return {
        "crop_type": normalized_crop,
        "overall_status": "needs_attention",
        "summary": (
            f"Visible signs in the uploaded {normalized_crop} photo may indicate mild stress. "
            "Please confirm by checking the plant in person before making treatment decisions."
        ),
        "observations": [
            {
                "category": "leaf",
                "finding": "Some leaves appear uneven in color, which may indicate nutrient, watering, or light stress.",
                "confidence": "medium",
            },
            {
                "category": "canopy",
                "finding": "The plant structure is visible enough for a first-pass review, but close-up details remain limited.",
                "confidence": "medium",
            },
            {
                "category": "context",
                "finding": f"{note_context} Image file: {image_name or 'uploaded photo'}.",
                "confidence": "low",
            },
        ],
        "risk_level": "medium",
        "risks": [
            {
                "name": "water_stress",
                "reason": "Visible signs suggest the plant may benefit from checking soil moisture near the root zone.",
                "confidence": "medium",
            },
            {
                "name": "nutrient_or_light_stress",
                "reason": "Uneven leaf color can have several causes, so this should be confirmed with recent care history.",
                "confidence": "low",
            },
        ],
        "recommended_actions": [
            {
                "priority": "high",
                "action": "Check soil moisture 2-5 cm below the surface before watering again.",
                "reason": "This helps distinguish dry soil from overwatering without guessing from the image alone.",
            },
            {
                "priority": "medium",
                "action": "Inspect the underside of several leaves for visible pests or residue.",
                "reason": "A closer inspection can confirm whether the visible stress is linked to pests or another cause.",
            },
            {
                "priority": "low",
                "action": "Take a follow-up photo in similar lighting after the next watering or care change.",
                "reason": "Consistent photos make it easier to compare whether the plant is improving.",
            },
        ],
        "uncertainty": [
            "A single image cannot confirm a specific disease, pest, or nutrient deficiency.",
            "Soil moisture, recent weather, watering schedule, and local conditions are not fully visible.",
            "Any pesticide-related decision should follow local regulations and product labels.",
        ],
        "next_photo_suggestions": [
            "Capture a close-up of the most affected leaves in natural light.",
            "Photograph the underside of leaves and the soil surface near the stem.",
            "Include a wider photo showing the full plant and nearby growing conditions.",
        ],
    }
