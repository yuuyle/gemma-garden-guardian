from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_LOG_PATH = Path("data/observations.jsonl")


def log_observation(entry: dict[str, Any], path: Path | str = DEFAULT_LOG_PATH) -> Path:
    """Append one observation entry to a JSONL file."""
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return log_path


def load_observations(path: Path | str = DEFAULT_LOG_PATH, limit: int | None = None) -> list[dict[str, Any]]:
    """Load saved observations from newest to oldest."""
    log_path = Path(path)
    if not log_path.exists():
        return []

    entries: list[dict[str, Any]] = []
    with log_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    entries.reverse()
    if limit is not None:
        return entries[:limit]
    return entries
