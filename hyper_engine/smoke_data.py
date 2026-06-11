"""Synthetic smoke-data loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


APP_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ROOT = APP_ROOT / "sample_data"
REQUIRED_COLUMNS = ["date", "symbol", "open", "high", "low", "close", "volume"]
SUPPORTED_SPLITS = ("train", "val", "test")


def dataset_path(dataset: str, split: str) -> Path:
    """Return the path to one smoke dataset split."""

    if split not in SUPPORTED_SPLITS:
        raise ValueError(f"Unsupported split '{split}'. Expected one of {SUPPORTED_SPLITS}.")
    return SAMPLE_ROOT / dataset / f"smoke_daily_panel_{split}.csv"


def load_panel(dataset: str = "sp500_smoke", split: str = "val") -> pd.DataFrame:
    """Load and validate one synthetic OHLCV smoke panel."""

    path = dataset_path(dataset, split)
    if not path.exists():
        raise FileNotFoundError(f"Smoke dataset split not found: {path}")

    panel = pd.read_csv(path, parse_dates=["date"])
    missing = [column for column in REQUIRED_COLUMNS if column not in panel.columns]
    if missing:
        raise ValueError(f"Smoke dataset {path} is missing required columns: {missing}")

    panel = panel[REQUIRED_COLUMNS].copy()
    panel = panel.sort_values(["date", "symbol"]).reset_index(drop=True)
    return panel


def list_smoke_datasets() -> dict[str, Any]:
    """List bundled smoke datasets and split-level sizes."""

    datasets = []
    if not SAMPLE_ROOT.exists():
        return {"datasets": [], "count": 0, "sample_root": str(SAMPLE_ROOT)}

    for dataset_dir in sorted(path for path in SAMPLE_ROOT.iterdir() if path.is_dir()):
        splits = {}
        for split in SUPPORTED_SPLITS:
            path = dataset_path(dataset_dir.name, split)
            if not path.exists():
                continue
            panel = pd.read_csv(path, usecols=["date", "symbol"])
            splits[split] = {
                "rows": int(len(panel)),
                "dates": int(panel["date"].nunique()),
                "symbols": int(panel["symbol"].nunique()),
                "path": str(path.relative_to(APP_ROOT)),
            }
        datasets.append({"id": dataset_dir.name, "splits": splits})

    return {
        "datasets": datasets,
        "count": len(datasets),
        "sample_root": str(SAMPLE_ROOT),
        "caveat": "Synthetic smoke data verifies pipeline behavior, not real financial performance.",
    }
