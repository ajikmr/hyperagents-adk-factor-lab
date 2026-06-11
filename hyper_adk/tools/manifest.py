"""Manifest loading utilities for curated HyperAgents-ADK study evidence."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from hyper_adk.config import load_config


@lru_cache(maxsize=4)
def _load_manifest_cached(path: str) -> dict[str, Any]:
    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_manifest(path: str | Path | None = None) -> dict[str, Any]:
    """Load the curated study manifest."""

    manifest_path = Path(path) if path is not None else load_config().study_manifest_path
    return _load_manifest_cached(str(manifest_path.resolve()))


def find_study(study_id: str) -> dict[str, Any]:
    """Find one study by ID."""

    manifest = load_manifest()
    for study in manifest.get("studies", []):
        if study.get("id") == study_id:
            return study
    available = [study.get("id") for study in manifest.get("studies", [])]
    raise ValueError(f"Unknown study_id '{study_id}'. Available studies: {available}")
