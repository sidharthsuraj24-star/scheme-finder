"""Load scheme seed data from JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Prefer repo data/ next to backend/, fall back to sibling scheme-finder mirror.
def _candidate_paths() -> list[Path]:
    import os

    env = os.environ.get("SCHEMES_PATH", "").strip()
    paths: list[Path] = []
    if env:
        paths.append(Path(env))
    paths.extend(
        [
            Path(__file__).resolve().parents[2] / "data" / "schemes.json",
            Path(__file__).resolve().parents[1] / "data" / "schemes.json",
            Path("/workspace/scheme-finder-repo/data/schemes.json"),
            Path("/workspace/scheme-finder/data/schemes.json"),
        ]
    )
    return paths


def default_schemes_path() -> Path:
    candidates = _candidate_paths()
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(
        "schemes.json not found. Tried: " + ", ".join(str(p) for p in candidates)
    )


def load_schemes(path: Path | None = None) -> list[dict[str, Any]]:
    schemes_path = path or default_schemes_path()
    with schemes_path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("schemes.json must be a JSON array")
    return data


def index_by_id(schemes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in schemes if "id" in s}
