"""Safe smoke-cycle runner for HyperAgents-ADK."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from hyper_adk.config import load_config
from hyper_engine.artifacts import default_run_id, list_run_manifests, read_manifest, utc_timestamp, write_manifest
from hyper_engine.evaluator import CrossSectionalSmokeEvaluator, EvaluationConfig
from hyper_engine.factor_templates import TEMPLATES, list_factor_templates, run_template
from hyper_engine.smoke_data import list_smoke_datasets, load_panel


def run_smoke_cycle(
    dataset: str | None = None,
    split: str = "val",
    run_id: str | None = None,
    artifact_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run a deterministic, public-safe self-learning smoke cycle."""

    config = load_config()
    selected_dataset = dataset or config.default_dataset
    selected_run_id = run_id or default_run_id()
    panel = load_panel(selected_dataset, split)
    evaluator = CrossSectionalSmokeEvaluator(
        EvaluationConfig(dataset=selected_dataset, split=split)
    )

    candidates = []
    for template_id in TEMPLATES:
        signals = run_template(template_id, panel)
        metrics = evaluator.evaluate_signals(signals)
        candidates.append(
            {
                "template_id": template_id,
                "label": TEMPLATES[template_id].label,
                "description": TEMPLATES[template_id].description,
                "params": TEMPLATES[template_id].default_params,
                "metrics": _rounded_metrics(metrics),
            }
        )

    best_candidate = max(
        candidates,
        key=lambda candidate: candidate["metrics"].get("combined_score", -100.0),
    )
    meta_diagnosis = _diagnose_best_candidate(best_candidate)

    manifest = {
        "run_id": selected_run_id,
        "status": "completed",
        "created_at": utc_timestamp(),
        "dataset": selected_dataset,
        "split": split,
        "sample_data_caveat": (
            "Synthetic smoke data verifies the ADK and evaluator pipeline. It is not "
            "evidence of real financial performance."
        ),
        "execution_mode": {
            "live_runs_enabled": config.enable_live_runs,
            "generated_code_enabled": config.enable_generated_code,
            "arbitrary_generated_code_executed": False,
            "docker_launched": False,
            "template_execution_only": True,
        },
        "task_agent_step": {
            "role": "Propose candidate factor families via whitelisted templates.",
            "candidate_count": len(candidates),
            "available_templates": list_factor_templates(),
        },
        "evaluation_step": {
            "metric_objective": "combined_score = Sharpe + 10 * Rank IC",
            "candidates": candidates,
        },
        "best_candidate": best_candidate,
        "meta_agent_step": meta_diagnosis,
    }
    manifest_path = write_manifest(manifest, artifact_root)
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def list_smoke_runs(artifact_root: str | Path | None = None) -> dict[str, Any]:
    """List local smoke-run manifests."""

    runs = list_run_manifests(artifact_root)
    return {"runs": runs, "count": len(runs)}


def inspect_smoke_run(run_id: str, artifact_root: str | Path | None = None) -> dict[str, Any]:
    """Inspect one smoke-run manifest."""

    return read_manifest(run_id, artifact_root)


def _rounded_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    metric_keys = [
        "combined_score",
        "rank_ic",
        "ic",
        "rank_ic_ir",
        "sharpe_ratio",
        "negative_max_drawdown",
        "turnover",
        "n_valid_days",
        "pnl",
        "can_run",
        "error_message",
    ]
    rounded = {}
    for key in metric_keys:
        value = metrics.get(key)
        rounded[key] = round(value, 6) if isinstance(value, float) else value
    return rounded


def _diagnose_best_candidate(best_candidate: dict[str, Any]) -> dict[str, Any]:
    metrics = best_candidate["metrics"]
    rank_ic = float(metrics.get("rank_ic", 0.0) or 0.0)
    sharpe = float(metrics.get("sharpe_ratio", 0.0) or 0.0)

    if rank_ic < 0:
        proposed_change = "Prioritize rank-stable templates and reduce overfit thresholding."
        risk = "Negative Rank IC suggests the candidate may rank future returns in the wrong direction."
    elif sharpe < 0:
        proposed_change = "Keep the ranking logic but add turnover and drawdown-aware validation checks."
        risk = "Positive ranking quality can still translate into weak long-short behavior after costs."
    else:
        proposed_change = "Test parameter sensitivity on the held-out smoke split before claiming robustness."
        risk = "A good synthetic smoke result can be an artifact of the generated sample process."

    return {
        "role": "Diagnose evaluated candidates and propose the next process improvement.",
        "observed_best_template": best_candidate["template_id"],
        "observed_metrics": metrics,
        "proposed_task_agent_change": proposed_change,
        "proposed_meta_process_change": (
            "Require every candidate summary to separate validation metrics from held-out "
            "checks and to state failure modes before proposing another candidate."
        ),
        "safety_or_overfitting_risk": risk,
        "required_next_check": "Evaluate the selected template on the synthetic test split and compare rank stability.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run HyperAgents-ADK smoke cycle")
    parser.add_argument("--dataset", default=None, help="Smoke dataset ID")
    parser.add_argument("--split", default="val", choices=["train", "val", "test"])
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--list-datasets", action="store_true")
    parser.add_argument("--list-runs", action="store_true")
    args = parser.parse_args()

    if args.list_datasets:
        print(json.dumps(list_smoke_datasets(), indent=2))
        return
    if args.list_runs:
        print(json.dumps(list_smoke_runs(), indent=2))
        return
    print(json.dumps(run_smoke_cycle(args.dataset, args.split, args.run_id), indent=2))


if __name__ == "__main__":
    main()
