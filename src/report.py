from __future__ import annotations

from collections import Counter
from typing import Any


def generate_weekly_report(observations: list[dict[str, Any]]) -> str:
    """Generate a compact Markdown report from recent observations."""
    if not observations:
        return "No observations have been logged yet."

    risk_counts = Counter(
        entry.get("analysis", {}).get("risk_level", "unknown") for entry in observations
    )
    latest = observations[0]
    latest_analysis = latest.get("analysis", {})
    latest_summary = latest_analysis.get("summary", "No summary available.")
    top_actions = []
    for entry in observations[:5]:
        for action in entry.get("analysis", {}).get("recommended_actions", [])[:1]:
            top_actions.append(action.get("action", "Review the latest observation."))

    lines = [
        "# Weekly Garden Report",
        "",
        f"Observations reviewed: {len(observations)}",
        f"Risk mix: {dict(risk_counts)}",
        "",
        "## Latest Summary",
        latest_summary,
        "",
        "## Suggested Focus",
    ]
    lines.extend(f"- {action}" for action in top_actions[:5])
    lines.append("")
    lines.append(
        "Confirm important decisions locally and consider consulting a local expert for persistent or severe signs."
    )
    return "\n".join(lines)
