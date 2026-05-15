from __future__ import annotations


def create_todo_items(analysis: dict) -> list[dict]:
    """Convert recommended actions into simple todo items for the dashboard."""
    return [
        {
            "title": item["action"],
            "priority": item["priority"],
            "reason": item["reason"],
            "done": False,
        }
        for item in analysis.get("recommended_actions", [])
    ]
