"""Configurable cross-sectional evaluator for safe smoke tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from hyper_engine.smoke_data import load_panel


@dataclass(frozen=True)
class EvaluationConfig:
    """Smoke evaluator configuration."""

    dataset: str = "sp500_smoke"
    split: str = "val"
    long_pct: float = 0.10
    short_pct: float = 0.10
    commission_buy: float = 0.0005
    commission_sell: float = 0.0010
    score_sharpe_weight: float = 1.0
    score_rank_ic_weight: float = 10.0
    min_stocks_per_day: int = 10
    min_valid_days: int = 20
    warmup_days: int = 20


class CrossSectionalSmokeEvaluator:
    """Evaluate whitelisted factor-template signals on synthetic panel data."""

    def __init__(self, config: EvaluationConfig | None = None):
        self.config = config or EvaluationConfig()
        self.panel_data = self._load_panel_with_forward_returns()

    def _load_panel_with_forward_returns(self) -> pd.DataFrame:
        panel = load_panel(self.config.dataset, self.config.split)
        panel = panel.sort_values(["symbol", "date"]).reset_index(drop=True)
        panel["forward_return"] = panel.groupby("symbol")["close"].transform(
            lambda series: series.shift(-1) / series - 1
        )
        return panel.sort_values(["date", "symbol"]).reset_index(drop=True)

    def evaluate_signals(self, signals_df: pd.DataFrame) -> dict[str, Any]:
        """Evaluate a DataFrame with columns `date`, `symbol`, and `signal`."""

        default_error = self._default_error_metrics()
        try:
            signals = self._validate_signals(signals_df)
            return self._compute_metrics(signals)
        except Exception as exc:
            default_error["error_message"] = str(exc)
            return default_error

    def _validate_signals(self, signals_df: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(signals_df, pd.DataFrame):
            raise TypeError(f"Expected DataFrame, got {type(signals_df).__name__}")
        missing = [col for col in ("date", "symbol", "signal") if col not in signals_df]
        if missing:
            raise ValueError(f"Signals missing required columns: {missing}")
        signals = signals_df[["date", "symbol", "signal"]].copy()
        signals["date"] = pd.to_datetime(signals["date"])
        signals["signal"] = pd.to_numeric(signals["signal"], errors="coerce").fillna(0.0)
        return signals.sort_values(["date", "symbol"]).reset_index(drop=True)

    def _compute_metrics(self, signals_df: pd.DataFrame) -> dict[str, Any]:
        cfg = self.config
        merged = self.panel_data.merge(
            signals_df,
            on=["date", "symbol"],
            how="left",
        )
        merged["signal"] = pd.to_numeric(merged["signal"], errors="coerce").fillna(0.0)

        dates = sorted(merged["date"].unique())
        if len(dates) > cfg.warmup_days:
            merged = merged[merged["date"] >= dates[cfg.warmup_days]].copy()

        daily_rank_ics: list[float] = []
        daily_ics: list[float] = []
        for _date, group in merged.groupby("date"):
            valid = group.dropna(subset=["forward_return"]).copy()
            valid = valid[valid["signal"] != 0]
            if len(valid) < cfg.min_stocks_per_day:
                continue
            signal_values = valid["signal"].to_numpy(dtype=float)
            return_values = valid["forward_return"].to_numpy(dtype=float)
            mask = ~(
                np.isnan(signal_values)
                | np.isnan(return_values)
                | np.isinf(signal_values)
                | np.isinf(return_values)
            )
            if int(mask.sum()) < cfg.min_stocks_per_day:
                continue
            rank_ic, _ = spearmanr(signal_values[mask], return_values[mask])
            ic, _ = pearsonr(signal_values[mask], return_values[mask])
            if not np.isnan(rank_ic):
                daily_rank_ics.append(float(rank_ic))
            if not np.isnan(ic):
                daily_ics.append(float(ic))

        rank_ic = float(np.mean(daily_rank_ics)) if daily_rank_ics else 0.0
        ic = float(np.mean(daily_ics)) if daily_ics else 0.0
        rank_ic_ir = _safe_mean_over_std(daily_rank_ics)
        ic_ir = _safe_mean_over_std(daily_ics)

        portfolio_returns, daily_turnovers = self._long_short_returns(merged)
        sharpe_ratio = _safe_sharpe(portfolio_returns)
        max_drawdown = _max_drawdown(portfolio_returns)
        turnover = float(np.mean(daily_turnovers)) if daily_turnovers else 0.0
        pnl = float(np.sum(portfolio_returns)) if len(portfolio_returns) else 0.0

        n_valid_days = len(daily_rank_ics)
        combined_score = cfg.score_sharpe_weight * sharpe_ratio + cfg.score_rank_ic_weight * rank_ic
        if rank_ic < 0:
            combined_score = min(combined_score, rank_ic)
        if n_valid_days < cfg.min_valid_days:
            combined_score *= n_valid_days / max(cfg.min_valid_days, 1)

        return {
            "rank_ic": rank_ic,
            "ic": ic,
            "rank_ic_ir": rank_ic_ir,
            "ic_ir": ic_ir,
            "sharpe_ratio": sharpe_ratio,
            "negative_max_drawdown": max_drawdown,
            "turnover": turnover,
            "n_valid_days": n_valid_days,
            "pnl": pnl,
            "combined_score": float(combined_score),
            "can_run": 1.0,
            "error": 0.0,
            "error_message": "",
            "dataset": cfg.dataset,
            "split": cfg.split,
        }

    def _long_short_returns(self, merged: pd.DataFrame) -> tuple[np.ndarray, list[float]]:
        cfg = self.config
        portfolio_returns: list[float] = []
        daily_turnovers: list[float] = []
        prev_long_positions: set[str] = set()
        prev_short_positions: set[str] = set()

        for _date, group in merged.groupby("date"):
            valid = group.dropna(subset=["forward_return"]).copy()
            valid = valid[valid["signal"] != 0]
            if len(valid) < cfg.min_stocks_per_day:
                portfolio_returns.append(0.0)
                daily_turnovers.append(0.0)
                continue

            valid = valid.sort_values("signal", ascending=False)
            n_stocks = len(valid)
            n_long = max(1, int(n_stocks * cfg.long_pct))
            n_short = max(1, int(n_stocks * cfg.short_pct))
            long_stocks = valid.head(n_long)
            short_stocks = valid.tail(n_short)
            ls_return = float(long_stocks["forward_return"].mean() - short_stocks["forward_return"].mean())

            current_long = set(long_stocks["symbol"].tolist())
            current_short = set(short_stocks["symbol"].tolist())
            if prev_long_positions or prev_short_positions:
                n_total = len(current_long | current_short | prev_long_positions | prev_short_positions)
                n_changed = len(
                    current_long.symmetric_difference(prev_long_positions)
                    | current_short.symmetric_difference(prev_short_positions)
                )
                turnover = n_changed / max(n_total, 1)
                avg_commission = (cfg.commission_buy + cfg.commission_sell) / 2
                ls_return -= turnover * avg_commission
                daily_turnovers.append(float(turnover))
            else:
                daily_turnovers.append(0.0)

            prev_long_positions = current_long
            prev_short_positions = current_short
            portfolio_returns.append(ls_return)

        return np.array(portfolio_returns, dtype=float), daily_turnovers

    def _default_error_metrics(self) -> dict[str, Any]:
        return {
            "rank_ic": 0.0,
            "ic": 0.0,
            "rank_ic_ir": 0.0,
            "ic_ir": 0.0,
            "sharpe_ratio": -100.0,
            "negative_max_drawdown": -1.0,
            "turnover": 0.0,
            "n_valid_days": 0,
            "pnl": 0.0,
            "combined_score": -100.0,
            "can_run": 0.0,
            "error": 1.0,
            "error_message": "Evaluation not started",
            "dataset": self.config.dataset,
            "split": self.config.split,
        }


def _safe_mean_over_std(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    std = float(np.std(values))
    return float(np.mean(values) / std) if std > 0 else 0.0


def _safe_sharpe(returns: np.ndarray) -> float:
    if len(returns) <= 1:
        return 0.0
    std = float(np.std(returns))
    if std <= 0:
        return 0.0
    sharpe = float(np.mean(returns) / std * np.sqrt(252))
    return sharpe if np.isfinite(sharpe) else 0.0


def _max_drawdown(returns: np.ndarray) -> float:
    if len(returns) == 0:
        return 0.0
    cumulative = np.cumprod(1 + returns)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    max_drawdown = float(np.min(drawdown)) if len(drawdown) else 0.0
    return max_drawdown if np.isfinite(max_drawdown) else -1.0
