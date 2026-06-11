"""Create deterministic synthetic OHLCV panels for HyperAgents-ADK smoke tests."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


APP_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ROOT = APP_ROOT / "sample_data"

DATES = pd.bdate_range("2024-01-02", periods=220)
SPLITS = {
    "train": DATES[:130],
    "val": DATES[130:175],
    "test": DATES[175:],
}

DATASETS = {
    "sp500_smoke": {
        "prefix": "SP",
        "seed": 1729,
        "n_symbols": 48,
        "base_price": 35.0,
        "market_drift": 0.00015,
    },
    "csi300_smoke": {
        "prefix": "CSI",
        "seed": 3141,
        "n_symbols": 48,
        "base_price": 18.0,
        "market_drift": 0.00010,
    },
}


def _make_dataset(name: str, cfg: dict[str, float | int | str]) -> pd.DataFrame:
    rng = np.random.default_rng(int(cfg["seed"]))
    n_symbols = int(cfg["n_symbols"])
    symbols = [f"{cfg['prefix']}{idx:03d}" for idx in range(n_symbols)]

    prices = np.linspace(float(cfg["base_price"]), float(cfg["base_price"]) * 2.4, n_symbols)
    trend_state = rng.normal(0.0, 0.003, n_symbols)
    prior_return = rng.normal(0.0, 0.01, n_symbols)
    liquidity = rng.lognormal(mean=12.0, sigma=0.35, size=n_symbols)

    rows = []
    for day_idx, date in enumerate(DATES):
        market_shock = rng.normal(float(cfg["market_drift"]), 0.004)
        sector_cycle = np.sin(day_idx / 18.0 + np.arange(n_symbols) / 7.0) * 0.0015
        trend_state = 0.94 * trend_state + rng.normal(0.0, 0.0013, n_symbols)

        # Synthetic return process intentionally contains weak momentum and
        # reversal structure so smoke factors produce non-degenerate metrics.
        returns = (
            market_shock
            + sector_cycle
            + 0.35 * trend_state
            - 0.10 * prior_return
            + rng.normal(0.0, 0.012, n_symbols)
        )

        open_prices = prices * (1 + rng.normal(0.0, 0.002, n_symbols))
        close_prices = np.maximum(0.5, prices * (1 + returns))
        intraday_range = np.abs(returns) + rng.uniform(0.004, 0.018, n_symbols)
        high_prices = np.maximum(open_prices, close_prices) * (1 + intraday_range / 2)
        low_prices = np.minimum(open_prices, close_prices) * (1 - intraday_range / 2)
        volume = liquidity * (1 + 12 * np.abs(returns) + rng.normal(0.0, 0.08, n_symbols))
        volume = np.maximum(1_000, volume).astype(int)

        for symbol_idx, symbol in enumerate(symbols):
            rows.append(
                {
                    "date": date.date().isoformat(),
                    "symbol": symbol,
                    "open": round(float(open_prices[symbol_idx]), 4),
                    "high": round(float(high_prices[symbol_idx]), 4),
                    "low": round(float(low_prices[symbol_idx]), 4),
                    "close": round(float(close_prices[symbol_idx]), 4),
                    "volume": int(volume[symbol_idx]),
                }
            )

        prices = close_prices
        prior_return = returns

    return pd.DataFrame(rows)


def _write_dataset(name: str, panel: pd.DataFrame) -> None:
    dataset_root = SAMPLE_ROOT / name
    dataset_root.mkdir(parents=True, exist_ok=True)
    for split, dates in SPLITS.items():
        split_dates = {date.date().isoformat() for date in dates}
        split_df = panel[panel["date"].isin(split_dates)].copy()
        split_df.to_csv(dataset_root / f"smoke_daily_panel_{split}.csv", index=False)


def main() -> None:
    for name, cfg in DATASETS.items():
        panel = _make_dataset(name, cfg)
        _write_dataset(name, panel)
    print(f"Wrote HyperAgents-ADK smoke data under {SAMPLE_ROOT}")


if __name__ == "__main__":
    main()
