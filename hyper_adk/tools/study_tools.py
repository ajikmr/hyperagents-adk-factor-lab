"""Curated-study inspection tools for HyperAgents-ADK."""

from __future__ import annotations

from typing import Any

from .manifest import find_study, load_manifest


def _matches(value: str | None, candidate: str) -> bool:
    return value is None or value.strip().lower() in candidate.lower()


def _round_metric(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 4)
    return value


def list_available_studies(
    dataset: str | None = None,
    evidence_type: str | None = None,
) -> dict[str, Any]:
    """List curated HyperAgents finance studies.

    Args:
        dataset: Optional dataset filter, such as "sp500" or "csi300".
        evidence_type: Optional evidence filter, such as "validation_selected" or
            "heldout_test".
    """

    manifest = load_manifest()
    studies = []
    for study in manifest.get("studies", []):
        if not _matches(dataset, study.get("dataset", "")):
            continue
        if evidence_type is not None and study.get("evidence_type") != evidence_type:
            continue
        studies.append(
            {
                "id": study["id"],
                "label": study["label"],
                "dataset": study["dataset"],
                "market": study["market"],
                "split_profile": study["split_profile"],
                "evidence_type": study["evidence_type"],
                "runs": study["runs"],
                "takeaway": study["takeaway"],
            }
        )

    return {
        "studies": studies,
        "count": len(studies),
        "filters": {"dataset": dataset, "evidence_type": evidence_type},
        "global_caveats": manifest.get("global_caveats", []),
    }


def get_study_summary(study_id: str) -> dict[str, Any]:
    """Return a compact summary of one curated study.

    Args:
        study_id: Study ID from `list_available_studies`.
    """

    study = find_study(study_id)
    conditions = []
    for condition in study.get("conditions", []):
        conditions.append(
            {
                key: _round_metric(value)
                for key, value in condition.items()
                if key
                in {
                    "id",
                    "label",
                    "parent_selection",
                    "combined_score_mean",
                    "combined_score_std",
                    "rank_ic_mean",
                    "rank_ic_std",
                    "sharpe_mean",
                    "sharpe_std",
                }
            }
        )

    return {
        "id": study["id"],
        "label": study["label"],
        "dataset": study["dataset"],
        "market": study["market"],
        "split_profile": study["split_profile"],
        "evidence_type": study["evidence_type"],
        "runs": study["runs"],
        "source": study["source"],
        "conditions": conditions,
        "takeaway": study["takeaway"],
        "caveats": study.get("caveats", []),
    }


def compare_conditions(
    study_id: str,
    primary_metric: str = "combined_score_mean",
) -> dict[str, Any]:
    """Compare conditions in one curated study.

    Args:
        study_id: Study ID from `list_available_studies`.
        primary_metric: Metric key to rank conditions by. Common values include
            "combined_score_mean", "rank_ic_mean", and "sharpe_mean".
    """

    study = find_study(study_id)
    conditions = study.get("conditions", [])
    if not conditions:
        return {"study_id": study_id, "error": "Study has no conditions."}

    ranked = sorted(
        conditions,
        key=lambda item: item.get(primary_metric, float("-inf")),
        reverse=True,
    )
    return {
        "study_id": study_id,
        "label": study["label"],
        "evidence_type": study["evidence_type"],
        "primary_metric": primary_metric,
        "best_condition": {
            "id": ranked[0]["id"],
            "label": ranked[0]["label"],
            "value": _round_metric(ranked[0].get(primary_metric)),
        },
        "ranked_conditions": [
            {
                "id": condition["id"],
                "label": condition["label"],
                primary_metric: _round_metric(condition.get(primary_metric)),
                "rank_ic_mean": _round_metric(condition.get("rank_ic_mean")),
                "sharpe_mean": _round_metric(condition.get("sharpe_mean")),
            }
            for condition in ranked
        ],
        "interpretation_warning": (
            "Validation-selected rankings are not final out-of-sample claims. "
            "Held-out test studies should be weighted more heavily for future "
            "generalization."
        ),
        "study_caveats": study.get("caveats", []),
    }
