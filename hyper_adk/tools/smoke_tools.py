"""ADK tools for public-safe smoke testing."""

from __future__ import annotations

from typing import Any

from hyper_engine.runner import inspect_smoke_run, list_smoke_runs, run_smoke_cycle
from hyper_engine.smoke_data import list_smoke_datasets as _list_smoke_datasets


def list_smoke_datasets() -> dict[str, Any]:
    """List bundled synthetic smoke datasets.

    The listed datasets are synthetic and intended for pipeline verification only.
    They are not the full research datasets used in the large study.
    """

    return _list_smoke_datasets()


def run_smoke_self_learning_cycle(
    dataset: str | None = None,
    split: str = "val",
) -> dict[str, Any]:
    """Run a public-safe self-learning smoke cycle.

    Args:
        dataset: Optional smoke dataset ID, such as "sp500_smoke" or
            "csi300_smoke". Defaults to `HYPER_ADK_DEFAULT_DATASET`.
        split: Data split to evaluate. Defaults to "val".
    """

    return run_smoke_cycle(dataset=dataset, split=split)


def list_smoke_engine_runs() -> dict[str, Any]:
    """List local smoke-cycle run manifests."""

    return list_smoke_runs()


def inspect_smoke_engine_run(run_id: str) -> dict[str, Any]:
    """Inspect one smoke-cycle run manifest.

    Args:
        run_id: Run ID from `list_smoke_engine_runs`.
    """

    return inspect_smoke_run(run_id)
