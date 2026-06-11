"""Whitelisted factor templates for public smoke tests."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


SignalFunction = Callable[[pd.DataFrame, dict[str, Any]], pd.DataFrame]


@dataclass(frozen=True)
class FactorTemplate:
    """Metadata and callable for one safe factor template."""

    id: str
    label: str
    description: str
    default_params: dict[str, Any]
    function: SignalFunction


def _rank_to_centered_signal(series: pd.Series) -> pd.Series:
    return series.rank(pct=True, method="average") - 0.5


def _safe_ranked(raw: pd.Series, dates: pd.Series) -> pd.Series:
    ranked = raw.groupby(dates).transform(_rank_to_centered_signal)
    return ranked.replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(-0.5, 0.5)


def _base_frame(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values(["symbol", "date"]).reset_index(drop=True)


def short_reversal_vol_scaled(data: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    """Short-horizon reversal scaled by rolling volatility."""

    df = _base_frame(data)
    lookback = int(params.get("lookback", 5))
    vol_window = int(params.get("vol_window", 20))
    eps = float(params.get("eps", 1e-8))
    grouped = df.groupby("symbol", group_keys=False)
    df["ret1"] = grouped["close"].pct_change()
    df["ret_n"] = grouped["close"].pct_change(lookback)
    df["volatility"] = grouped["ret1"].transform(
        lambda series: series.rolling(vol_window, min_periods=max(3, vol_window // 4)).std()
    )
    raw = -df["ret_n"] / (df["volatility"] + eps)
    df["signal"] = _safe_ranked(raw, df["date"])
    return df[["date", "symbol", "signal"]]


def momentum_volume_confirmed(data: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    """Medium-horizon momentum with abnormal-volume confirmation."""

    df = _base_frame(data)
    momentum_window = int(params.get("momentum_window", 20))
    vol_window = int(params.get("vol_window", 20))
    volume_window = int(params.get("volume_window", 20))
    eps = float(params.get("eps", 1e-8))
    grouped = df.groupby("symbol", group_keys=False)
    df["ret1"] = grouped["close"].pct_change()
    df["momentum"] = grouped["close"].pct_change(momentum_window)
    df["volatility"] = grouped["ret1"].transform(
        lambda series: series.rolling(vol_window, min_periods=max(3, vol_window // 4)).std()
    )
    df["avg_volume"] = grouped["volume"].transform(
        lambda series: series.rolling(volume_window, min_periods=max(3, volume_window // 4)).mean()
    )
    volume_ratio = df["volume"] / (df["avg_volume"] + eps)
    volume_rank = volume_ratio.groupby(df["date"]).transform(lambda series: series.rank(pct=True))
    raw = (df["momentum"] / (df["volatility"] + eps)) * (0.75 + 0.5 * (volume_rank - 0.5))
    df["signal"] = _safe_ranked(raw, df["date"])
    return df[["date", "symbol", "signal"]]


def range_position_reversal(data: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    """Fade overextended range position while accounting for recent returns."""

    df = _base_frame(data)
    range_window = int(params.get("range_window", 20))
    reversal_window = int(params.get("reversal_window", 3))
    eps = float(params.get("eps", 1e-8))
    grouped = df.groupby("symbol", group_keys=False)
    roll_high = grouped["high"].transform(
        lambda series: series.rolling(range_window, min_periods=max(5, range_window // 4)).max()
    )
    roll_low = grouped["low"].transform(
        lambda series: series.rolling(range_window, min_periods=max(5, range_window // 4)).min()
    )
    range_pos = (df["close"] - roll_low) / (roll_high - roll_low + eps)
    ret_n = grouped["close"].pct_change(reversal_window)
    raw = -(range_pos - 0.5) - 0.25 * ret_n
    df["signal"] = _safe_ranked(raw, df["date"])
    return df[["date", "symbol", "signal"]]


def blend_ranked_ohlcv(data: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    """Simple rank-normalized blend of reversal, momentum, range, and volume."""

    df = _base_frame(data)
    short_window = int(params.get("short_window", 5))
    medium_window = int(params.get("medium_window", 20))
    volume_window = int(params.get("volume_window", 20))
    range_window = int(params.get("range_window", 20))
    eps = float(params.get("eps", 1e-8))
    grouped = df.groupby("symbol", group_keys=False)

    ret_short = grouped["close"].pct_change(short_window)
    ret_medium = grouped["close"].pct_change(medium_window)
    avg_volume = grouped["volume"].transform(
        lambda series: series.rolling(volume_window, min_periods=max(3, volume_window // 4)).mean()
    )
    rel_volume = df["volume"] / (avg_volume + eps)
    roll_high = grouped["high"].transform(
        lambda series: series.rolling(range_window, min_periods=max(5, range_window // 4)).max()
    )
    roll_low = grouped["low"].transform(
        lambda series: series.rolling(range_window, min_periods=max(5, range_window // 4)).min()
    )
    range_pos = (df["close"] - roll_low) / (roll_high - roll_low + eps)

    reversal_rank = _safe_ranked(-ret_short, df["date"])
    momentum_rank = _safe_ranked(ret_medium, df["date"])
    volume_rank = _safe_ranked(rel_volume, df["date"])
    range_rank = _safe_ranked(-(range_pos - 0.5), df["date"])
    df["signal"] = (
        0.35 * reversal_rank + 0.30 * momentum_rank + 0.20 * range_rank + 0.15 * volume_rank
    ).clip(-0.5, 0.5)
    return df[["date", "symbol", "signal"]]


TEMPLATES: dict[str, FactorTemplate] = {
    "short_reversal_vol_scaled": FactorTemplate(
        id="short_reversal_vol_scaled",
        label="Short reversal, volatility scaled",
        description="Short-horizon reversal normalized by rolling volatility and ranked cross-sectionally.",
        default_params={"lookback": 5, "vol_window": 20, "eps": 1e-8},
        function=short_reversal_vol_scaled,
    ),
    "momentum_volume_confirmed": FactorTemplate(
        id="momentum_volume_confirmed",
        label="Momentum with volume confirmation",
        description="Medium-horizon momentum scaled by volatility and mildly conditioned on abnormal volume.",
        default_params={"momentum_window": 20, "vol_window": 20, "volume_window": 20, "eps": 1e-8},
        function=momentum_volume_confirmed,
    ),
    "range_position_reversal": FactorTemplate(
        id="range_position_reversal",
        label="Range-position reversal",
        description="Cross-sectional reversal around recent high-low range position and short-term return.",
        default_params={"range_window": 20, "reversal_window": 3, "eps": 1e-8},
        function=range_position_reversal,
    ),
    "blend_ranked_ohlcv": FactorTemplate(
        id="blend_ranked_ohlcv",
        label="Ranked OHLCV blend",
        description="Simple rank-normalized blend of reversal, momentum, range position, and relative volume.",
        default_params={"short_window": 5, "medium_window": 20, "volume_window": 20, "range_window": 20, "eps": 1e-8},
        function=blend_ranked_ohlcv,
    ),
}


def list_factor_templates() -> list[dict[str, Any]]:
    """Return public metadata for safe factor templates."""

    return [
        {
            "id": template.id,
            "label": template.label,
            "description": template.description,
            "default_params": template.default_params,
        }
        for template in TEMPLATES.values()
    ]


def run_template(
    template_id: str,
    panel: pd.DataFrame,
    params: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Run one whitelisted factor template."""

    if template_id not in TEMPLATES:
        raise ValueError(f"Unknown template_id '{template_id}'. Available: {sorted(TEMPLATES)}")
    template = TEMPLATES[template_id]
    merged_params = dict(template.default_params)
    if params:
        merged_params.update(params)
    signals = template.function(panel, merged_params)
    return signals.sort_values(["date", "symbol"]).reset_index(drop=True)
