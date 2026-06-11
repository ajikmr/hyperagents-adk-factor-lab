"""Configuration helpers for HyperAgents-ADK."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - keeps utility imports lightweight.
    load_dotenv = None  # type: ignore[assignment]


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STUDY_MANIFEST_PATH = APP_ROOT / "hyper_adk" / "data" / "study_manifest.json"
DEFAULT_ARTIFACT_ROOT = APP_ROOT / "artifacts"


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration loaded from environment variables."""

    model: str
    app_root: Path
    study_manifest_path: Path
    artifact_root: Path
    deploy_region: str
    default_dataset: str
    enable_live_runs: bool
    enable_generated_code: bool


def _as_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _as_path(value: str | None, default: Path) -> Path:
    if not value:
        return default
    return Path(value).expanduser().resolve()


def load_config(env_file: str | Path | None = None) -> AppConfig:
    """Load HyperAgents-ADK configuration from `.env` and the environment."""

    if load_dotenv is not None:
        if env_file is not None:
            load_dotenv(Path(env_file))
        else:
            load_dotenv(APP_ROOT / ".env")

    return AppConfig(
        model=os.getenv("HYPER_ADK_MODEL", "gemini-3.5-flash"),
        app_root=APP_ROOT,
        study_manifest_path=_as_path(
            os.getenv("HYPER_ADK_STUDY_MANIFEST_PATH"),
            DEFAULT_STUDY_MANIFEST_PATH,
        ),
        artifact_root=_as_path(
            os.getenv("HYPER_ADK_ARTIFACT_ROOT"),
            DEFAULT_ARTIFACT_ROOT,
        ),
        deploy_region=os.getenv("HYPER_ADK_DEPLOY_REGION", "asia-south1"),
        default_dataset=os.getenv("HYPER_ADK_DEFAULT_DATASET", "sp500_smoke"),
        enable_live_runs=_as_bool(os.getenv("HYPER_ADK_ENABLE_LIVE_RUNS")),
        enable_generated_code=_as_bool(
            os.getenv("HYPER_ADK_ENABLE_GENERATED_CODE")
        ),
    )
