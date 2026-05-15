from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


RISK_SCORES = {
    "low": 25,
    "medium": 60,
    "high": 90,
}

PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


def create_todo_items(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert recommended actions into simple todo items for the dashboard."""
    todos = [
        {
            "id": f"todo-{index + 1}",
            "title": item["action"],
            "priority": item["priority"],
            "reason": item["reason"],
            "done": False,
        }
        for index, item in enumerate(analysis.get("recommended_actions", []))
    ]
    return sorted(todos, key=lambda item: PRIORITY_ORDER.get(item["priority"], 9))


def calculate_risk_score(analysis: dict[str, Any]) -> int:
    """Map the qualitative risk level plus action urgency to a simple 0-100 score."""
    base_score = RISK_SCORES.get(analysis.get("risk_level", "medium"), 60)
    high_priority_actions = sum(
        1 for item in analysis.get("recommended_actions", []) if item.get("priority") == "high"
    )
    return min(100, base_score + high_priority_actions * 5)


def compare_with_previous(
    current: dict[str, Any],
    previous_entry: dict[str, Any] | None,
) -> list[str]:
    """Create a short human-readable comparison against the previous observation."""
    if not previous_entry:
        return ["No previous observation is available yet for comparison."]

    previous = previous_entry.get("analysis", previous_entry)
    changes = []
    previous_risk = previous.get("risk_level", "unknown")
    current_risk = current.get("risk_level", "unknown")
    if previous_risk != current_risk:
        changes.append(f"Risk changed from {previous_risk} to {current_risk}.")
    else:
        changes.append(f"Risk remains {current_risk}.")

    previous_status = previous.get("overall_status", "unknown")
    current_status = current.get("overall_status", "unknown")
    if previous_status != current_status:
        changes.append(f"Status changed from {previous_status} to {current_status}.")

    changes.append(
        "Please compare photos taken in similar lighting before deciding whether the plant is improving."
    )
    return changes


def build_observation_entry(
    analysis: dict[str, Any],
    image_name: str,
    notes: str,
    source: str,
    risk_score: int,
) -> dict[str, Any]:
    """Wrap an analysis with local metadata before saving it."""
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "image_name": image_name,
        "notes": notes,
        "source": source,
        "risk_score": risk_score,
        "analysis": analysis,
    }
