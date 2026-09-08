"""Load scheme seed data from JSON."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

# Repo root = parents[2] of this file (.../backend/app/schemes_loader.py → repo).
_REPO_ROOT = Path(__file__).resolve().parents[2]
# Docker image layout copies data to /app/data.
_ALLOWED_ROOTS = (_REPO_ROOT, Path("/app"), Path("/workspace/scheme-finder-repo"))


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (ValueError, OSError):
        return False


def confine_schemes_path(path: Path) -> Path:
    """Reject paths that escape the repo / container data roots (path traversal)."""
    resolved = path.expanduser().resolve()
    if not any(_is_under(resolved, root) for root in _ALLOWED_ROOTS):
        raise ValueError(
            "SCHEMES_PATH escapes allowed roots "
            f"({', '.join(str(r) for r in _ALLOWED_ROOTS)}): {resolved}"
        )
    if resolved.suffix.lower() != ".json":
        raise ValueError(f"SCHEMES_PATH must be a .json file: {resolved}")
    return resolved


def _candidate_paths() -> list[Path]:
    paths: list[Path] = []
    env = os.environ.get("SCHEMES_PATH", "").strip()
    if env:
        paths.append(confine_schemes_path(Path(env)))
    paths.extend(
        [
            _REPO_ROOT / "data" / "schemes.json",
            Path(__file__).resolve().parents[1] / "data" / "schemes.json",
            Path("/app/data/schemes.json"),
            Path("/workspace/scheme-finder-repo/data/schemes.json"),
        ]
    )
    return paths


def default_schemes_path() -> Path:
    candidates = _candidate_paths()
    for path in candidates:
        if path.is_file():
            return path.resolve()
    raise FileNotFoundError(
        "schemes.json not found. Tried: " + ", ".join(str(p) for p in candidates)
    )


def load_schemes(path: Path | None = None) -> list[dict[str, Any]]:
    schemes_path = confine_schemes_path(path) if path is not None else default_schemes_path()
    with schemes_path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("schemes.json must be a JSON array")
    return data


def index_by_id(schemes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in schemes if "id" in s}
