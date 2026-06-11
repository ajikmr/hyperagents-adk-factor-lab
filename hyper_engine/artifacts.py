"""Local artifact helpers for smoke runs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hyper_adk.config import load_config


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_run_id(prefix: str = "smoke") -> str:
    """Create a timestamped local run ID."""

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{stamp}"


def artifact_root(root: str | Path | None = None) -> Path:
    """Return the artifact root path."""

    return Path(root).expanduser().resolve() if root is not None else load_config().artifact_root


def run_dir(run_id: str, root: str | Path | None = None) -> Path:
    """Return the directory for one smoke run."""

    return artifact_root(root) / "runs" / run_id


def write_manifest(payload: dict[str, Any], root: str | Path | None = None) -> Path:
    """Write a smoke-run manifest and return its path."""

    target = run_dir(payload["run_id"], root) / "manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target


def read_manifest(run_id: str, root: str | Path | None = None) -> dict[str, Any]:
    """Read one smoke-run manifest."""

    target = run_dir(run_id, root) / "manifest.json"
    if not target.exists():
        raise FileNotFoundError(f"Smoke-run manifest not found: {target}")
    return json.loads(target.read_text(encoding="utf-8"))


def list_run_manifests(root: str | Path | None = None) -> list[dict[str, Any]]:
    """List local smoke-run manifests."""

    runs_root = artifact_root(root) / "runs"
    if not runs_root.exists():
        return []
    manifests = []
    for manifest_path in sorted(runs_root.glob("*/manifest.json"), reverse=True):
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        manifests.append(
            {
                "run_id": payload.get("run_id"),
                "status": payload.get("status"),
                "dataset": payload.get("dataset"),
                "created_at": payload.get("created_at"),
                "best_template_id": payload.get("best_candidate", {}).get("template_id"),
                "manifest_path": str(manifest_path),
            }
        )
    return manifests
